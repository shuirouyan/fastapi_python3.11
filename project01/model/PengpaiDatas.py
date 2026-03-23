from sqlalchemy.orm import DeclarativeBase

from sqlalchemy.orm import Mapped, mapped_column as Column
from sqlalchemy import Integer, String, DateTime, BIGINT, TEXT


class Base(DeclarativeBase):
    pass


class PengpaiDatas(Base):
    """
     CREATE TABLE `pengpai_datas` (
      `id` bigint NOT NULL AUTO_INCREMENT,
      `msg_json` longtext COMMENT 'json字符串消息',
      `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
    """

    __tablename__ = "pengpai_datas"
    id = Column(BIGINT, primary_key=True, index=True)
    msg_json = Column(TEXT)
    create_time = Column(DateTime, nullable=True)
