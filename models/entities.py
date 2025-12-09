from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from core.db import Base


class Operator(Base):
    __tablename__ = "operators"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    max_active_contacts = Column(Integer, default=20)

    contacts = relationship("Contact", back_populates="operator")
    weights = relationship("OperatorSourceWeight", back_populates="operator")


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    description = Column(String, nullable=True)

    weights = relationship("OperatorSourceWeight", back_populates="source")
    contacts = relationship("Contact", back_populates="source")


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    external_key = Column(String, nullable=False, unique=True, index=True)
    name = Column(String, nullable=True)

    contacts = relationship("Contact", back_populates="lead")


class OperatorSourceWeight(Base):
    __tablename__ = "operator_source_weights"

    id = Column(Integer, primary_key=True, index=True)
    operator_id = Column(Integer, ForeignKey("operators.id"), nullable=False)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)
    weight = Column(Integer, nullable=False)

    operator = relationship("Operator", back_populates="weights")
    source = relationship("Source", back_populates="weights")


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)
    operator_id = Column(Integer, ForeignKey("operators.id"), nullable=True)

    payload = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_closed = Column(Boolean, default=False)

    lead = relationship("Lead", back_populates="contacts")
    source = relationship("Source", back_populates="contacts")
    operator = relationship("Operator", back_populates="contacts")
