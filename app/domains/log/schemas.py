from pydantic import BaseModel
from datetime import datetime

class UserActionLogBase(BaseModel):
    action: str

class UserActionLogResponse(UserActionLogBase):
    id: int
    user_id: int | None
    endpoint: str
    method: str
    client_ip: str | None
    user_agent: str | None
    created_at: datetime

    class Config:
        orm_mode = True
