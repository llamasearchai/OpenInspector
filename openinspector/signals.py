from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, validator


class SignalType(str, Enum):
    user_behavior = "user_behavior"
    authentication = "authentication"
    transaction = "transaction"
    content = "content"
    network = "network"


class SignalSeverity(str, Enum):
    info = "info"
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class SignalBase(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    type: SignalType
    severity: SignalSeverity = SignalSeverity.info
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    ip_address: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        validate_assignment = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class AuthenticationSignal(SignalBase):
    type: SignalType = SignalType.authentication
    success: bool
    auth_type: str = "password"


class TransactionSignal(SignalBase):
    type: SignalType = SignalType.transaction
    amount: float
    currency: str = "USD" 