from sqlalchemy.orm import DeclarativeBase

from sqlalchemy.orm import Mapped, mapped_column as Column
from sqlalchemy import Integer, String, TIMESTAMP, BIGINT, TEXT


class Base(DeclarativeBase):
    pass


class PengpaiNews(Base):
    """
    CREATE TABLE `pengpai_news` (
      `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'id',
      `title` varchar(255) DEFAULT NULL COMMENT 'title',
      `news_id` varchar(128) DEFAULT NULL COMMENT '新闻第',
      `content_msg` longtext COMMENT '内容',
      `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4
    """

    __tablename__ = "pengpai_news"
    id = Column(BIGINT, primary_key=True, index=True)
    title = Column(String(255), nullable=True)
    news_id = Column(String(128), nullable=True)
    content_msg = Column(TEXT)
    create_time = Column(TIMESTAMP, nullable=True)
