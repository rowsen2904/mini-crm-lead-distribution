from pydantic import BaseModel

from schemas.operators import OperatorOut


class OperatorStatsItem(BaseModel):
    operator: OperatorOut
    active_contacts: int
