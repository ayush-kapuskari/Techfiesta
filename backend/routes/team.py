from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, models
from ..database import get_db
from ..services.team_engine import generate_team

router = APIRouter()


@router.post("/auto-generate")
def auto_generate_team(
    payload: schemas.TeamGenerationRequest,
    db: Session = Depends(get_db),
):
    faculty = db.query(models.Faculty).filter(models.Faculty.id == payload.faculty_id).first()
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")

    if not payload.required_roles:
        raise HTTPException(status_code=400, detail="At least one required role is needed")

    if not payload.title or not payload.title.strip():
        raise HTTPException(status_code=400, detail="Project title is required")

    required_roles = [role.dict() for role in payload.required_roles]
    project, members = generate_team(
        db=db,
        project_title=payload.title,
        faculty_id=payload.faculty_id,
        required_roles=required_roles,
    )
    return {
        "project_id": project.id,
        "title": project.title,
        "team": members,
    }

