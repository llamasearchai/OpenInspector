from __future__ import annotations

from fastapi import APIRouter, HTTPException, Depends, Response
from pydantic import BaseModel
from typing import Any, Dict, List
import uuid

from ..signals import SignalBase
from ..detection import DetectionEngine
from ..defense import DefenseSystem
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..models import SignalORM, DetectionORM, InterventionORM
from prometheus_client import Counter, generate_latest, REGISTRY

router = APIRouter()
_engine = DetectionEngine()
_defense = DefenseSystem()

_signals_ingested = Counter("oi_signals_ingested", "Signals ingested")


class SignalPayload(BaseModel):
    type: str
    severity: str | None = None
    user_id: str | None = None
    session_id: str | None = None
    ip_address: str | None = None
    metadata: Dict[str, Any] | None = None
    # Additional dynamic fields captured in metadata

    def to_signal(self) -> SignalBase:
        data = self.dict(exclude_unset=True)
        data.setdefault("metadata", {})
        return SignalBase.parse_obj(data)


@router.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


@router.post("/signals")
async def ingest_signal(payload: SignalPayload, session: AsyncSession = Depends(get_session)):
    try:
        signal = payload.to_signal()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(422, f"Invalid signal: {exc}")

    _signals_ingested.inc()
    detection = _engine.process(signal)
    interventions = _defense.handle(detection) if detection else []

    # persist
    db_signal = SignalORM(
        id=signal.id,
        timestamp=signal.timestamp,
        type=signal.type,
        severity=signal.severity,
        user_id=signal.user_id,
        session_id=signal.session_id,
        ip_address=signal.ip_address,
        metadata=signal.metadata,
    )
    session.add(db_signal)

    db_detection = None
    if detection:
        db_detection = DetectionORM(
            id=str(uuid.uuid4()),
            signal_id=signal.id,
            risk_score=detection["risk_score"],
            risk_level=detection["risk_level"],
            description=detection.get("description"),
        )
        session.add(db_detection)

    for intv in interventions:
        session.add(
            InterventionORM(
                id=str(uuid.uuid4()),
                detection_id=db_detection.id if db_detection else "",  # may be empty
                action=intv["action"],
                details=intv,
            )
        )

    await session.commit()

    return {
        "signal_id": signal.id,
        "detection": detection,
        "interventions": interventions,
    }


# Retrieval endpoints


@router.get("/signals", response_model=List[Dict[str, Any]])
async def list_signals(limit: int = 50, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        SignalORM.__table__.select().order_by(SignalORM.timestamp.desc()).limit(limit)
    )
    rows = [dict(r) for r in result.mappings()]
    return rows


@router.get("/detections", response_model=List[Dict[str, Any]])
async def list_detections(limit: int = 50, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        DetectionORM.__table__.select().order_by(DetectionORM.created_at.desc()).limit(limit)
    )
    rows = [dict(r) for r in result.mappings()]
    return rows


@router.get("/interventions", response_model=List[Dict[str, Any]])
async def list_interventions(limit: int = 50, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        InterventionORM.__table__.select().order_by(InterventionORM.created_at.desc()).limit(limit)
    )
    rows = [dict(r) for r in result.mappings()]
    return rows


@router.get("/metrics", include_in_schema=False)
async def metrics() -> Any:
    content = generate_latest(REGISTRY)
    return Response(content=content, media_type="text/plain; version=0.0.4") 