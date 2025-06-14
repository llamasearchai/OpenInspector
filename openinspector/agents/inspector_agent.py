from __future__ import annotations

import json
from typing import Any, Dict, Callable, List

import openai
from langchain.chat_models.openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, BaseMessage
from langchain.tools import tool

from ..config import settings
from ..detection import DetectionEngine
from ..defense import DefenseSystem
from ..signals import SignalBase

openai.api_key = settings.openai_api_key

_engine = DetectionEngine()
_defense = DefenseSystem()


@tool
def detect_abuse(signal_json: str) -> str:
    """Run the detection engine on a JSON-encoded signal and return any detection event."""
    signal_dict = json.loads(signal_json)
    signal = SignalBase.parse_obj(signal_dict)
    detection = _engine.process(signal)
    return json.dumps(detection or {})


@tool
def handle_defense(detection_json: str) -> str:
    """Given a detection event, return interventions according to policy."""
    detection_event = json.loads(detection_json)
    interventions = _defense.handle(detection_event or {})
    return json.dumps(interventions)


def build_inspector_agent(model_name: str | None = None) -> ChatOpenAI:
    llm = ChatOpenAI(model_name or settings.openai_model, temperature=0.0)
    return llm.bind_tools([detect_abuse, handle_defense])


class InspectorAgent:
    """High-level wrapper around the bound LLM for convenient usage."""

    def __init__(self, llm: ChatOpenAI | None = None):
        self.llm = llm or build_inspector_agent()

    def analyse_signal(self, signal: SignalBase) -> Dict[str, Any]:
        # Compose function call instructions
        prompt: List[BaseMessage] = [
            SystemMessage(content="You are OpenInspector. You detect and mitigate account abuse."),
            HumanMessage(content=f"Analyse the following signal and respond with your function calls. Signal: {signal.json()}")
        ]
        response = self.llm(prompt)
        return response.additional_kwargs  # contains function call tool invocations 