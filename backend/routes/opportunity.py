from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import schemas, models
from ..database import get_db

router = APIRouter()


@router.post("/create", response_model=schemas.OpportunityOut)
def create_opportunity(payload: schemas.OpportunityCreate, db: Session = Depends(get_db)):
    # Role-based validation: Faculty OR Company, not both
    if payload.company_id is not None and payload.faculty_id is not None:
        raise HTTPException(status_code=400, detail="Cannot specify both company_id and faculty_id")
    
    if payload.company_id is None and payload.faculty_id is None:
        raise HTTPException(status_code=400, detail="Must specify either company_id or faculty_id")
    
    # Validate company_id if provided
    if payload.company_id is not None:
        company = db.query(models.Company).filter(models.Company.id == payload.company_id).first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        # Companies create external opportunities (internships)
        if payload.is_internal:
            raise HTTPException(status_code=400, detail="Companies cannot create internal opportunities")
    
    # Validate faculty_id if provided
    if payload.faculty_id is not None:
        faculty = db.query(models.Faculty).filter(models.Faculty.id == payload.faculty_id).first()
        if not faculty:
            raise HTTPException(status_code=404, detail="Faculty not found")
        # Faculty typically create internal opportunities (projects)
        if not payload.is_internal and payload.type == models.OpportunityType.project:
            # Allow but warn - faculty can create external projects too
            pass
    
    # Validate min_cgpa is within valid range
    if payload.min_cgpa < 0 or payload.min_cgpa > 10:
        raise HTTPException(status_code=400, detail="min_cgpa must be between 0 and 10")
    
    opportunity = models.Opportunity(
        title=payload.title,
        creator_name=payload.creator_name,
        type=payload.type,
        min_cgpa=payload.min_cgpa,
        company_id=payload.company_id,
        faculty_id=payload.faculty_id,
        is_internal=payload.is_internal,
    )
    db.add(opportunity)
    db.commit()
    db.refresh(opportunity)

    required_names = []
    for skill_name in payload.required_skills:
        skill = db.query(models.Skill).filter(models.Skill.name.ilike(skill_name)).first()
        if not skill:
            skill = models.Skill(name=skill_name)
            db.add(skill)
            db.commit()
            db.refresh(skill)
        link = models.OpportunitySkill(opportunity_id=opportunity.id, skill_id=skill.id)
        db.add(link)
        required_names.append(skill.name)
    db.commit()
    return schemas.OpportunityOut(
        id=opportunity.id,
        title=opportunity.title,
        creator_name=opportunity.creator_name,
        type=opportunity.type,
        min_cgpa=opportunity.min_cgpa,
        required_skills=required_names,
        company_id=opportunity.company_id,
        faculty_id=opportunity.faculty_id,
        is_internal=opportunity.is_internal,
    )


@router.get("/all", response_model=list[schemas.OpportunityOut])
def list_opportunities(
    is_internal: Optional[bool] = Query(None, description="Filter by internal/external opportunities"),
    db: Session = Depends(get_db),
):
    query = db.query(models.Opportunity)
    
    # Apply filter if provided
    if is_internal is not None:
        query = query.filter(models.Opportunity.is_internal == is_internal)
    
    opportunities = query.all()
    result = []
    for opp in opportunities:
        skills = [rs.skill.name for rs in opp.required_skills]
        result.append(
            schemas.OpportunityOut(
                id=opp.id,
                title=opp.title,
                creator_name=opp.creator_name,
                type=opp.type,
                min_cgpa=opp.min_cgpa,
                required_skills=skills,
                company_id=opp.company_id,
                faculty_id=opp.faculty_id,
                is_internal=opp.is_internal,
            )
        )
    return result

