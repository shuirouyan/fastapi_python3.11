


from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, AsyncConnection
from sqlalchemy.ext.asyncio import async_sessionmaker


from logger import logger

MYSQL_URI = "mysql+aiomysql://root:root@127.0.0.1:3306/testdb?charset=utf8mb4"

engine = create_async_engine(MYSQL_URI, echo=True)
async_session_local = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False
    )


async def get_db():
    '''
    获取数据库连接
    '''
    async with async_session_local() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()



async def get_session() -> AsyncSession:
    async with get_engine() as engine:
        async with AsyncSession(engine) as session:
            yield session
