# app/api/routers/webhooks.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal
from .. import schemas  # 注意根据你的项目结构调整导入路径
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("")
async def receive_marketing_comms(
    payload: schemas.MarketingCommBatchIn,
    db: Session = Depends(get_db),
):
    """
    接收 Power Automate 的 POST：
    Body 形如：
    {
      "records": [
        { "title": "...", "detail": "...", ... },
        ...
      ]
    }
    """

    logger.info("Received %d marketing comm records from Power Automate", len(payload.records))

    # 先简单打印一下，确认 Flow 的数据结构
    for idx, rec in enumerate(payload.records):
        logger.info(
            "[%d] title=%s, start_date=%s, customer_base=%s",
            idx,
            rec.title,
            rec.start_date,
            rec.customer_base,
        )

    # 下面是一个“可选”的示例：写进数据库（你有对应的 models 再启用）

    # for rec in payload.records:
    #     db_item = models.MarketingComm(
    #         title=rec.title,
    #         document_type=rec.document_type,
    #         customer_base=rec.customer_base,
    #         customer_type=rec.customer_type,
    #         start_date=rec.start_date,
    #         end_date=rec.end_date,
    #         contact_method=rec.contact_method,
    #         target_group=rec.target_group,
    #         product_base=rec.product_base,
    #         detail=rec.detail,
    #         comms_copy=rec.comms_copy,
    #     )
    #     db.add(db_item)
    # db.commit()

    return {
        "status": "ok",
        "received": len(payload.records),
    }
