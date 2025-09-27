from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from app.db import SessionLocal
from .. import models, schemas

router = APIRouter(prefix="/interviews", tags=["Interviews"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", response_model=schemas.InterviewOut)
def create_interview(
    interview_in: schemas.InterviewCreate,
    db: Session = Depends(get_db),
):
    interview = models.Interview(**interview_in.dict())
    db.add(interview)
    db.commit()
    db.refresh(interview)
    return interview

@router.get("", response_model=list[schemas.InterviewOut])
def list_interviews(
    applicant_id: int | None = Query(None),
    job_id: int | None = Query(None),
    company_id: int | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    stmt = db.query(models.Interview)
    if applicant_id:
        stmt = stmt.filter(models.Interview.applicant_id == applicant_id)
    if job_id:
        stmt = stmt.filter(models.Interview.job_id == job_id)
    if company_id:
        stmt = stmt.filter(models.Interview.company_id == company_id)

    items = (
        stmt.order_by(models.Interview.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return items

@router.patch("/{interview_id}/status", response_model=schemas.InterviewOut)
def update_interview_status(
    interview_id: int = Path(..., description="Interview ID"),
    new_status: str = Query(..., description="New status (Pending / Confirmed / Cancelled / Completed)"),
    db: Session = Depends(get_db),
):
    interview = db.get(models.Interview, interview_id)
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    if new_status not in {"Pending", "Confirmed", "Cancelled", "Completed"}:
        raise HTTPException(status_code=400, detail="Invalid status value")

    interview.status = new_status
    db.commit()
    db.refresh(interview)
    return interview
