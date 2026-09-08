"""Event system for CanvasUI."""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class Event:
    """An event in the system."""
    name: str
    source: str = ""
    data: dict[str, Any] = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: f"evt_{uuid.uuid4().hex[:8]}")


class EventBus:
    """Central event bus for decoupled communication."""

    def __init__(self):
        self._subscribers: dict[str, list[Callable[[Event], None]]] = {}

    def subscribe(self, event_name: str, handler: Callable[[Event], None]) -> None:
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(handler)

    def unsubscribe(self, event_name: str, handler: Callable[[Event], None]) -> None:
        if event_name in self._subscribers:
            self._subscribers[event_name] = [h for h in self._subscribers[event_name] if h is not handler]

    def publish(self, event: Event) -> None:
        for handler in self._subscribers.get(event.name, []):
            handler(event)

    def clear(self) -> None:
        self._subscribers.clear()
