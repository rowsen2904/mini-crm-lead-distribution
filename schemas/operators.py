from typing import Optional

from pydantic import BaseModel


class OperatorBase(BaseModel):
    name: str
    max_active_contacts: int = 20


class OperatorCreate(OperatorBase):
    pass


class OperatorUpdate(BaseModel):
    is_active: Optional[bool] = None
    max_active_contacts: Optional[int] = None


class OperatorOut(BaseModel):
    id: int
    name: str
    is_active: bool
    max_active_contacts: int

    class Config:
        orm_mode = True
