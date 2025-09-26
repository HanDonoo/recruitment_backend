from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db import SessionLocal
from .. import models, schemas

router = APIRouter(prefix="/assessments", tags=["assessments"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=list[schemas.AssessmentOut])
def list_assessments(
    application_id: int | None = Query(None, description="按申请ID筛选"),
    version: str | None = Query(None, description="指定版本"),
    latest_only: bool = Query(False, description="当提供 application_id 时，仅返回最新一条"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    stmt = db.query(models.ApplicationAssessment)
    if application_id:
        stmt = stmt.filter(models.ApplicationAssessment.application_id == application_id)
    if version:
        stmt = stmt.filter(models.ApplicationAssessment.version == version)

    stmt = stmt.order_by(models.ApplicationAssessment.created_at.desc())

    if latest_only and application_id:
        # 仅当给了 application_id 时，返回最新一条
        item = stmt.first()
        return [] if not item else [item]

    items = stmt.offset(offset).limit(limit).all()
    return items

@router.get("/{assessment_id}", response_model=schemas.AssessmentOut)
def get_assessment(assessment_id: int, db: Session = Depends(get_db)):
    item = db.get(models.ApplicationAssessment, assessment_id)
    if not item:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return item
