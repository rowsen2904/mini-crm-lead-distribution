from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.db import get_db
from models import Operator, OperatorSourceWeight, Source
from schemas.sources import (
    SourceCreate,
    SourceOut,
    SourceRoutingUpdate,
)

router = APIRouter(prefix="/sources", tags=["sources"])


@router.post("", response_model=SourceOut)
def create_source(source_in: SourceCreate, db: Session = Depends(get_db)):
    source = Source(name=source_in.name, description=source_in.description)
    db.add(source)
    db.commit()
    db.refresh(source)
    return source


@router.get("", response_model=list[SourceOut])
def list_sources(db: Session = Depends(get_db)):
    return db.query(Source).all()


@router.put("/{source_id}/routing", response_model=SourceOut)
def set_source_routing(
    source_id: int, routing_in: SourceRoutingUpdate, db: Session = Depends(get_db)
):
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    # Clear existing routing
    db.query(OperatorSourceWeight).filter(
        OperatorSourceWeight.source_id == source_id
    ).delete()

    # Create new routing
    for item in routing_in.routing:
        operator = db.query(Operator).filter(
            Operator.id == item.operator_id).first()
        if not operator:
            raise HTTPException(
                status_code=400,
                detail=f"Operator {item.operator_id} does not exist",
            )
        if item.weight <= 0:
            raise HTTPException(
                status_code=400,
                detail="Weight should be positive",
            )

        db.add(
            OperatorSourceWeight(
                source_id=source_id,
                operator_id=item.operator_id,
                weight=item.weight,
            )
        )

    db.commit()
    db.refresh(source)
    return source
