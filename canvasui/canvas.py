"""Canvas core — Component hierarchy for dashboard UIs."""
from __future__ import annotations

import uuid
from typing import Any, Callable


class Component:
    """Base component."""

    def __init__(self, name: str = "", **kwargs):
        self.id = f"comp_{uuid.uuid4().hex[:8]}"
        self.name = name
        self.visible: bool = True
        self.children: list["Component"] = []
        self.parent: "Component | None" = None
        self._handlers: dict[str, list[Callable]] = {}
        self.metadata: dict[str, Any] = kwargs

    def add_child(self, child: "Component") -> "Component":
        child.parent = self
        self.children.append(child)
        return child

    def remove_child(self, child: "Component") -> None:
        self.children = [c for c in self.children if c is not child]

    def find(self, name: str) -> "Component | None":
        if self.name == name:
            return self
        for child in self.children:
            found = child.find(name)
            if found:
                return found
        return None

    def on(self, event: str, handler: Callable) -> None:
        if event not in self._handlers:
            self._handlers[event] = []
        self._handlers[event].append(handler)

    def trigger(self, event: str, **kwargs) -> None:
        for handler in self._handlers.get(event, []):
            handler(self, **kwargs)
        if self.parent:
            self.parent.trigger(event, **kwargs)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "visible": self.visible,
            "children": [c.to_dict() for c in self.children],
        }


class Panel(Component):
    """A rectangular panel on the canvas."""

    def __init__(self, name: str = "", x: int = 0, y: int = 0, width: int = 100, height: int = 100, **kwargs):
        super().__init__(name, **kwargs)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def resize(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.trigger("resize")

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d.update(x=self.x, y=self.y, width=self.width, height=self.height)
        return d


class Widget(Component):
    """A leaf widget."""

    def __init__(self, name: str = "", widget_type: str = "generic", **kwargs):
        super().__init__(name, **kwargs)
        self.widget_type = widget_type


class Canvas:
    """Top-level canvas holding all components."""

    def __init__(self, name: str = "main"):
        self.name = name
        self.children: list[Component] = []
        self._selection: list[Component] = []

    def add(self, component: Component) -> Component:
        self.children.append(component)
        return component

    def add_panel(self, name: str, x: int = 0, y: int = 0, width: int = 800, height: int = 600) -> Panel:
        panel = Panel(name=name, x=x, y=y, width=width, height=height)
        return self.add(panel)

    def add_widget(self, name: str, widget_type: str = "generic", parent: str | None = None) -> Widget:
        widget = Widget(name=name, widget_type=widget_type)
        if parent:
            p = self.find(parent)
            if isinstance(p, Panel):
                p.add_child(widget)
                return widget
        return self.add(widget)

    def find(self, name: str) -> Component | None:
        for c in self.children:
            found = c.find(name)
            if found:
                return found
        return None

    def select(self, name: str) -> bool:
        comp = self.find(name)
        if comp:
            self._selection = [comp]
            return True
        return False

    @property
    def selection(self) -> list[Component]:
        return self._selection

    def handle_click(self, name: str) -> bool:
        comp = self.find(name)
        if comp:
            comp.trigger("click")
            return True
        return False

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "components": [c.to_dict() for c in self.children]}
