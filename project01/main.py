from fastapi import FastAPI, Request, Depends
import uvicorn
from logger import logger
from sqlalchemy import select
from database import get_db
from model.UserSmsCode import UserSmsCode
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import json
from typing import Dict

logger.info("Starting the FastAPI application")
app = FastAPI()


@app.get("/", name="根目录", tags=["基础功能"])
async def method01() -> dict:
    session = get_db()
    logger.info("Handling request to root endpoint{}".format(session))
    stm = select(UserSmsCode).order_by(UserSmsCode.id.desc())
    # session.execute(stm).all()
    execute_sql = await anext(session)
    try:
        many_number = await execute_sql.execute(stm)
        user = many_number.scalars().all()
        list_user = [u.to_dict() for u in user]
        logger.info("many_number:{}".format(json.dumps(list_user)))
    except Exception as e:
        logger.error("Error executing SQL: {}".format(e))
        raise e
    return {"message": "Hello, World!"}


@app.get("/users", name="用户列表", tags=["用户管理"])
async def read_root(request: Request, get_db: AsyncSession = Depends(get_db)):
    stm = select(UserSmsCode).order_by(UserSmsCode.id.desc())
    result = await get_db.execute(stm)
    users = result.scalars().all()
    list_user = [u.to_dict() for u in users]
    body = await request.body()
    logger.info("Received request: {}".format(body))
    return list_user


@app.get("/get_users", name="获取用户列表", tags=["用户管理"])
async def get_users(name: str = None, db: AsyncSession = Depends(get_db)) -> str:
    stm = select(UserSmsCode).order_by(UserSmsCode.id.desc())
    result = await db.execute(stm)
    users = result.scalars().all()
    list_user = [u.to_dict() for u in users]
    return json.dumps(list_user)


@app.get("/mysql_version", name="获取 MySQL 版本", tags=["数据库管理"])
async def get_mysql_version(db: AsyncSession = Depends(get_db)) -> Dict[str, object]:
    result = await db.execute(text("SELECT VERSION()"))
    version = result.scalar()
    logger.info("MySQL version: {}".format(version))
    result2 = await db.execute(text("select current_timestamp()"))
    current_timestamp = str(result2.scalar())
    result3 = await db.execute(text("show variables"))
    variables_dict = result3.fetchall()
    variables_list = {v[0]: v[1] for v in variables_dict}
    return {
        "mysql_version": version,
        "current_timestamp": current_timestamp,
        "variables_list": variables_list,
    }


if __name__ == "__main__":
    logger.info("Starting the FastAPI application")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
