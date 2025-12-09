from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.db import get_db
from models import Operator, Contact
from schemas.stats import OperatorStatsItem

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/operators", response_model=list[OperatorStatsItem])
def get_operator_stats(db: Session = Depends(get_db)):
    # Very simple load stats per operator
    items: list[OperatorStatsItem] = []

    for op in db.query(Operator).all():
        active_count = (
            db.query(Contact)
            .filter(Contact.operator_id == op.id, Contact.is_closed.is_(False))
            .count()
        )
        items.append(
            OperatorStatsItem(
                operator=op,
                active_contacts=active_count,
            )
        )

    return items
