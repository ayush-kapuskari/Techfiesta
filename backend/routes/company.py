from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db

router = APIRouter()


@router.post("/create")
def create_company(user_id: int, name: str, description: str = "", db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id, models.User.role == models.UserRole.company).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid company user")

    exists = db.query(models.Company).filter(models.Company.user_id == user.id).first()
    if exists:
        raise HTTPException(status_code=400, detail="Company profile already exists")

    company = models.Company(user_id=user.id, name=name, description=description)
    db.add(company)
    db.commit()
    db.refresh(company)
    return {"id": company.id, "name": company.name, "description": company.description}


@router.get("/{id}")
def get_company(id: int, db: Session = Depends(get_db)):
    company = db.query(models.Company).filter(models.Company.id == id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return {"id": company.id, "name": company.name, "description": company.description}

