from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, models
from ..database import get_db

router = APIRouter()


@router.post("/create")
def create_faculty(user_id: int, name: str, department: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id, models.User.role == models.UserRole.faculty).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid faculty user")

    exists = db.query(models.Faculty).filter(models.Faculty.user_id == user.id).first()
    if exists:
        raise HTTPException(status_code=400, detail="Faculty profile already exists")

    faculty = models.Faculty(user_id=user.id, name=name, department=department)
    db.add(faculty)
    db.commit()
    db.refresh(faculty)
    return {"id": faculty.id, "name": faculty.name, "department": faculty.department}


@router.get("/{id}")
def get_faculty(id: int, db: Session = Depends(get_db)):
    faculty = db.query(models.Faculty).filter(models.Faculty.id == id).first()
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return {"id": faculty.id, "name": faculty.name, "department": faculty.department}

