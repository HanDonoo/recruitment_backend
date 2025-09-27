from sqlalchemy import Column, BigInteger, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import JSON as MySQLJSON
from .db import Base

class Company(Base):
    __tablename__ = "company"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    website = Column(String(200))
    industry = Column(String(80))
    size = Column(String(40))
    location = Column(String(120))
    logo_url = Column(String(300))
    created_at = Column(DateTime, server_default=func.now())

class Job(Base):
    __tablename__ = "job"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(120), nullable=False)
    description = Column(Text)
    role = Column(String(50), nullable=False)
    location = Column(String(80))
    employment_type = Column(String(50))
    skill_tags = Column(String(500))
    salary = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())
    company_id = Column(BigInteger)          # 逻辑关联，无外键
    company_name = Column(String(150))

class Applicant(Base):
    __tablename__ = "applicant"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120))
    phone = Column(String(30))
    desired_role = Column(String(50), nullable=False)
    desired_location = Column(String(80))
    skill_tags = Column(String(500))
    university = Column(String(100))
    major = Column(String(100))
    year = Column(String(10))
created_at = Column(DateTime, server_default=func.now())

class ApplicationAssessment(Base):
    __tablename__ = "application_assessment"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    application_id = Column(BigInteger, nullable=False)  # 逻辑关联到 application.id
    version = Column(String(40), nullable=False)
    data_json = Column(MySQLJSON, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class JobAssessment(Base):
    __tablename__ = "job_assessment"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    applicant_id = Column(BigInteger, nullable=False)
    job_id = Column(BigInteger, nullable=False)
    version = Column(String(40), nullable=False)
    data_json = Column(MySQLJSON, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Application(Base):
    __tablename__ = "application"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    applicant_id = Column(BigInteger, nullable=False)
    job_id = Column(BigInteger, nullable=False)
    job_assessment_id = Column(BigInteger, nullable=True)
    company_id = Column(BigInteger, nullable=True)
    status = Column(String(50), nullable=False, default="pending")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
