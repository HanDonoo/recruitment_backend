from fastapi import FastAPI
from app.routers import jobs, applicants, companies, job_assessments, applications, interviews, organizer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="RECRUITMENT MVP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://127.0.0.1:3000"],
    allow_credentials=True,
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
