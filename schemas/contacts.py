from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ContactCreate(BaseModel):
    lead_key: str
    source_id: int
    payload: Optional[str] = None


class ContactOperatorShort(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class ContactOut(BaseModel):
    id: int
    lead_id: int
    source_id: int
    operator: Optional[ContactOperatorShort]
    payload: Optional[str]
    created_at: datetime
    is_closed: bool

    class Config:
        orm_mode = True
