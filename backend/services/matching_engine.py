from sqlalchemy.orm import Session

from ..models import Student, Opportunity, OpportunitySkill, StudentSkill


def _student_skills_map(db: Session, student_id: int):
    return {
        ss.skill.name.lower(): ss.level
        for ss in db.query(StudentSkill).filter(StudentSkill.student_id == student_id).all()
    }


def calculate_fit_score(db: Session, student: Student, opportunity: Opportunity):
    required_skill_names = [
        rs.skill.name.lower()
        for rs in db.query(OpportunitySkill).filter(OpportunitySkill.opportunity_id == opportunity.id).all()
    ]
    student_skills = _student_skills_map(db, student.id)

    if not required_skill_names:
        skill_match = 1
        missing_skills = []
    else:
        matched = sum(1 for s in required_skill_names if s in student_skills)
        skill_match = matched / len(required_skill_names)
        missing_skills = [s for s in required_skill_names if s not in student_skills]

    cgpa_match = 1 if student.cgpa >= opportunity.min_cgpa else 0
    final_score = (0.7 * skill_match) + (0.3 * cgpa_match)
    
    # Ensure fit_score is bounded between 0 and 100
    fit_score = max(0, min(100, round(final_score * 100, 2)))
    
    # Determine eligibility and reason
    eligible = cgpa_match == 1 and skill_match > 0
    reason = None
    if not eligible:
        reasons = []
        if cgpa_match == 0:
            reasons.append(f"CGPA requirement not met (required: {opportunity.min_cgpa}, student: {student.cgpa})")
        if skill_match == 0:
            reasons.append("No matching skills")
        elif missing_skills:
            reasons.append(f"Missing required skills: {', '.join(missing_skills)}")
        reason = "; ".join(reasons) if reasons else "Not eligible"

    return {
        "opportunity_id": opportunity.id,
        "opportunity": opportunity.title,
        "fit_score": fit_score,
        "eligible": eligible,
        "missing_skills": missing_skills,
        "reason": reason,
    }

