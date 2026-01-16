from typing import Generic, List, TypeVar
from pydantic import BaseModel, ConfigDict


T = TypeVar("T")


class SendRequest(BaseModel):
    phone: str
    title: str
    message: str

    model_config = ConfigDict(from_attributes=True)


class Page(BaseModel, Generic[T]):
    items: List[T]
    page: int
    size: int
    total: int
    has_next: bool
    