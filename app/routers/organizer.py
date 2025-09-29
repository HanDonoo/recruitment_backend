# app/routers/organizer.py

from fastapi import APIRouter, Depends
# 假设 db.py 提供了 get_db_engine 函数
from app.db import get_db_engine
from sqlalchemy import create_engine
from typing import List

# 导入 service 函数和 schema
from app.services.organizer import get_core_stats, get_daily_trends, get_company_leaderboard, get_application_status_counts
from app.schemas import OrganizerStatsOut, ApplicationTrend, CompanyLeaderboardItem, ApplicationStatusCount

router = APIRouter(
    prefix="/organizer",
    tags=["Organizer Dashboard"],
)

@router.get("/stats", response_model=OrganizerStatsOut)
def read_core_stats(engine: create_engine = Depends(get_db_engine)):

    stats = get_core_stats(engine)
    if stats is None:
        # 如果数据库没有数据，返回默认值
        return OrganizerStatsOut(
            total_students=0, total_companies=0, total_applications=0,
            total_interviews=0, placement_rate=0.0, active_jobs=0
        )
    return stats

@router.get("/trends", response_model=List[ApplicationTrend])
def read_application_trends(engine: create_engine = Depends(get_db_engine), limit: int = 7):

    trends_data = get_daily_trends(engine, limit_days=limit)
    return trends_data

@router.get("/leaderboard", response_model=List[CompanyLeaderboardItem])
def read_company_leaderboard(engine: create_engine = Depends(get_db_engine), limit: int = 5):

    leaderboard = get_company_leaderboard(engine, limit=limit)
    return leaderboard

@router.get("/status_counts", response_model=List[ApplicationStatusCount])
def read_application_status_counts(engine: create_engine = Depends(get_db_engine)):

    counts = get_application_status_counts(engine)
    return counts