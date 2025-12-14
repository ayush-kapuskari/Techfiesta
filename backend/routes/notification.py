from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter()


@router.get("/{user_id}", response_model=list[schemas.NotificationOut])
def list_notifications(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    notifs = db.query(models.Notification).filter(models.Notification.user_id == user_id).order_by(models.Notification.id.desc()).all()
    return [
        schemas.NotificationOut(
            id=notif.id,
            message=notif.message,
            is_read=notif.is_read,
        )
        for notif in notifs
    ]

