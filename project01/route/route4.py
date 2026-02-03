from typing import Dict, List
from fastapi import APIRouter, Depends, Request
from logger import logger

import json
from redis_utils import get_redis_connection
import datetime
from redis.asyncio import Redis

route4 = APIRouter(prefix="/v4", tags=["V4"])


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
