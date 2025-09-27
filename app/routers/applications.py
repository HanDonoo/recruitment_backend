from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db import SessionLocal
from .. import models, schemas

router = APIRouter(prefix="/applications", tags=["Application"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=list[schemas.ApplicationOut])
def list_applications(
    applicant_id: int = Query(..., description="Applicant ID"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    stmt = (
        db.query(models.Application)
        .filter(models.Application.applicant_id == applicant_id)
        .order_by(models.Application.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    results = stmt.all()
    if not results:
        raise HTTPException(status_code=404, detail="No applications found for this applicant.")
    return results

@router.post("", response_model=schemas.ApplicationOut)
def create_application(
    application_in: schemas.ApplicationCreate,
    db: Session = Depends(get_db),
):
    # 1. 检查是否已申请过该岗位
    existing = (
        db.query(models.Application)
        .filter(
            models.Application.applicant_id == application_in.applicant_id,
            models.Application.job_id == application_in.job_id
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="You have already applied for this job.")

    # 2. 查找最新的 job assessment（可选）
    latest_assessment = (
        db.query(models.JobAssessment)
        .filter(
            models.JobAssessment.applicant_id == application_in.applicant_id,
            models.JobAssessment.job_id == application_in.job_id
        )
        .order_by(models.JobAssessment.version.desc())
        .first()
    )

    job_assessment_id = latest_assessment.id if latest_assessment else None

    job = db.query(models.Job).filter(models.Job.id == application_in.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")

    # 3. 创建新的申请
    application = models.Application(
        applicant_id=application_in.applicant_id,
        job_id=application_in.job_id,
        company_id=job.company_id,
        job_assessment_id=job_assessment_id,
        status="pending"
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application

@router.get("/one", response_model=schemas.ApplicationOut | None)
def get_single_application(
    applicant_id: int = Query(..., description="Applicant ID"),
    job_id: int = Query(..., description="Job ID"),
    db: Session = Depends(get_db),
):
    application = (
        db.query(models.Application)
        .filter(
            models.Application.applicant_id == applicant_id,
            models.Application.job_id == job_id
        )
        .first()
    )
    return application

@router.get("/by_job_and_company", response_model=list[schemas.ApplicationOut])
def list_applications_by_job_and_company(
    job_id: int = Query(..., description="Job ID"),
    company_id: int = Query(..., description="Company ID"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    stmt = (
        db.query(models.Application)
        .filter(
            models.Application.job_id == job_id,
            models.Application.company_id == company_id
        )
        .order_by(models.Application.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    results = stmt.all()
    if not results:
        raise HTTPException(status_code=404, detail="No applications found for this job and company.")
    return results

