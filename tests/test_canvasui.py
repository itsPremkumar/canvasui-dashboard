"""Tests for CanvasUI — Dashboard Component System."""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from canvasui.canvas import Canvas, Component, Panel, Widget
from canvasui.events import EventBus, Event
from canvasui.layout import GridLayout, FlexLayout
from canvasui.theme import Theme, DarkTheme, LightTheme


class TestComponent:
    def test_create(self):
        c = Component("test")
        assert c.name == "test"
        assert c.visible is True
        assert c.id.startswith("comp_")

    def test_add_child(self):
        parent = Component("parent")
        child = Component("child")
        parent.add_child(child)
        assert len(parent.children) == 1
        assert child.parent is parent

    def test_remove_child(self):
        parent = Component("parent")
        child = Component("child")
        parent.add_child(child)
        parent.remove_child(child)
        assert len(parent.children) == 0

    def test_find(self):
        root = Component("root")
        child = Component("target")
        root.add_child(child)
        found = root.find("target")
        assert found is child

    def test_find_nested(self):
        root = Component("root")
        mid = Component("mid")
        leaf = Component("deep")
        root.add_child(mid)
        mid.add_child(leaf)
        found = root.find("deep")
        assert found is leaf

    def test_find_not_found(self):
        root = Component("root")
        assert root.find("missing") is None

    def test_on_trigger(self):
        c = Component("test")
        results = []
        c.on("click", lambda comp, **kw: results.append(comp.name))
        c.trigger("click")
        assert results == ["test"]

    def test_trigger_bubbles(self):
        parent = Component("parent")
        child = Component("child")
        parent.add_child(child)
        results = []
        child.on("click", lambda comp, **kw: results.append(comp.name))
        parent.on("click", lambda comp, **kw: results.append(comp.name))
        child.trigger("click")
        assert "child" in results
        assert "parent" in results

    def test_to_dict(self):
        c = Component("test")
        d = c.to_dict()
        assert d["name"] == "test"
        assert "id" in d


class TestPanel:
    def test_create(self):
        p = Panel("p1", x=10, y=20, width=100, height=200)
        assert p.x == 10
        assert p.y == 20
        assert p.width == 100
        assert p.height == 200

    def test_resize(self):
        p = Panel("p1", width=100, height=100)
        p.resize(200, 300)
        assert p.width == 200
        assert p.height == 300

    def test_resize_triggers_event(self):
        p = Panel("p1")
        results = []
        p.on("resize", lambda comp, **kw: results.append("resized"))
        p.resize(50, 50)
        assert len(results) == 1

    def test_to_dict(self):
        p = Panel("p1", x=5, y=5)
        d = p.to_dict()
        assert d["x"] == 5
        assert d["y"] == 5


class TestWidget:
    def test_create(self):
        w = Widget("w1", widget_type="gauge")
        assert w.widget_type == "gauge"


class TestCanvas:
    def test_create(self):
        c = Canvas("main")
        assert c.name == "main"

    def test_add(self):
        c = Canvas()
        comp = Component("test")
        c.add(comp)
        assert len(c.children) == 1

    def test_add_panel(self):
        c = Canvas()
        panel = c.add_panel("Status", x=0, y=0, width=800, height=600)
        assert isinstance(panel, Panel)
        assert panel.width == 800

    def test_add_widget(self):
        c = Canvas()
        w = c.add_widget("Meter", widget_type="gauge")
        assert isinstance(w, Widget)

    def test_add_widget_to_panel(self):
        c = Canvas()
        c.add_panel("Status")
        w = c.add_widget("Meter", parent="Status")
        assert w.parent is not None

    def test_find(self):
        c = Canvas()
        c.add_panel("Grid")
        found = c.find("Grid")
        assert found is not None
        assert found.name == "Grid"

    def test_select(self):
        c = Canvas()
        c.add_panel("Target")
        assert c.select("Target") is True
        assert len(c.selection) == 1

    def test_select_not_found(self):
        c = Canvas()
        assert c.select("missing") is False

    def test_handle_click(self):
        c = Canvas()
        c.add_panel("ClickTarget")
        results = []
        panel = c.find("ClickTarget")
        panel.on("click", lambda comp, **kw: results.append(comp.name))
        assert c.handle_click("ClickTarget") is True
        assert len(results) == 1

    def test_to_dict(self):
        c = Canvas("test")
        c.add_panel("p1")
        d = c.to_dict()
        assert d["name"] == "test"
        assert len(d["components"]) == 1


class TestEventBus:
    def test_create(self):
        bus = EventBus()
        assert bus._subscribers == {}

    def test_subscribe_publish(self):
        bus = EventBus()
        results = []
        bus.subscribe("click", lambda e: results.append(e.name))
        bus.publish(Event(name="click"))
        assert len(results) == 1

    def test_unsubscribe(self):
        bus = EventBus()
        handler = lambda e: None
        bus.subscribe("click", handler)
        bus.unsubscribe("click", handler)
        bus.publish(Event(name="click"))  # Should not raise

    def test_multiple_subscribers(self):
        bus = EventBus()
        count = [0]
        bus.subscribe("evt", lambda e: count.__setitem__(0, count[0] + 1))
        bus.subscribe("evt", lambda e: count.__setitem__(0, count[0] + 1))
        bus.publish(Event(name="evt"))
        assert count[0] == 2

    def test_clear(self):
        bus = EventBus()
        bus.subscribe("evt", lambda e: None)
        bus.clear()
        assert bus._subscribers == {}


class TestEvent:
    def test_create(self):
        e = Event(name="click", source="btn")
        assert e.name == "click"
        assert e.source == "btn"
        assert e.event_id.startswith("evt_")


class TestGridLayout:
    def test_create(self):
        gl = GridLayout(columns=12, rows=8)
        assert gl.columns == 12
        assert gl.rows == 8

    def test_place(self):
        gl = GridLayout()
        p = Panel("p1")
        gl.place(p, col=0, row=0)
        assert gl.get_at(0, 0) is p

    def test_get_at_empty(self):
        gl = GridLayout()
        assert gl.get_at(5, 5) is None

    def test_remove(self):
        gl = GridLayout()
        p = Panel("p1")
        gl.place(p, col=0, row=0)
        gl.remove(0, 0)
        assert gl.get_at(0, 0) is None

    def test_get_all(self):
        gl = GridLayout()
        gl.place(Panel("p1"), col=0, row=0)
        gl.place(Panel("p2"), col=1, row=0)
        assert len(gl.get_all()) == 2


class TestFlexLayout:
    def test_create(self):
        fl = FlexLayout(direction="row")
        assert fl.direction == "row"

    def test_add(self):
        fl = FlexLayout()
        fl.add(Panel("p1", width=100))
        assert len(fl.get_items()) == 1

    def test_remove(self):
        fl = FlexLayout()
        p = Panel("p1")
        fl.add(p)
        fl.remove(p)
        assert len(fl.get_items()) == 0


class TestTheme:
    def test_create(self):
        t = Theme(name="custom")
        assert t.name == "custom"
        assert t.background == "#ffffff"

    def test_get(self):
        t = Theme()
        assert t.get("accent") == "#3b82f6"

    def test_set(self):
        t = Theme()
        t.set("custom_key", "#abc")
        assert t.get("custom_key") == "#abc"

    def test_to_dict(self):
        t = Theme()
        d = t.to_dict()
        assert "name" in d
        assert "background" in d


class TestDarkTheme:
    def test_create(self):
        t = DarkTheme()
        assert t.name == "dark"
        assert t.background == "#1a1a2e"
        assert t.accent == "#6366f1"


class TestLightTheme:
    def test_create(self):
        t = LightTheme()
        assert t.name == "light"
        assert t.background == "#ffffff"
        assert t.accent == "#3b82f6"
