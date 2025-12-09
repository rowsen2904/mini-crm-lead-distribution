import random
from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from models import Contact, Lead, Operator, OperatorSourceWeight, Source


def get_or_create_lead(db: Session, lead_key: str) -> Lead:
    # Reuse lead by external_key or create a new one
    lead = db.query(Lead).filter(Lead.external_key == lead_key).first()
    if lead:
        return lead

    lead = Lead(external_key=lead_key)
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


def get_source_or_404(db: Session, source_id: int) -> Source:
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        # Route layer will map this to HTTPException
        raise ValueError("Source not found")
    return source


def get_operator_load(db: Session, operator_id: int) -> int:
    # Count open contacts for given operator
    return (
        db.query(Contact)
        .filter(
            Contact.operator_id == operator_id,
            Contact.is_closed.is_(False),
        )
        .count()
    )


def get_available_operators_for_source(
    db: Session, source_id: int
) -> List[Tuple[Operator, int]]:
    """
    Returns list of (operator, weight) that are:
    - active
    - below their load limit
    for given source.
    """
    rows = (
        db.query(OperatorSourceWeight, Operator)
        .join(Operator, OperatorSourceWeight.operator_id == Operator.id)
        .filter(
            OperatorSourceWeight.source_id == source_id,
            Operator.is_active.is_(True),
        )
        .all()
    )

    candidates: List[Tuple[Operator, int]] = []
    for weight_row, operator in rows:
        current_load = get_operator_load(db, operator.id)
        if current_load < operator.max_active_contacts:
            candidates.append((operator, weight_row.weight))

    return candidates


def choose_operator_weighted(
    candidates: List[Tuple[Operator, int]]
) -> Optional[Operator]:
    # Simple weighted random choice
    if not candidates:
        return None

    total_weight = sum(weight for _, weight in candidates)
    if total_weight <= 0:
        return None

    r = random.uniform(0, total_weight)
    upto = 0.0
    for operator, weight in candidates:
        upto += weight
        if r <= upto:
            return operator

    return candidates[-1][0]


def create_contact_with_distribution(
    db: Session, lead_key: str, source_id: int, payload: Optional[str] = None
) -> Contact:
    """
    Main entry point for contact creation with distribution logic.
    """
    lead = get_or_create_lead(db, lead_key)
    _ = get_source_or_404(db, source_id)

    candidates = get_available_operators_for_source(db, source_id)
    operator = choose_operator_weighted(candidates)

    contact = Contact(
        lead_id=lead.id,
        source_id=source_id,
        operator_id=operator.id if operator else None,
        payload=payload,
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact
