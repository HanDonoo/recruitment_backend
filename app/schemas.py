from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

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
    status: Optional[str] = "active"


class JobOut(JobCreate, ORMBase):
    id: int
    created_at: Optional[datetime]


class ApplicantCreate(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    desired_role: str
    desired_location: Optional[str] = None
    skill_tags: Optional[str] = None
    university: Optional[str] = None
    major: Optional[str] = None
    year: Optional[str] = None


class ApplicantOut(ApplicantCreate, ORMBase):
    id: int


class ApplicationCreate(BaseModel):
    applicant_id: int
    job_id: int
    status: Optional[str] = Field(default="pending", max_length=50)


class ApplicationOut(ApplicationCreate, ORMBase):
    id: int
    applicant_id: int
    job_id: int
    company_id: int
    job_assessment_id: Optional[int]  # 改成 Optional[int]
    status: str

    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class JobAssessmentCreate(BaseModel):
    applicant_id: int
    job_id: int
    version: str = Field(..., max_length=40)
    data_json: dict


class JobAssessmentOut(JobAssessmentCreate, ORMBase):
    id: int

    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class Score(BaseModel):
    overall: int
    skills_match: int
    experience_depth: int
    education_match: int
    potential_fit: int


class AssessmentResult(BaseModel):
    jobId: int
    applicantId: int
    summary: str
    score: Score
    assessment_highlights: List[str]
    recommendations_for_candidate: List[str]
    createdAt: str


class InterviewCreate(BaseModel):
    application_id: int
    job_id: int
    applicant_id: int
    company_id: int
    interviewer_id: Optional[int] = None
    scheduled_time: datetime
    duration_minutes: Optional[int] = None
    type: str
    location_url: Optional[str] = None
    status: Optional[str] = "Pending"
    notes: Optional[str] = None


class InterviewOut(InterviewCreate):
    id: int
    created_at: Optional[datetime]

    class Config:
        from_attributes = True

class OrganizerStatsOut(BaseModel):
    total_students: int
    total_companies: int
    total_applications: int
    total_interviews: int
    placement_rate: float  # 67.5 (百分比，但作为 float)
    active_jobs: int

class ApplicationTrend(BaseModel):
    day_label: str  # 例如: "2025-09-16"
    applications: int
    interviews: int


class ApplicationTrendsOut(BaseModel):
    trends: List[ApplicationTrend]


class ApplicationStatusCount(BaseModel):
    status: str
    count: int


class CompanyLeaderboardItem(BaseModel):
    company_name: str
    applications: int
    interviews: int
    placements: int
