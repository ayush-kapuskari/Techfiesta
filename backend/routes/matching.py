from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..services.matching_engine import calculate_fit_score

router = APIRouter()


@router.get("/{student_id}", response_model=list[schemas.MatchResult])
def get_matches(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    opportunities = db.query(models.Opportunity).all()
    if not opportunities:
        return []
    results = [calculate_fit_score(db, student, opp) for opp in opportunities]
    # Sort by fit_score descending (best matches first)
    results.sort(key=lambda x: x["fit_score"], reverse=True)
    return results

