"""Tests for CanvasUI Dashboard."""
from __future__ import annotations

import pytest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from components import CanvasDashboard, DashboardPanel, DashboardWidget


class TestDashboardWidget:
    def test_create_widget(self):
        widget = DashboardWidget(id="1", title="CPU", widget_type="chart")
        assert widget.title == "CPU"
        assert widget.widget_type == "chart"

    def test_widget_with_data(self):
        widget = DashboardWidget(id="1", title="CPU", widget_type="chart", data={"values": [1, 2, 3]})
        assert widget.data == {"values": [1, 2, 3]}


class TestDashboardPanel:
    def test_create_panel(self):
        panel = DashboardPanel(id="1", title="System")
        assert panel.title == "System"
        assert panel.widgets == []


class TestCanvasDashboard:
    def test_create_dashboard(self):
        dash = CanvasDashboard("Test")
        assert dash.name == "Test"

    def test_add_panel(self):
        dash = CanvasDashboard()
        panel = dash.add_panel("System")
        assert panel.title == "System"
        assert len(dash.list_panels()) == 1

    def test_add_widget(self):
        dash = CanvasDashboard()
        panel = dash.add_panel("System")
        widget = dash.add_widget(panel.id, "CPU", "chart")
        assert widget.title == "CPU"
        assert len(dash.list_widgets()) == 1

    def test_get_panel(self):
        dash = CanvasDashboard()
        panel = dash.add_panel("System")
        retrieved = dash.get_panel(panel.id)
        assert retrieved is not None
        assert retrieved.title == "System"

    def test_get_widget(self):
        dash = CanvasDashboard()
        panel = dash.add_panel("System")
        widget = dash.add_widget(panel.id, "CPU", "chart")
        retrieved = dash.get_widget(widget.id)
        assert retrieved is not None
        assert retrieved.title == "CPU"

    def test_remove_panel(self):
        dash = CanvasDashboard()
        panel = dash.add_panel("System")
        assert dash.remove_panel(panel.id) is True
        assert dash.get_panel(panel.id) is None

    def test_remove_widget(self):
        dash = CanvasDashboard()
        panel = dash.add_panel("System")
        widget = dash.add_widget(panel.id, "CPU", "chart")
        assert dash.remove_widget(widget.id) is True
        assert dash.get_widget(widget.id) is None

    def test_get_stats(self):
        dash = CanvasDashboard()
        panel = dash.add_panel("System")
        dash.add_widget(panel.id, "CPU", "chart")
        dash.add_widget(panel.id, "Memory", "gauge")
        stats = dash.get_stats()
        assert stats["panels"] == 1
        assert stats["widgets"] == 2
