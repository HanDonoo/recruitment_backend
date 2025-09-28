from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from datetime import datetime, timedelta


class DatabaseService:
    def __init__(self, engine):
        self.engine = engine

    def _execute_sql(self, sql_query):
        """通用 SQL 执行辅助函数，返回 dict-like 结果"""
        with Session(self.engine) as session:
            result = session.execute(text(sql_query)).mappings()  # ✅ 修复关键
            return result.fetchall()


# ----------------------------------------------------

def get_core_stats(engine: create_engine):
    """
    获取仪表板的核心统计数据 (Total Students, Companies, etc.)
    """
    db_service = DatabaseService(engine)

    query = """
    SELECT 
        (SELECT COUNT(DISTINCT id) FROM applicant) AS total_students,
        (SELECT COUNT(DISTINCT id) FROM company) AS total_companies,
        (SELECT COUNT(id) FROM application) AS total_applications,
        (SELECT COUNT(id) FROM interviews) AS total_interviews,
        (SELECT COUNT(id) FROM job WHERE status = 'active') AS active_jobs,
        20.0 AS placement_rate
    """

    result = db_service._execute_sql(query)

    if not result:
        return None

    stats = result[0]

    return {
        "total_students": stats['total_students'],
        "total_companies": stats['total_companies'],
        "total_applications": stats['total_applications'],
        "total_interviews": stats['total_interviews'],
        "active_jobs": stats['active_jobs'],
        "placement_rate": round(stats['placement_rate'] or 0, 2)
    }


def get_daily_trends(engine: create_engine, limit_days: int = 7):
    """
    获取日级别的申请和面试趋势数据
    """
    db_service = DatabaseService(engine)

    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

    query = f"""
    SELECT
        DATE_FORMAT(a.created_at, '%Y-%m-%d') AS day_label,
        COUNT(a.id) AS applications,
        COUNT(i.id) AS interviews
    FROM
        application a
    LEFT JOIN
        interviews i ON a.id = i.application_id
    WHERE 
        DATE(a.created_at) >= '{start_date}'
    GROUP BY
        day_label
    ORDER BY
        day_label DESC
    LIMIT {limit_days};
    """

    results = db_service._execute_sql(query)

    return [{
        "day_label": r['day_label'],
        "applications": r['applications'],
        "interviews": r['interviews'],
    } for r in results]


def get_company_leaderboard(engine: create_engine, limit: int = 5):
    """
    获取公司活跃度排行榜
    """
    db_service = DatabaseService(engine)

    query = f"""
    SELECT
        c.name AS company_name,
        COUNT(DISTINCT a.id) AS applications,
        COUNT(DISTINCT i.id) AS interviews,
        COUNT(CASE WHEN a.status = 'accepted' THEN 1 END) AS placements 
    FROM
        company c
    JOIN
        job j ON c.id = j.company_id
    JOIN
        application a ON j.id = a.job_id
    LEFT JOIN
        interviews i ON a.id = i.application_id
    GROUP BY
        c.id, c.name
    ORDER BY
        applications DESC, interviews DESC
    LIMIT {limit};
    """

    results = db_service._execute_sql(query)

    return [{
        "company_name": r['company_name'],
        "applications": r['applications'],
        "interviews": r['interviews'],
        "placements": r['placements'],
    } for r in results]


def get_application_status_counts(engine: create_engine):
    """
    获取所有申请的状态分布（用于 Pie Chart）
    """
    db_service = DatabaseService(engine)

    query = """
    SELECT status, COUNT(id) AS count 
    FROM application 
    GROUP BY status;
    """

    results = db_service._execute_sql(query)

    return [{
        "status": r['status'],
        "count": r['count']
    } for r in results]
