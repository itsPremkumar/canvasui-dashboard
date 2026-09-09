"""Smoke tests for CanvasUI — tests for new modules (design_tokens, components, docs_site)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from canvasui.canvas import Canvas, Component, Panel, Widget
from canvasui.events import EventBus, Event
from canvasui.layout import GridLayout, FlexLayout
from canvasui.theme import Theme, DarkTheme, LightTheme

from src.canvasui.design_tokens import (
    DesignTokenSystem,
    ColorPalette,
    TypographyTokens,
    SpacingTokens,
    ShadowTokens,
    RadiusTokens,
    BreakpointTokens,
    ZIndexTokens,
    MotionTokens,
    create_light_tokens,
    create_dark_tokens,
)

from src.canvasui.components import (
    Button,
    IconButton,
    TextInput,
    NumberInput,
    Select,
    Checkbox,
    Toggle,
    Table,
    Column,
    BarChart,
    LineChart,
    PieChart,
    Gauge,
    Card,
    StatCard,
    Form,
)

from src.canvasui.docs_site import DocsSiteGenerator, generate_docs


# ── Design Token Tests ──────────────────────────────────────────────────

class TestColorPalette:
    def test_shade(self):
        p = ColorPalette(_shades={50: "#fff", 500: "#aaa"})
        assert p.shade(50) == "#fff"
        assert p.shade(500) == "#aaa"

    def test_getitem(self):
        p = ColorPalette(_shades={100: "#abc"})
        assert p[100] == "#abc"

    def test_shade_not_found(self):
        p = ColorPalette(_shades={50: "#fff"})
        with pytest.raises(KeyError):
            p.shade(999)

    def test_lightest_darkest(self):
        p = ColorPalette(_shades={50: "#fff", 900: "#000", 500: "#aaa"})
        assert p.lightest == "#fff"
        assert p.darkest == "#000"


class TestDesignTokenSystem:
    def test_create_light(self):
        tokens = create_light_tokens()
        assert tokens.theme.name == "light"
        assert tokens.theme.background == "#ffffff"

    def test_create_dark(self):
        tokens = create_dark_tokens()
        assert tokens.theme.name == "dark"
        assert tokens.theme.background == "#1a1a2e"

    def test_resolve_color_hex(self):
        tokens = create_light_tokens()
        assert tokens.resolve_color("#ff0000") == "#ff0000"

    def test_resolve_color_palette(self):
        tokens = create_light_tokens()
        assert tokens.resolve_color("blue.500") == "#3b82f6"
        assert tokens.resolve_color("gray.900") == "#111827"

    def test_resolve_color_theme(self):
        tokens = create_light_tokens()
        assert tokens.resolve_color("accent") == "#3b82f6"
        assert tokens.resolve_color("background") == "#ffffff"

    def test_resolve_spacing(self):
        tokens = create_light_tokens()
        assert tokens.resolve_spacing("space_4") == "1rem"
        assert tokens.resolve_spacing("space_0") == "0"

    def test_resolve_shadow(self):
        tokens = create_light_tokens()
        assert tokens.resolve_shadow("shadow_md") != ""
        assert tokens.resolve_shadow("shadow_none") == "none"

    def test_resolve_radius(self):
        tokens = create_light_tokens()
        assert tokens.resolve_radius("radius_lg") == "0.5rem"
        assert tokens.resolve_radius("radius_full") == "9999px"

    def test_to_dict(self):
        tokens = create_light_tokens()
        d = tokens.to_dict()
        assert "colors" in d
        assert "typography" in d
        assert "spacing" in d
        assert "theme" in d
        assert "gray" in d["colors"]
        assert "blue" in d["colors"]


# ── Component Tests ─────────────────────────────────────────────────────

class TestButton:
    def test_create(self):
        b = Button("btn", label="Click", variant="primary")
        assert b.label == "Click"
        assert b.variant == "primary"
        assert b.widget_type == "button"

    def test_click(self):
        b = Button("btn")
        results = []
        b.on("click", lambda c, **kw: results.append("clicked"))
        b.click()
        assert len(results) == 1

    def test_click_disabled(self):
        b = Button("btn")
        b.disabled = True
        results = []
        b.on("click", lambda c, **kw: results.append("clicked"))
        b.click()
        assert len(results) == 0

    def test_on_click_handler(self):
        b = Button("btn")
        results = []
        b.on_click(lambda btn: results.append(btn.name))
        b.click()
        assert results == ["btn"]

    def test_to_dict(self):
        b = Button("btn", label="Test", variant="danger")
        d = b.to_dict()
        assert d["label"] == "Test"
        assert d["variant"] == "danger"


class TestIconButton:
    def test_create(self):
        b = IconButton("icon_btn", label="Settings", icon="gear")
        assert b.icon == "gear"
        assert b.widget_type == "icon_button"


class TestTextInput:
    def test_create(self):
        t = TextInput("name", placeholder="Enter name")
        assert t.placeholder == "Enter name"
        assert t.value == ""
        assert t.required is False

    def test_create_required(self):
        t = TextInput("email", required=True)
        assert t.required is True

    def test_set_value(self):
        t = TextInput("name")
        t.set_value("Alice")
        assert t.value == "Alice"

    def test_set_value_triggers_change(self):
        t = TextInput("name")
        results = []
        t.on("change", lambda c, **kw: results.append(kw))
        t.set_value("Bob")
        assert len(results) == 1
        assert results[0]["new"] == "Bob"

    def test_validate_required_empty(self):
        t = TextInput("email", required=True)
        assert t.validate() is False

    def test_validate_required_filled(self):
        t = TextInput("email", required=True)
        t.set_value("a@b.com")
        assert t.validate() is True

    def test_validate_not_required(self):
        t = TextInput("name")
        assert t.validate() is True


class TestNumberInput:
    def test_create(self):
        n = NumberInput("age", value=25, min_val=0, max_val=120)
        assert n.value == 25
        assert n.min_val == 0
        assert n.max_val == 120
        assert n.step == 1

    def test_set_value_clamp_min(self):
        n = NumberInput("age", value=10, min_val=0)
        n.set_value(-5)
        assert n.value == 0

    def test_set_value_clamp_max(self):
        n = NumberInput("age", value=10, max_val=100)
        n.set_value(150)
        assert n.value == 100

    def test_increment(self):
        n = NumberInput("count", value=5, step=3)
        n.increment()
        assert n.value == 8

    def test_decrement(self):
        n = NumberInput("count", value=10, step=2)
        n.decrement()
        assert n.value == 8


class TestSelect:
    def test_create(self):
        s = Select("color", options=["red", "green", "blue"])
        assert len(s.options) == 3
        assert s.selected == ""

    def test_set_selected(self):
        s = Select("color", options=["red", "green"])
        s.set_selected("green")
        assert s.selected == "green"

    def test_set_selected_invalid(self):
        s = Select("color", options=["red"])
        s.set_selected("purple")
        assert s.selected == ""

    def test_add_option(self):
        s = Select("color")
        s.add_option("red")
        assert "red" in s.options

    def test_remove_option(self):
        s = Select("color", options=["red", "blue"])
        s.set_selected("red")
        s.remove_option("red")
        assert "red" not in s.options
        assert s.selected == ""


class TestCheckbox:
    def test_create(self):
        c = Checkbox("agree", label="I agree", checked=True)
        assert c.label == "I agree"
        assert c.checked is True

    def test_toggle(self):
        c = Checkbox("agree")
        assert c.checked is False
        c.toggle()
        assert c.checked is True
        c.toggle()
        assert c.checked is False


class TestToggle:
    def test_create(self):
        t = Toggle("dark_mode", label="Dark Mode", on=True)
        assert t.label == "Dark Mode"
        assert t.on is True

    def test_toggle(self):
        t = Toggle("dark_mode")
        assert t.on is False
        t.toggle()
        assert t.on is True


class TestTable:
    def test_create(self):
        t = Table("data", columns=[Column("id", "ID"), Column("name", "Name")])
        assert len(t.columns) == 2
        assert len(t.data) == 0

    def test_add_row(self):
        t = Table("data")
        t.add_row({"id": 1, "name": "Alice"})
        assert len(t.data) == 1

    def test_remove_row(self):
        t = Table("data")
        t.add_row({"id": 1})
        t.add_row({"id": 2})
        t.remove_row(0)
        assert len(t.data) == 1
        assert t.data[0]["id"] == 2

    def test_pagination(self):
        t = Table("data", page_size=2)
        for i in range(5):
            t.add_row({"id": i})
        assert t.total_pages == 3
        assert len(t.get_page_data()) == 2

    def test_next_page(self):
        t = Table("data", page_size=1)
        t.add_row({"id": 1})
        t.add_row({"id": 2})
        assert t.page == 0
        t.next_page()
        assert t.page == 1

    def test_prev_page(self):
        t = Table("data", page_size=1)
        t.add_row({"id": 1})
        t.add_row({"id": 2})
        t.next_page()
        t.prev_page()
        assert t.page == 0

    def test_sort_by(self):
        t = Table("data", columns=[Column("name", "Name")])
        t.add_row({"name": "Charlie"})
        t.add_row({"name": "Alice"})
        t.add_row({"name": "Bob"})
        t.sort_by("name")
        page_data = t.get_page_data()
        assert page_data[0]["name"] == "Alice"
        assert page_data[1]["name"] == "Bob"
        assert page_data[2]["name"] == "Charlie"

    def test_sort_toggle_asc_desc(self):
        t = Table("data", columns=[Column("val", "Value")])
        t.add_row({"val": 1})
        t.add_row({"val": 2})
        t.add_row({"val": 3})
        t.sort_by("val")
        assert t._sort_asc is True
        t.sort_by("val")
        assert t._sort_asc is False


class TestBarChart:
    def test_create(self):
        c = BarChart("sales", data={"Jan": 100, "Feb": 200})
        assert c.data["Jan"] == 100

    def test_set_data(self):
        c = BarChart("sales")
        c.set_data({"Q1": 500})
        assert c.data == {"Q1": 500}


class TestLineChart:
    def test_create(self):
        c = LineChart("traffic", series={"visits": [100, 200]})
        assert len(c.series["visits"]) == 2

    def test_add_point(self):
        c = LineChart("traffic", series={"visits": [100]})
        c.add_point("visits", 300)
        assert c.series["visits"] == [100, 300]


class TestPieChart:
    def test_create(self):
        c = PieChart("share", data={"A": 30, "B": 70})
        assert c.total == 100

    def test_get_percentages(self):
        c = PieChart("share", data={"A": 25, "B": 75})
        pct = c.get_percentages()
        assert pct["A"] == 25.0
        assert pct["B"] == 75.0

    def test_get_percentages_empty(self):
        c = PieChart("share")
        pct = c.get_percentages()
        assert pct == {}


class TestGauge:
    def test_create(self):
        g = Gauge("cpu", value=75, max_val=100, unit="%")
        assert g.value == 75
        assert g.percentage == 75.0

    def test_set_value_clamp(self):
        g = Gauge("cpu", max_val=100)
        g.set_value(150)
        assert g.value == 100
        g.set_value(-10)
        assert g.value == 0

    def test_percentage_zero_range(self):
        g = Gauge("cpu", value=50, min_val=50, max_val=50)
        assert g.percentage == 0


class TestCard:
    def test_create(self):
        c = Card("info", title="Info", subtitle="Details")
        assert c.title == "Info"
        assert c.subtitle == "Details"
        assert c.widget_type == "card"


class TestStatCard:
    def test_create(self):
        s = StatCard("revenue", title="Revenue", value="$10K", change=5.2)
        assert s.value == "$10K"
        assert s.change == 5.2
        assert s.is_positive is True

    def test_is_positive_negative(self):
        s = StatCard("revenue", change=-3.1)
        assert s.is_positive is False

    def test_is_positive_none(self):
        s = StatCard("revenue")
        assert s.is_positive is None


class TestForm:
    def test_create(self):
        f = Form("login", title="Login")
        assert f.title == "Login"
        assert f.widget_type == "form"

    def test_add_input(self):
        f = Form("login")
        inp = TextInput("username")
        f.add_input(inp)
        assert "username" in f._inputs

    def test_get_values(self):
        f = Form("settings")
        f.add_input(TextInput("name"))
        f._inputs["name"].set_value("Alice")
        f.add_input(Toggle("dark"))
        f._inputs["dark"].toggle()
        values = f.get_values()
        assert values["name"] == "Alice"
        assert values["dark"] is True

    def test_validate_all_valid(self):
        f = Form("settings")
        f.add_input(TextInput("name", required=True))
        f._inputs["name"].set_value("Alice")
        assert f.validate() is True

    def test_validate_one_invalid(self):
        f = Form("settings")
        f.add_input(TextInput("email", required=True))
        assert f.validate() is False


# ── Docs Site Tests ────────────────────────────────────────────────────

class TestDocsSiteGenerator:
    def test_create(self):
        gen = DocsSiteGenerator(output_dir="/tmp/test_docs")
        assert gen.output_dir == Path("/tmp/test_docs")

    def test_generate_creates_files(self, tmp_path):
        gen = DocsSiteGenerator(output_dir=tmp_path)
        paths = gen.generate()
        assert len(paths) >= 4
        assert gen.get_page_count() >= 4

    def test_generate_creates_index(self, tmp_path):
        gen = DocsSiteGenerator(output_dir=tmp_path)
        gen.generate()
        assert (tmp_path / "index.html").exists()

    def test_generate_creates_components(self, tmp_path):
        gen = DocsSiteGenerator(output_dir=tmp_path)
        gen.generate()
        assert (tmp_path / "components.html").exists()

    def test_generate_creates_tokens(self, tmp_path):
        gen = DocsSiteGenerator(output_dir=tmp_path)
        gen.generate()
        assert (tmp_path / "tokens.html").exists()

    def test_generate_creates_api(self, tmp_path):
        gen = DocsSiteGenerator(output_dir=tmp_path)
        gen.generate()
        assert (tmp_path / "api.html").exists()

    def test_generate_creates_getting_started(self, tmp_path):
        gen = DocsSiteGenerator(output_dir=tmp_path)
        gen.generate()
        assert (tmp_path / "getting-started.html").exists()

    def test_convenience_function(self, tmp_path):
        paths = generate_docs(output_dir=tmp_path)
        assert len(paths) >= 4
