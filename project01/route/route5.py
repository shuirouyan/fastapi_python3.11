from typing import Dict, List
from fastapi import APIRouter, Depends, Request
from logger import logger
from sqlalchemy.ext.asyncio import AsyncSession
import json
from database import get_db
import datetime
from redis.asyncio import Redis
from sqlalchemy import insert, select, func
from model.PengpaiNews import PengpaiNews

route5 = APIRouter(prefix="/v5", tags=["V5"])


@route5.post("/save", tags=["澎湃新闻"])
async def pengpai_info_msg(
    http_request: Request,
    db: AsyncSession = Depends(get_db),
    id: str = "default",
    name: str = "default",
):
    body = await http_request.body()
    body_str = body.decode("utf-8")
    body_json = json.loads(body_str)
    logger.info(f"body:{body_json}, id:{id}, name:{name}")
    if body_str.strip() != "":
        # await redis.setnx(f"pengpai:{name}", body_json)
        # 保存到数据库
        body_json_str = json.dumps(body_json, ensure_ascii=False)
        stm = insert(PengpaiNews).values(
            title=name, news_id=id, content_msg=body_json_str
        )
        pre_stm = select(PengpaiNews).where(PengpaiNews.news_id == id).limit(1)
        exec_result = await db.execute(pre_stm)
        exists_val = exec_result.scalar_one_or_none()
        if exists_val is None:
            result_row = await db.execute(stm)
            rowcount = result_row.rowcount
            logger.info(f"result_row:{rowcount}")
        else:
            logger.info(f"id is dumplicate:{id}")
    else:
        logger.info("Empty body received, id:{id}")
    return {
        "msg": "ok",
        "timestamp": int(datetime.datetime.timestamp(datetime.datetime.now())),
    }


@route5.get("/get", tags=["澎湃新闻"])
async def get_pengpai_news(
    http_request: Request, db: AsyncSession = Depends(get_db), size: int = 10, page: int = 1
):
    # 参数边界验证
    if page < 1:
        page = 1
    if size < 1:
        size = 10
    if size > 100:
        size = 100

    # 查询总数
    count_stmt = select(func.count(PengpaiNews.id))
    count_result = await db.execute(count_stmt)
    total = count_result.scalar()

    # 分页查询
    stm = (
        select(PengpaiNews)
        .order_by(PengpaiNews.id.desc())
        .offset((page - 1) * size)
        .limit(size)
    )
    result = await db.execute(stm)
    all_page_data = result.mappings().all()

    # 返回带分页元数据的结果
    return {
        "data": all_page_data,
        "pagination": {
            "page": page,
            "size": size,
            "total": total,
            "total_pages": (total + size - 1) // size,
        }
    }
