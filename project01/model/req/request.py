from pydantic import BaseModel
from datetime import datetime

from pydantic import Field


class UserSmsCodeReq(BaseModel):
    id: str | None = Field(default="123456")
    mobile_no: int = Field(default="13800138000")
    sms_code: str = Field(default="345345")
    send_time: datetime = Field(default="2025-06-01 12:00:00")
    create_time: datetime | None = Field(default=None)
