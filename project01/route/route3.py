from typing import Dict, List
from fastapi import APIRouter, Depends, status, Query, Body, Request
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from sqlalchemy import select
from model.UserSmsCode import UserSmsCode
from logger import logger

from fastapi.responses import JSONResponse, RedirectResponse
import json

route3 = APIRouter(prefix="/v3", tags=["route3使用JSONResponse"])


@route3.get("/list", tags=["从数据看获取usersmscode"])
async def get_users(db: AsyncSession = Depends(get_db)) -> JSONResponse:
    stm = select(UserSmsCode.id, UserSmsCode.sms_code).order_by(UserSmsCode.id.desc())
    result = await db.execute(statement=stm)
    resp = result.mappings().fetchall()
    logger.info("resp:{},type:{}".format(resp, type(resp)))
    return JSONResponse(
        content=[dict(item) for item in resp], status_code=status.HTTP_200_OK
    )


@route3.post("/redirect", tags=["307重定向"])
async def redirect_method(
    request: Request,
    param1: str = Query(default="参数1"),
    param2: str = Body(default="http://www.baidu.com", embed=True),
) -> RedirectResponse:
    logger.info("param1:{},param2:{}".format(param1, param2))
    headers = request.headers
    # headers["param1"] = param1
    return RedirectResponse(url=param2, headers=headers)
