from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db import SessionLocal
from .. import models, schemas

router = APIRouter(prefix="/applicants", tags=["applicants"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=list[schemas.ApplicantOut])
def list_applicants(
    q: str | None = Query(None, description="模糊搜索 name/email/skill_tags"),
    desired_role: str | None = Query(None),
    desired_location: str | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    stmt = db.query(models.Applicant)
    if desired_role:
        stmt = stmt.filter(models.Applicant.desired_role == desired_role)
    if desired_location:
        stmt = stmt.filter(models.Applicant.desired_location == desired_location)
    if q:
        like = f"%{q}%"
        stmt = stmt.filter(
            (models.Applicant.name.like(like)) |
            (models.Applicant.email.like(like)) |
            (models.Applicant.skill_tags.like(like))
        )
    items = (
        stmt.order_by(models.Applicant.created_at.desc())
        .offset(offset).limit(limit).all()
    )
    return items

@router.get("/by_ids", response_model=list[schemas.ApplicantOut])
def get_applicants_by_ids(
        applicant_ids: str = Query(..., description="Comma separated list of applicant IDs"),
        db: Session = Depends(get_db),
):
    try:
        applicant_ids_list = [int(id) for id in applicant_ids.split(',')]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid applicant IDs format")

    applicants = db.query(models.Applicant).filter(models.Applicant.id.in_(applicant_ids_list)).all()

    if not applicants:
        raise HTTPException(status_code=404, detail="No applicants found for the given IDs.")

    return applicants

@router.get("/{applicant_id}", response_model=schemas.ApplicantOut)
def get_applicant(applicant_id: int, db: Session = Depends(get_db)):
    item = db.get(models.Applicant, applicant_id)
    if not item:
        raise HTTPException(status_code=404, detail="Applicant not found")
    return item
