from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, Enum, Text, JSON
from sqlalchemy.orm import relationship
import enum

from .database import Base


class UserRole(str, enum.Enum):
    student = "student"
    faculty = "faculty"
    company = "company"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)

    student = relationship("Student", back_populates="user", uselist=False, cascade="all, delete-orphan")
    faculty = relationship("Faculty", back_populates="user", uselist=False, cascade="all, delete-orphan")
    company = relationship("Company", back_populates="user", uselist=False, cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    name = Column(String, nullable=False)
    branch = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    cgpa = Column(Float, nullable=False)
    # Enhanced profile fields (using JSON for flexibility)
    projects = Column(JSON, nullable=True)  # List of {title, description, tech_stack}
    certifications = Column(JSON, nullable=True)  # List of {name, issuer, date}
    interests = Column(JSON, nullable=True)  # List of interest strings
    external_links = Column(JSON, nullable=True)  # {github: url, linkedin: url, portfolio: url}

    user = relationship("User", back_populates="student")
    skills = relationship("StudentSkill", back_populates="student", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="student", cascade="all, delete-orphan")
    team_memberships = relationship("Team", back_populates="student", cascade="all, delete-orphan")


class Faculty(Base):
    __tablename__ = "faculty"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    name = Column(String, nullable=False)
    department = Column(String, nullable=False)

    user = relationship("User", back_populates="faculty")
    projects = relationship("Project", back_populates="faculty")
    opportunities = relationship("Opportunity", back_populates="faculty")


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    user = relationship("User", back_populates="company")
    opportunities = relationship("Opportunity", back_populates="company")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    student_skills = relationship("StudentSkill", back_populates="skill")
    opportunity_skills = relationship("OpportunitySkill", back_populates="skill")


class StudentSkill(Base):
    __tablename__ = "student_skills"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    level = Column(Integer, nullable=False)

    student = relationship("Student", back_populates="skills")
    skill = relationship("Skill", back_populates="student_skills")


class OpportunityType(str, enum.Enum):
    internship = "internship"
    project = "project"


class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    creator_name = Column(String, nullable=False)
    type = Column(Enum(OpportunityType), nullable=False)
    min_cgpa = Column(Float, nullable=False, default=0)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"), nullable=True)
    is_internal = Column(Boolean, default=False, nullable=False)  # Internal college opportunities

    company = relationship("Company", back_populates="opportunities")
    faculty = relationship("Faculty", back_populates="opportunities")
    required_skills = relationship("OpportunitySkill", back_populates="opportunity", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="opportunity", cascade="all, delete-orphan")


class OpportunitySkill(Base):
    __tablename__ = "opportunity_skills"

    id = Column(Integer, primary_key=True, index=True)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)

    opportunity = relationship("Opportunity", back_populates="required_skills")
    skill = relationship("Skill", back_populates="opportunity_skills")


class ApplicationStatus(str, enum.Enum):
    applied = "applied"
    shortlisted = "shortlisted"
    rejected = "rejected"


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"), nullable=False)
    status = Column(Enum(ApplicationStatus), nullable=False, default=ApplicationStatus.applied)

    student = relationship("Student", back_populates="applications")
    opportunity = relationship("Opportunity", back_populates="applications")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculty.id"), nullable=False)

    faculty = relationship("Faculty", back_populates="projects")
    teams = relationship("Team", back_populates="project", cascade="all, delete-orphan")


class Team(Base):
    __tablename__ = "team"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    role = Column(String, nullable=False)

    project = relationship("Project", back_populates="teams")
    student = relationship("Student", back_populates="team_memberships")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(String, nullable=False)
    is_read = Column(Boolean, default=False)

    user = relationship("User", back_populates="notifications")

