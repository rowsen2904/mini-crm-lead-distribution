from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.db import get_db
from models import Lead
from schemas.contacts import ContactCreate, ContactOut, ContactOperatorShort
from schemas.leads import LeadOut
from services.contacts import create_contact_with_distribution

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("", response_model=ContactOut)
def create_contact(contact_in: ContactCreate, db: Session = Depends(get_db)):
    try:
        contact = create_contact_with_distribution(
            db=db,
            lead_key=contact_in.lead_key,
            source_id=contact_in.source_id,
            payload=contact_in.payload,
        )
    except ValueError:
        raise HTTPException(status_code=404, detail="Source not found")

    operator = contact.operator
    operator_short = (
        ContactOperatorShort.from_orm(
            operator) if operator is not None else None
    )

    return ContactOut(
        id=contact.id,
        lead_id=contact.lead_id,
        source_id=contact.source_id,
        operator=operator_short,
        payload=contact.payload,
        created_at=contact.created_at,
        is_closed=contact.is_closed,
    )


@router.get("/leads", response_model=list[LeadOut])
def list_leads(db: Session = Depends(get_db)):
    # Just a simple leads listing
    leads = db.query(Lead).all()
    return leads
