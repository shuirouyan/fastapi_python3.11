from typing import Dict, List
from fastapi import APIRouter, Depends, Request
from logger import logger
from sqlalchemy.ext.asyncio import AsyncSession
import json
from database import get_db
import datetime
from redis.asyncio import Redis
from sqlalchemy import insert, select
from model.PengpaiDatas import PengpaiDatas
import requests


route5 = APIRouter(prefix="/v5", tags=["V5"])


@route5.post("/save", tags=["澎湃新闻"])
async def pengpai_info_msg(
    request: Request,
    db: AsyncSession = Depends(get_db),
    id: str = "default",
    name: str = "default",
):
    """
    记得加try-catch处理，数据库操作失败时，需要回滚
    """
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


@route5.post("/redirect_sagve")
async def redirect_save_method(request: Request, db: AsyncSession = Depends(get_db)):
    home_page = await get_home_page()

    body = await request.body()

    body_str = body.decode("utf-8")

    # body_json = json.loads(body_str)

    logger.info(f"body:, home_page:{home_page}")

    stm = insert(PengpaiDatas).values(msg_json=home_page)
    result = await db.execute(stm)
    result_stat = result.rowcount
    logger.info("result:{result_stat}")
    return {
        "msg": home_page,
        "result": result_stat,
        "timestamp": int(datetime.datetime.timestamp(datetime.datetime.now())),
        "code": 200,
    }


async def get_home_page():
    url = "https://app.thepaper.cn/api/appHome/homePage"
    payload = {
        "smallTopicsCount": 27,
        "insertFinancial": False,
        "adCount": 29,
        "pageNum": 2,
        "specialCardCount": 30,
        "filterIdArray": [
            "32489612",
            "32209583",
            "32489798",
            "32489636",
            "32489796",
            "32489666",
            "32489889",
            "32489888",
            "32489856",
            "32489887",
            "32488927",
            "32489306",
            "32489658",
            "32488915",
            "32488307",
            "32484819",
        ],
    }

    headers = {
        "User-Agent": "okhttp/3.14.9",
        "wd-version": "11.1.5",
        "wd-version-code": "11150",
        "os": "Android",
        "wd-ua": "Dalvik%2F2.1.0%20%28Linux%3B%20U%3B%20Android%209%3B%20GM1900%20Build%2FPQ3A.190705.11211812%29%20%E6%BE%8E%E6%B9%83%E6%96%B0%E9%97%BB%2F11.1.5",
        "wd-token": "",
        "paper-device-id": "767CDD8237CA74E9201723FC054AB82C",
        "build_id": "2",
        "wd-channel": "yingyb",
        "userid": "",
        "network": "1",
        "sdk_int": "28",
        "gps-location": "",
        "wd-uuid": "767CDD8237CA74E9201723FC054AB82C",
        "osv": "28",
        "wd-system": "9",
        "package_name": "com.wondertek.paper",
        "wd-resolution": "900*1600",
        "paper-client-type": "04",
        "wd-client-type": "04",
        "thepaper-timestamp": "1769675019072",
        "thepaper-sign": "4DA80CE6E07871B8FEF23A1B9C3A105F",
        "piccardmode": "3",
        "wd-version": "11.1.5",
        "content-type": "application/json; charset=utf-8",
    }
    resp = requests.post(url=url, headers=headers, json=payload)

    if resp.json() != None:
        datas = resp.json()["data"]
        temp_data = json.dumps(datas, ensure_ascii=False)
        logger.info("datas:{}".format(temp_data))
        return temp_data
    else:
        return None
