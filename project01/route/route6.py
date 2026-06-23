from typing import Dict, List
from fastapi import APIRouter, Depends, Request
from logger import logger
from sqlalchemy.ext.asyncio import AsyncSession
import json
from database import get_db
import datetime
from redis.asyncio import Redis
from sqlalchemy import insert, select
from model.WeixinReader import WeixinReader
import requests


route6 = APIRouter(prefix="/v6", tags=["V6"])



@route6.post("/weixinreader")
async def getWeixinReader(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    try:
        body = await request.body()
        body_str = body.decode("utf-8")
        body_json = json.loads(body_str)
        logger.info(f"body:{body_json}")
        if body_json is not None and body_str is not None and body_str != "":
            for item in body_json['data']['cell_view']['cell_data']:
                body_title = item['video_data'][0]['title']
                body_intro = item['video_data'][0]['video_desc']
                body_id = item['video_data'][0]['vid']
                item_str = json.dumps(item, ensure_ascii=False)
                logger.info(f'body_title:{body_title}, body_intro:{body_intro}')
                query_stm = select(WeixinReader).where(WeixinReader.id == body_id).limit(1)
                exists_val = await db.execute(query_stm)
                if exists_val.scalar_one_or_none() is None:
                    stm = insert(WeixinReader).values(id=body_id, msg_json=item_str)
                    result = await db.execute(stm)
                    logger.info(f'result rowcount:{result.rowcount}')          

        return {"msg": "ok", "time":int(datetime.datetime.timestamp(datetime.datetime.now()))}
    except Exception as e:
        logger.error(f'request failed: {e}')
        raise Exception(e)