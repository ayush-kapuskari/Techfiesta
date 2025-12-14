from typing import List
from sqlalchemy.orm import Session

from ..models import Project, Team, Student, StudentSkill, Skill
from .notification import create_notification


def _find_or_create_skill(db: Session, skill_name: str) -> Skill:
    skill = db.query(Skill).filter(Skill.name.ilike(skill_name)).first()
    if not skill:
        skill = Skill(name=skill_name)
        db.add(skill)
        db.commit()
        db.refresh(skill)
    return skill


def generate_team(
    db: Session,
    project_title: str,
    faculty_id: int,
    required_roles: List[dict],
):
    project = Project(title=project_title, faculty_id=faculty_id)
    db.add(project)
    db.commit()
    db.refresh(project)

    assigned_students = set()
    team_members = []

    for role_req in required_roles:
        skill_name = role_req["skill_name"]
        role_label = role_req["role"]
        skill = _find_or_create_skill(db, skill_name)

        candidate = (
            db.query(Student)
            .join(StudentSkill, Student.id == StudentSkill.student_id)
            .filter(StudentSkill.skill_id == skill.id)
            .filter(Student.id.notin_(assigned_students))
            .order_by(StudentSkill.level.desc())
            .first()
        )

        if not candidate:
            continue

        # Check for duplicate team assignment (student already in this project)
        existing_team = (
            db.query(Team)
            .filter(Team.project_id == project.id, Team.student_id == candidate.id)
            .first()
        )
        if existing_team:
            continue  # Skip if student already assigned to this project

        team_entry = Team(project_id=project.id, student_id=candidate.id, role=role_label)
        db.add(team_entry)
        db.commit()
        db.refresh(team_entry)
        assigned_students.add(candidate.id)

        create_notification(
            db,
            user_id=candidate.user_id,
            message=f"You have been added to project '{project.title}' as {role_label}",
        )

        team_members.append(
            {
                "student_id": candidate.id,
                "student_name": candidate.name,
                "role": role_label,
            }
        )

    return project, team_members

