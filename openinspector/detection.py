from __future__ import annotations

from typing import Dict, Any, Optional

from .signals import SignalBase, SignalSeverity


class DetectionEvent(Dict[str, Any]):
    """Simple dict-based detection event."""


class DetectionEngine:
    """Very small rule-based engine for demonstration purposes."""

    def process(self, signal: SignalBase) -> Optional[DetectionEvent]:
        # Example heuristic rules
        if signal.severity in {SignalSeverity.high, SignalSeverity.critical}:
            return self._make_event(signal, risk_score=0.9)

        if signal.type.value == "authentication" and signal.metadata.get("failed_attempts", 0) >= 5:
            return self._make_event(signal, risk_score=0.7)

        # No detection
        return None

    @staticmethod
    def _make_event(signal: SignalBase, risk_score: float) -> DetectionEvent:
        return {
            "signal_id": signal.id,
            "risk_score": risk_score,
            "risk_level": _score_to_level(risk_score),
            "description": "Rule-based detection",
        }


def _score_to_level(score: float) -> str:
    if score < 0.2:
        return "safe"
    if score < 0.4:
        return "low"
    if score < 0.6:
        return "medium"
    if score < 0.8:
        return "high"
    return "critical" 