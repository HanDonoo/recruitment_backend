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
