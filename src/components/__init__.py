"""CanvasUI Dashboard — Interactive dashboard framework."""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any


@dataclass
class DashboardWidget:
    """A dashboard widget."""
    id: str
    title: str
    widget_type: str
    data: dict[str, Any] = field(default_factory=dict)
    layout: dict[str, int] = field(default_factory=lambda: {"x": 0, "y": 0, "w": 4, "h": 4})


@dataclass
class DashboardPanel:
    """A dashboard panel."""
    id: str
    title: str
    widgets: list[DashboardWidget] = field(default_factory=list)


class CanvasDashboard:
    """Interactive dashboard framework."""

    def __init__(self, name: str = "Dashboard") -> None:
        self.name = name
        self.panels: dict[str, DashboardPanel] = {}
        self.widgets: dict[str, DashboardWidget] = {}

    def add_panel(self, title: str) -> DashboardPanel:
        panel = DashboardPanel(id=str(uuid.uuid4()), title=title)
        self.panels[panel.id] = panel
        return panel

    def add_widget(
        self,
        panel_id: str,
        title: str,
        widget_type: str,
        data: dict[str, Any] | None = None,
        layout: dict[str, int] | None = None,
    ) -> DashboardWidget:
        widget = DashboardWidget(
            id=str(uuid.uuid4()),
            title=title,
            widget_type=widget_type,
            data=data or {},
            layout=layout or {"x": 0, "y": 0, "w": 4, "h": 4},
        )
        self.widgets[widget.id] = widget
        panel = self.panels.get(panel_id)
        if panel:
            panel.widgets.append(widget)
        return widget

    def get_panel(self, id: str) -> DashboardPanel | None:
        return self.panels.get(id)

    def get_widget(self, id: str) -> DashboardWidget | None:
        return self.widgets.get(id)

    def remove_panel(self, id: str) -> bool:
        if id in self.panels:
            del self.panels[id]
            return True
        return False

    def remove_widget(self, id: str) -> bool:
        if id in self.widgets:
            del self.widgets[id]
            return True
        return False

    def list_panels(self) -> list[DashboardPanel]:
        return list(self.panels.values())

    def list_widgets(self) -> list[DashboardWidget]:
        return list(self.widgets.values())

    def get_stats(self) -> dict[str, int]:
        return {
            "panels": len(self.panels),
            "widgets": len(self.widgets),
        }
