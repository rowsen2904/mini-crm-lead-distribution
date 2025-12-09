from typing import Optional

from pydantic import BaseModel


class LeadOut(BaseModel):
    id: int
    external_key: str
    name: Optional[str] = None

    class Config:
        orm_mode = True
