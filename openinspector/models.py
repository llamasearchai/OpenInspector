from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict

from sqlalchemy import Column, String, DateTime, Float, JSON, Enum as SAEnum, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base
from .signals import SignalType, SignalSeverity


class SignalORM(Base):
    __tablename__ = "signals"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    type = Column(SAEnum(SignalType), nullable=False)
    severity = Column(SAEnum(SignalSeverity), default=SignalSeverity.info)
    user_id = Column(String, index=True)
    session_id = Column(String, index=True)
    ip_address = Column(String, index=True)
    metadata = Column(JSON, default=dict)

    detections = relationship("DetectionORM", back_populates="signal")


class DetectionORM(Base):
    __tablename__ = "detections"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    signal_id = Column(String, ForeignKey("signals.id"), nullable=False)
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    signal = relationship("SignalORM", back_populates="detections")
    interventions = relationship("InterventionORM", back_populates="detection")


class InterventionORM(Base):
    __tablename__ = "interventions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    detection_id = Column(String, ForeignKey("detections.id"), nullable=False)
    action = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    details = Column(JSON, default=dict)

    detection = relationship("DetectionORM", back_populates="interventions") 