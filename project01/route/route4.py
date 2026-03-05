from typing import Dict, List
from fastapi import APIRouter, Depends, Request
from logger import logger

import json
from redis_utils import get_redis_connection
import datetime
from redis.asyncio import Redis

route4 = APIRouter(prefix="/v4", tags=["澎湃新闻V4"])


@route4.get("/info")
async def get_redis_info(
    request: Request, redis: Redis = Depends(get_redis_connection)
):
    """
    redis info
    """
    body = None
    if body != None:
        body_str = json.dumps(body)
        logger.info(f"body:{body_str}")
    timestamp_str = str(int(datetime.datetime.timestamp(datetime.datetime.now())))
    await redis.set(f"key_val:{timestamp_str}", f"value:{timestamp_str}")
    return {"signature": "asfewaKSFfesfsfjjjKS"}


@route4.post("/save")
async def pengpai_info_msg(
    request: Request,
    redis: Redis = Depends(get_redis_connection),
    id: str = "default",
    name: str = "default",
):
    body = await request.body()
    body_str = body.decode("utf-8")
    body_json = json.loads(body_str)
    logger.info(f"body:{body_json}")
    if body != None and body_str.strip() != "":
        await redis.setnx(f"pengpai:{name}", body_json)
    else:
        logger.info("Empty body received, id:{id}")
    return {
        "msg": "ok",
        "timestamp": int(datetime.datetime.timestamp(datetime.datetime.now())),
    }
