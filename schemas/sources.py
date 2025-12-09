from typing import List, Optional

from pydantic import BaseModel


class SourceCreate(BaseModel):
    name: str
    description: Optional[str] = None


class SourceOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True


class RoutingItem(BaseModel):
    operator_id: int
    weight: int


class SourceRoutingUpdate(BaseModel):
    routing: List[RoutingItem]
