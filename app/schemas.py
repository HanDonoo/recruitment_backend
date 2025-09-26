from typing import Optional, Any, Dict
from pydantic import BaseModel, Field, ConfigDict

# 公共基类：等同于 v1 的 orm_mode=True
class ORMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class CompanyCreate(BaseModel):
    name: str
    website: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    location: Optional[str] = None
    logo_url: Optional[str] = None

class CompanyOut(CompanyCreate, ORMBase):
    id: int

class JobCreate(BaseModel):
    title: str
    description: Optional[str] = None
    role: str
    location: Optional[str] = None
    employment_type: Optional[str] = None
    skill_tags: Optional[str] = None
    salary: Optional[str] = None
    company_id: Optional[int] = None
    company_name: Optional[str] = None

class JobOut(JobCreate, ORMBase):
    id: int

class ApplicantCreate(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    desired_role: str
    desired_location: Optional[str] = None
    skill_tags: Optional[str] = None

class ApplicantOut(ApplicantCreate, ORMBase):
    id: int

class ApplicationCreate(BaseModel):
    applicant_id: int
    job_id: int
    job_assessment_id: Optional[int] = None
    status: Optional[str] = Field(default="pending", max_length=50)

class ApplicationOut(ApplicationCreate, ORMBase):
    id: int
    created_at: Optional[str]
    updated_at: Optional[str]

class JobAssessmentCreate(BaseModel):
    applicant_id: int
    job_id: int
    version: str = Field(..., max_length=40)
    data_json: dict

class JobAssessmentOut(JobAssessmentCreate, ORMBase):
    id: int
    created_at: Optional[str]
    updated_at: Optional[str]