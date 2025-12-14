from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, models
from ..database import get_db

router = APIRouter()


@router.post("/profile", response_model=schemas.StudentOut)
def create_student_profile(payload: schemas.StudentProfileCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == payload.user_id).first()
    if not user or user.role != models.UserRole.student:
        raise HTTPException(status_code=400, detail="Invalid student user")

    existing = db.query(models.Student).filter(models.Student.user_id == user.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student profile already exists")

    student = models.Student(
        user_id=user.id,
        name=payload.name,
        branch=payload.branch,
        year=payload.year,
        cgpa=payload.cgpa,
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return schemas.StudentOut(
        id=student.id, name=student.name, branch=student.branch, year=student.year, cgpa=student.cgpa, skills=[]
    )


@router.get("/{id}", response_model=schemas.StudentOut)
def get_student(id: int, db: Session = Depends(get_db)):
    """Get full enriched student profile"""
    student = db.query(models.Student).filter(models.Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    skills = [ss.skill.name for ss in student.skills]
    return schemas.StudentOut(
        id=student.id,
        name=student.name,
        branch=student.branch,
        year=student.year,
        cgpa=student.cgpa,
        skills=skills,
        projects=student.projects,
        certifications=student.certifications,
        interests=student.interests,
        external_links=student.external_links,
    )


@router.put("/{id}/profile", response_model=schemas.StudentOut)
def update_student_profile(id: int, payload: schemas.StudentProfileUpdate, db: Session = Depends(get_db)):
    """Update student enhanced profile (projects, certifications, interests, links)"""
    student = db.query(models.Student).filter(models.Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Update only provided fields
    if payload.projects is not None:
        student.projects = payload.projects
    if payload.certifications is not None:
        student.certifications = payload.certifications
    if payload.interests is not None:
        student.interests = payload.interests
    if payload.external_links is not None:
        student.external_links = payload.external_links
    
    db.commit()
    db.refresh(student)
    
    skills = [ss.skill.name for ss in student.skills]
    return schemas.StudentOut(
        id=student.id,
        name=student.name,
        branch=student.branch,
        year=student.year,
        cgpa=student.cgpa,
        skills=skills,
        projects=student.projects,
        certifications=student.certifications,
        interests=student.interests,
        external_links=student.external_links,
    )


@router.post("/add-skill")
def add_skill(payload: schemas.StudentSkillCreate, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    skill = db.query(models.Skill).filter(models.Skill.name.ilike(payload.skill_name)).first()
    if not skill:
        skill = models.Skill(name=payload.skill_name)
        db.add(skill)
        db.commit()
        db.refresh(skill)

    # Check for duplicate skill assignment
    existing = (
        db.query(models.StudentSkill)
        .filter(
            models.StudentSkill.student_id == student.id,
            models.StudentSkill.skill_id == skill.id,
        )
        .first()
    )
    if existing:
        # Update existing skill level instead of creating duplicate
        existing.level = payload.level
        db.commit()
        return {"message": "Skill level updated", "skill_id": skill.id, "level": payload.level}

    student_skill = models.StudentSkill(student_id=student.id, skill_id=skill.id, level=payload.level)
    db.add(student_skill)
    db.commit()
    db.refresh(student_skill)
    return {"message": "Skill added", "skill_id": skill.id, "level": payload.level}

