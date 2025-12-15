from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .routes import (
    auth_routes,
    student,
    faculty,
    company,
    opportunity,
    application,
    matching,
    team,
    notification,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Campus Opportunity Platform", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router, tags=["auth"])
app.include_router(student.router, prefix="/student", tags=["student"])
app.include_router(faculty.router, prefix="/faculty", tags=["faculty"])
app.include_router(company.router, prefix="/company", tags=["company"])
app.include_router(opportunity.router, prefix="/opportunity", tags=["opportunity"])
app.include_router(application.router, prefix="/applications", tags=["applications"])
app.include_router(matching.router, prefix="/matching", tags=["matching"])
app.include_router(team.router, prefix="/team", tags=["team"])
app.include_router(notification.router, prefix="/notifications", tags=["notifications"])


@app.get("/")
def read_root():
    return {"status": "ok", "message": "Campus AI Opportunity API"}

