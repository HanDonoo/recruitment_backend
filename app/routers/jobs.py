from fastapi import UploadFile, File, APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal
from .. import models, schemas
from app.services.matching import calc_match_score
import pdfplumber
import docx
import requests

router = APIRouter(prefix="/jobs", tags=["jobs"])

AI_API_URL = "https://assess-cv.lhanddong.workers.dev/"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def extract_text_from_pdf(file: UploadFile) -> str:
    with pdfplumber.open(file.file) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

def extract_text_from_docx(file: UploadFile) -> str:
    doc = docx.Document(file.file)
    return "\n".join([p.text for p in doc.paragraphs])

@router.post("", response_model=schemas.JobOut)
def create_job(payload: schemas.JobCreate, db: Session = Depends(get_db)):
    job = models.Job(**payload.dict())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

@router.get("", response_model=list[schemas.JobOut])
def list_jobs(
    q: str | None = Query(None),
    role: str | None = Query(None),
    location: str | None = Query(None),
    limit: int = 50,
    db: Session = Depends(get_db),
):
    stmt = db.query(models.Job)
    if role:
        stmt = stmt.filter(models.Job.role == role)
    if location:
        stmt = stmt.filter((models.Job.location == location) | (models.Job.location == "Remote"))
    if q:
        like = f"%{q}%"
        stmt = stmt.filter(
            (models.Job.title.like(like)) | (models.Job.description.like(like)) | (models.Job.skill_tags.like(like))
        )
    return stmt.order_by(models.Job.created_at.desc()).limit(limit).all()

@router.get("/{job_id}", response_model=schemas.JobOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/recommend/{applicant_id}")
def recommend_jobs(applicant_id: int, db: Session = Depends(get_db)):
    a = db.get(models.Applicant, applicant_id)
    if not a:
        return []

    jobs = (
        db.query(models.Job)
        .filter(models.Job.role == a.desired_role)
        .filter((models.Job.location == a.desired_location) | (models.Job.location == "Remote") | (a.desired_location == None))
        .order_by(models.Job.created_at.desc())
        .limit(200)
        .all()
    )

    def same_loc(job_loc: str | None) -> bool:
        return bool(a.desired_location and (job_loc == a.desired_location or job_loc == "Remote"))

    result = []
    for j in jobs:
        score = calc_match_score(a.skill_tags, j.skill_tags, same_loc(j.location))
        result.append({
            "id": j.id,
            "title": j.title,
            "company_name": j.company_name,
            "location": j.location,
            "role": j.role,
            "employment_type": j.employment_type,
            "skill_tags": j.skill_tags,
            "salary": j.salary,
            "matchScore": score,
            "created_at": j.created_at,
        })
    result.sort(key=lambda x: (-x["matchScore"], x["created_at"]))
    return result[:50]

@router.post("/{job_id}/assess")
async def assess_cv(
    job_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # 获取 Job 数据
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # 解析简历文字
    ext = file.filename.lower()
    if ext.endswith(".pdf"):
        resume_text = extract_text_from_pdf(file)
    elif ext.endswith(".docx"):
        resume_text = extract_text_from_docx(file)
    elif ext.endswith(".txt"):
        resume_text = await file.read()
        resume_text = resume_text.decode("utf-8")
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    # 构建请求体
    payload = {
        "jd_text": job.description,
        "resume_text": resume_text
    }

    # 发送到 AI 服务
    try:
        # response = requests.post(AI_API_URL, json=payload, timeout=300)
        # response.raise_for_status()
        # data = response.json()
        data = {
            "summary": "候选人Mingle Zhang的简历与Generative AI Engineer职位描述有一定匹配，但需要进一步强化相关技能和经验",
            "score": {
                "overall": 60,
                "skills_match": 40,
                "experience_depth": 30,
                "education_match": 50,
                "potential_fit": 80
            },
            "assessment_highlights": [
                "Mingle Zhang在前端开发方面有丰富的经验，熟悉Vue、React和TypeScript等技术栈，具有良好的编码能力和团队合作精神",
                "Mingle Zhang有志向成为全栈开发者，正在学习C#和.net，展现出强烈的学习意愿和转型潜力",
                "Mingle Zhang在项目经验方面有一定的基础，但需要进一步强化相关技能和经验，例如机器学习、深度学习和AI框架"
            ],
            "recommendations_for_candidate": [
                "建议Mingle Zhang学习和掌握机器学习和深度学习相关知识，例如TensorFlow、PyTorch和Keras等框架",
                "建议Mingle Zhang参与一些AI相关的项目或竞赛，例如Kaggle等平台，来丰富自己的经验和技能",
                "建议Mingle Zhang在面试中强调自己的学习意愿和转型潜力，展示出自己对AI领域的兴趣和热情"
            ]
        };
        # 假设 AI 返回的 data 是评估结果，你可以封装成：
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI assessment failed: {e}")
