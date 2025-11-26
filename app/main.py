from fastapi import FastAPI
from app.routers import jobs, applicants, companies, job_assessments, applications, interviews, organizer, webhooks
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="RECRUITMENT MVP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(jobs.router)
app.include_router(applicants.router)
app.include_router(companies.router)
app.include_router(job_assessments.router)
app.include_router(applications.router)
app.include_router(interviews.router)
app.include_router(organizer.router)
app.include_router(webhooks.router)
