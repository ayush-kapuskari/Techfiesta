from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas, models
from ..database import get_db
from ..utils.password import hash_password, verify_password
from ..utils.jwt_handler import create_access_token

router = APIRouter()


@router.post("/register", response_model=schemas.Token)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user = models.User(email=user_in.email, password=hash_password(user_in.password), role=user_in.role)
    db.add(user)
    db.commit()
    db.refresh(user)

    if user_in.role == models.UserRole.student:
        if not (user_in.name and user_in.branch and user_in.year and user_in.cgpa is not None):
            raise HTTPException(status_code=400, detail="Student details required")
        student = models.Student(
            user_id=user.id,
            name=user_in.name,
            branch=user_in.branch,
            year=user_in.year,
            cgpa=user_in.cgpa,
        )
        db.add(student)
    elif user_in.role == models.UserRole.faculty:
        if not (user_in.name and user_in.department):
            raise HTTPException(status_code=400, detail="Faculty details required")
        faculty = models.Faculty(user_id=user.id, name=user_in.name, department=user_in.department)
        db.add(faculty)
    elif user_in.role == models.UserRole.company:
        if not user_in.name:
            raise HTTPException(status_code=400, detail="Company name required")
        company = models.Company(user_id=user.id, name=user_in.name, description=user_in.description)
        db.add(company)

    db.commit()

    token = create_access_token({"sub": str(user.id), "role": user.role})
    return schemas.Token(access_token=token)


@router.post("/login", response_model=schemas.Token)
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id), "role": user.role})
    return schemas.Token(access_token=token)

