from sqlalchemy.orm import DeclarativeBase

from sqlalchemy.orm import Mapped, mapped_column as Column
from sqlalchemy import Integer, String, TIMESTAMP, BIGINT, TEXT


class Base(DeclarativeBase):
    pass


class WeixinReader(Base):
    """
    CREATE TABLE `pengpai_datas` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `msg_json` longtext COLLATE utf8mb4_general_ci COMMENT 'json字符串消息',
    `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
    """

    __tablename__ = "pengpai_datas"
    id = Column(BIGINT, primary_key=True, index=True)
    msg_json = Column(String(2048), nullable=True)
    create_time = Column(TIMESTAMP, nullable=True)
