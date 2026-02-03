import asyncio
from redis.asyncio import Redis, ConnectionPool
from fastapi import Depends, HTTPException
from logger import logger

# 全局连接池和锁
_redis_pool = None
_redis_lock = asyncio.Lock()

# Redis 配置
REDIS_HOST = "192.168.159.17"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = "redis"
REDIS_POOL_MAX = 5

async def get_redis_pool():
    """获取或创建 Redis 连接池（线程安全）"""
    global _redis_pool
    
    async with _redis_lock:
        if _redis_pool is None:
            logger.info("Creating Redis connection pool")
            
            # 创建连接池配置
            pool = ConnectionPool(
                host=REDIS_HOST,
                port=REDIS_PORT,
                db=REDIS_DB,
                password=REDIS_PASSWORD,
                max_connections=REDIS_POOL_MAX,
                decode_responses=True,  # 自动解码为字符串
                encoding="utf-8"
            )
            
            # 创建 Redis 客户端实例
            _redis_pool = Redis(connection_pool=pool)
            
            # 测试连接
            try:
                await _redis_pool.ping()
                logger.info("Redis connection established")
            except Exception as e:
                logger.error(f"Redis connection failed: {str(e)}")
                raise
                
    return _redis_pool

async def get_redis_connection():
    """获取 Redis 连接（从连接池）"""
    return await get_redis_pool()

async def close_redis_pool():
    """关闭 Redis 连接池"""
    global _redis_pool
    if _redis_pool:
        logger.info("Closing Redis connection pool")
        await _redis_pool.close()
        await _redis_pool.connection_pool.disconnect()  # 确保断开所有连接
        _redis_pool = None