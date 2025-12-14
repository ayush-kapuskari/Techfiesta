from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from enum import Enum


class UserRole(str, Enum):
    student = "student"
    faculty = "faculty"
    company = "company"


class OpportunityType(str, Enum):
    internship = "internship"
    project = "project"


class ApplicationStatus(str, Enum):
    applied = "applied"
    shortlisted = "shortlisted"
    rejected = "rejected"


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole
    name: Optional[str] = None
    branch: Optional[str] = None
    year: Optional[int] = None
    cgpa: Optional[float] = None
    department: Optional[str] = None
    description: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class StudentProfileCreate(BaseModel):
    user_id: int
    name: str
    branch: str
    year: int = Field(ge=1, le=6)
    cgpa: float = Field(ge=0, le=10)


class StudentSkillCreate(BaseModel):
    student_id: int
    skill_name: str
    level: int = Field(ge=1, le=5)


class StudentOut(BaseModel):
    id: int
    name: str
    branch: str
    year: int
    cgpa: float
    skills: List[str] = []
    projects: Optional[List[dict]] = None
    certifications: Optional[List[dict]] = None
    interests: Optional[List[str]] = None
    external_links: Optional[dict] = None

    class Config:
        from_attributes = True


class StudentProfileUpdate(BaseModel):
    projects: Optional[List[dict]] = None  # [{title, description, tech_stack}]
    certifications: Optional[List[dict]] = None  # [{name, issuer, date}]
    interests: Optional[List[str]] = None
    external_links: Optional[dict] = None  # {github, linkedin, portfolio}


class OpportunityCreate(BaseModel):
    title: str
    creator_name: str
    type: OpportunityType
    min_cgpa: float = 0
    required_skills: List[str] = []
    company_id: Optional[int] = None
    faculty_id: Optional[int] = None
    is_internal: bool = False


class OpportunityOut(BaseModel):
    id: int
    title: str
    creator_name: str
    type: OpportunityType
    min_cgpa: float
    required_skills: List[str]
    company_id: Optional[int] = None
    faculty_id: Optional[int] = None
    is_internal: bool = False

    class Config:
        from_attributes = True


class ApplicationCreate(BaseModel):
    student_id: int
    opportunity_id: int


class ApplicationOut(BaseModel):
    id: int
    student_id: int
    opportunity_id: int
    status: ApplicationStatus

    class Config:
        from_attributes = True


class MatchResult(BaseModel):
    opportunity_id: int
    opportunity: str
    fit_score: float
    eligible: bool
    missing_skills: List[str]
    reason: Optional[str] = None  # Clear reason if not eligible


class TeamRoleRequirement(BaseModel):
    role: str
    skill_name: str


class TeamGenerationRequest(BaseModel):
    faculty_id: int
    title: str
    required_roles: List[TeamRoleRequirement]


class TeamMemberOut(BaseModel):
    student_id: int
    role: str
    student_name: str


class NotificationOut(BaseModel):
    id: int
    message: str
    is_read: bool

    class Config:
        from_attributes = True

