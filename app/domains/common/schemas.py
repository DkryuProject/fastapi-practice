from pydantic import BaseModel, ConfigDict


class SendRequest(BaseModel):
    phone: str
    title: str
    message: str

    model_config = ConfigDict(from_attributes=True)
