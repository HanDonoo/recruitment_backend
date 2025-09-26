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

@router.get("/latest", response_model=schemas.JobAssessmentOut)
def get_latest_job_assessment(
    applicant_id: int = Query(..., description="Applicant ID"),
    job_id: int = Query(..., description="Job ID"),
    db: Session = Depends(get_db),
):
    result = (
        db.query(models.JobAssessment)
        .filter(
            models.JobAssessment.applicant_id == applicant_id,
            models.JobAssessment.job_id == job_id
        )
        .order_by(models.JobAssessment.version.desc())
        .first()
    )
    if not result:
        raise HTTPException(status_code=404, detail="No assessment found for this applicant and job.")
    return result
