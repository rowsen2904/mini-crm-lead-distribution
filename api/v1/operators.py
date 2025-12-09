from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.db import get_db
from models import Operator, Contact
from schemas.operators import OperatorCreate, OperatorOut, OperatorUpdate
from schemas.stats import OperatorStatsItem

router = APIRouter(prefix="/operators", tags=["operators"])


@router.post("", response_model=OperatorOut)
def create_operator(operator_in: OperatorCreate, db: Session = Depends(get_db)):
    operator = Operator(
        name=operator_in.name,
        max_active_contacts=operator_in.max_active_contacts,
        is_active=True,
    )
    db.add(operator)
    db.commit()
    db.refresh(operator)
    return operator


@router.get("", response_model=list[OperatorOut])
def list_operators(db: Session = Depends(get_db)):
    return db.query(Operator).all()


@router.patch("/{operator_id}", response_model=OperatorOut)
def update_operator(
    operator_id: int, operator_in: OperatorUpdate, db: Session = Depends(get_db)
):
    operator = db.query(Operator).filter(Operator.id == operator_id).first()
    if not operator:
        raise HTTPException(status_code=404, detail="Operator not found")

    if operator_in.is_active is not None:
        operator.is_active = operator_in.is_active
    if operator_in.max_active_contacts is not None:
        operator.max_active_contacts = operator_in.max_active_contacts

    db.commit()
    db.refresh(operator)
    return operator


@router.get("/stats", response_model=list[OperatorStatsItem])
def operator_stats(db: Session = Depends(get_db)):
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
