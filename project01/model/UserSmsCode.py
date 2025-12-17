
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy.orm import Mapped, mapped_column as Column
from sqlalchemy import Integer, String, DateTime

class Base(DeclarativeBase):
    pass

class UserSmsCode(Base):
    __tablename__ = "user_sms_code"
    id:Mapped[int] = Column(primary_key=True, index=True)
    mobile_no = Column(Integer, nullable=True)
    sms_code = Column(String(6), nullable=True)
    send_time = Column(DateTime, nullable=False, default=DateTime)
    create_time = Column(DateTime, nullable=False, default=DateTime, onupdate=DateTime)
    
    # 新增：转字典方法
    def to_dict(self):
        return {
            "id": self.id,
            "mobile_no": self.mobile_no,
            "sms_code": self.sms_code,
            # 时间类型格式化（关键，否则 JSON 序列化失败）
            "send_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S") if self.create_time else None,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S") if self.create_time else None
        }