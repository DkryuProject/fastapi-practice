from pydantic import BaseModel, ConfigDict


class SMSSendRequest(BaseModel):
    phone: str
    title: str
    message: str

    model_config = ConfigDict(from_attributes=True)


class KakaoSendRequest(BaseModel):
    tpl_code: str
    sender: str
    emtitle_1: str
    subject: str
    receiver_1: str
    message_1: str
    button_1: str

    model_config = ConfigDict(from_attributes=True)
