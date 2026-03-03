from typing import Dict, List
from fastapi import APIRouter, Depends, Request
from logger import logger
from sqlalchemy.ext.asyncio import AsyncSession
import json
from database import get_db
import datetime
from redis.asyncio import Redis
from sqlalchemy import insert
from model.PengpaiNews import PengpaiNews

route5 = APIRouter(prefix="/v5", tags=["V5"])


@route5.post("/save", tags=["澎湃新闻"])
async def pengpai_info_msg(
    request: Request,
    db: AsyncSession = Depends(get_db),
    id: str = "default",
    name: str = "default",
):
    body = await request.body()
    body_str = body.decode("utf-8")
    body_json = json.loads(body_str)
    logger.info(f"body:{body_json}, id:{id}, name:{name}")
    if body != None and body_str.strip() != "":
        # await redis.setnx(f"pengpai:{name}", body_json)
        # 保存到数据库
        body_json_str = json.dumps(body_json, ensure_ascii=False)
        stm = insert(PengpaiNews).values(
            title=name, news_id=id, content_msg=body_json_str
        )
        result_row = await db.execute(stm)
        rowcount = result_row.rowcount
        logger.info(f"result_row:{rowcount}")
    else:
        logger.info("Empty body received, id:{id}")
    return {
        "msg": "ok",
        "timestamp": int(datetime.datetime.timestamp(datetime.datetime.now())),
    }
