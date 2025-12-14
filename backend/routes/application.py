from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, models
from ..database import get_db
from ..services.notification import create_notification

router = APIRouter()


@router.post("/apply", response_model=schemas.ApplicationOut)
def apply(payload: schemas.ApplicationCreate, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == payload.student_id).first()
    opportunity = db.query(models.Opportunity).filter(models.Opportunity.id == payload.opportunity_id).first()
    if not student or not opportunity:
        raise HTTPException(status_code=404, detail="Student or Opportunity not found")

    existing = (
        db.query(models.Application)
        .filter(
            models.Application.student_id == student.id,
            models.Application.opportunity_id == opportunity.id,
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Already applied")

    application = models.Application(student_id=student.id, opportunity_id=opportunity.id)
    db.add(application)
    db.commit()
    db.refresh(application)

    create_notification(
        db,
        user_id=student.user_id,
        message=f"You applied to {opportunity.title}",
    )

    return schemas.ApplicationOut(
        id=application.id,
        student_id=application.student_id,
        opportunity_id=application.opportunity_id,
        status=application.status,
    )


@router.get("/student/{student_id}", response_model=list[schemas.ApplicationOut])
def list_student_applications(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    applications = db.query(models.Application).filter(models.Application.student_id == student_id).all()
    return [
        schemas.ApplicationOut(
            id=app.id,
            student_id=app.student_id,
            opportunity_id=app.opportunity_id,
            status=app.status,
        )
        for app in applications
    ]

