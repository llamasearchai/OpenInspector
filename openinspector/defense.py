from __future__ import annotations

from typing import Dict, Any, List


class Intervention(Dict[str, Any]):
    pass


class DefenseSystem:
    """Very small defense engine mapping risk levels to interventions."""

    _POLICY = {
        "critical": ("terminate",),
        "high": ("suspend",),
        "medium": ("challenge",),
        "low": ("monitor",),
    }

    def handle(self, detection_event: Dict[str, Any]) -> List[Intervention]:
        risk_level: str = detection_event.get("risk_level", "low")
        actions = self._POLICY.get(risk_level, ("monitor",))
        interventions: List[Intervention] = []
        for action in actions:
            interventions.append({
                "action": action,
                "detection_signal_id": detection_event.get("signal_id"),
            })
        return interventions 