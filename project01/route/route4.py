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
    if not body:
        logger.info(f"Empty body received, id:{id}")
        return {
            "msg": "ok",
            "timestamp": int(datetime.datetime.timestamp(datetime.datetime.now())),
        }

    try:
        body_str = body.decode("utf-8")
        body_json = json.loads(body_str)
        logger.info(f"body:{body_json}")
        # 将 JSON 对象转换为格式化的汉字字符串存储
        json_str = json.dumps(body_json, ensure_ascii=False, indent=2)
        if json_str.strip() != "":
            # await redis.setnx(f"pengpai:{id}", json_str)
            await redis.zadd(f"pengpai", {name: id})
        else:
            pass
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON received, id:{id}, error:{e}")
        return {
            "msg": "invalid JSON",
            "timestamp": int(datetime.datetime.timestamp(datetime.datetime.now())),
        }
    except Exception as e:
        logger.error(f"Unexpected error, id:{id}, error:{e}")
        return {
            "msg": "internal error",
            "timestamp": int(datetime.datetime.timestamp(datetime.datetime.now())),
        }

    return {
        "msg": "ok",
        "timestamp": int(datetime.datetime.timestamp(datetime.datetime.now())),
    }
