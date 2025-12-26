from typing import Dict, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from sqlalchemy import select
from model.UserSmsCode import UserSmsCode

route = APIRouter(prefix="/v2", tags=["v2"])


@route.get("/users", name="获取用户列表", tags=["用户管理"])
async def get_users(name: str = None, db: AsyncSession = Depends(get_db)) -> List[Dict]:
    stm = select(UserSmsCode).order_by(UserSmsCode.id.desc())
    result = await db.execute(stm)
    users = result.scalars().all()

    list_user = [u.to_dict() for u in users]

    # return json.dumps(list_user)

    return list_user
