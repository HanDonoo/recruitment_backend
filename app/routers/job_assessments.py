from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db import SessionLocal
from .. import models, schemas

router = APIRouter(prefix="/job-assessments", tags=["JobAssessment"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/latest", response_model=schemas.AssessmentResult)
def get_latest_job_assessment(
    applicant_id: int = Query(...),
    job_id: int = Query(...),
    db: Session = Depends(get_db),
):
    record = (
        db.query(models.JobAssessment)
        .filter(
            models.JobAssessment.applicant_id == applicant_id,
            models.JobAssessment.job_id == job_id
        )
        .order_by(models.JobAssessment.version.desc())
        .first()
    )
    if not record:
        raise HTTPException(status_code=404, detail="No assessment found")

    data = record.data_json
    return schemas.AssessmentResult(
        jobId=record.job_id,
        applicantId=record.applicant_id,
        summary=data.get("summary", ""),
        score=schemas.Score(**data.get("score", {})),
        assessment_highlights=data.get("assessment_highlights", []),
        recommendations_for_candidate=data.get("recommendations_for_candidate", []),
        createdAt=record.created_at.isoformat() if record.created_at else ""
    )
