from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db import SessionLocal
from .. import models, schemas

router = APIRouter(prefix="/companies", tags=["companies"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=list[schemas.CompanyOut])
def list_companies(
    q: str | None = Query(None, description="模糊搜索 name/industry/location"),
    location: str | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    stmt = db.query(models.Company)
    if location:
        stmt = stmt.filter(models.Company.location == location)
    if q:
        like = f"%{q}%"
        stmt = stmt.filter(
            (models.Company.name.like(like)) |
            (models.Company.industry.like(like)) |
            (models.Company.location.like(like))
        )
    items = (
        stmt.order_by(models.Company.created_at.desc())
        .offset(offset).limit(limit).all()
    )
    return items

@router.get("/{company_id}", response_model=schemas.CompanyOut)
def get_company(company_id: int, db: Session = Depends(get_db)):
    item = db.get(models.Company, company_id)
    if not item:
        raise HTTPException(status_code=404, detail="Company not found")
    return item
