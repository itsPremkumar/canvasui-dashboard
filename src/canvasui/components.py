"""Component library for CanvasUI — Buttons, Forms, Tables, Charts.

Extends the base CanvasUI component hierarchy with high-level dashboard widgets:
- Buttons (primary, secondary, ghost, danger)
- Form inputs (text, number, select, checkbox, toggle)
- Tables (sortable, paginated)
- Charts (bar, line, pie, gauge)
- Cards and stat displays
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any, Callable

from canvasui.canvas import Component, Panel, Widget


# ── Button Components ────────────────────────────────────────────────────

class Button(Widget):
    """A clickable button widget."""

    def __init__(self, name: str = "", label: str = "", variant: str = "primary", **kwargs):
        super().__init__(name=name, widget_type="button", **kwargs)
        self.label = label or name
        self.variant = variant  # primary, secondary, ghost, danger
        self.disabled: bool = False
        self._click_handlers: list[Callable] = []

    def click(self) -> None:
        """Simulate a button click."""
        if not self.disabled:
            self.trigger("click")
            for handler in self._click_handlers:
                handler(self)

    def on_click(self, handler: Callable) -> None:
        """Register a click handler."""
        self._click_handlers.append(handler)

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d.update(label=self.label, variant=self.variant, disabled=self.disabled)
        return d


class IconButton(Button):
    """A button with an icon."""

    def __init__(self, name: str = "", label: str = "", icon: str = "", **kwargs):
        super().__init__(name=name, label=label, **kwargs)
        self.icon = icon
        self.widget_type = "icon_button"

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d["icon"] = self.icon
        return d


# ── Form Components ──────────────────────────────────────────────────────

class TextInput(Widget):
    """A text input field."""

    def __init__(self, name: str = "", placeholder: str = "", value: str = "",
                 required: bool = False, **kwargs):
        super().__init__(name=name, widget_type="text_input", **kwargs)
        self.placeholder = placeholder
        self.value = value
        self.required = required
        self._change_handlers: list[Callable] = []

    def set_value(self, value: str) -> None:
        """Set the input value and trigger change."""
        old = self.value
        self.value = value
        if old != value:
            self.trigger("change", old=old, new=value)
            for handler in self._change_handlers:
                handler(self, old=old, new=value)

    def on_change(self, handler: Callable) -> None:
        """Register a change handler."""
        self._change_handlers.append(handler)

    def validate(self) -> bool:
        """Basic validation — returns True if valid."""
        if self.required and not self.value:
            return False
        return True

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d.update(placeholder=self.placeholder, value=self.value, required=self.required)
        return d


class NumberInput(Widget):
    """A numeric input field."""

    def __init__(self, name: str = "", value: float = 0, min_val: float | None = None,
                 max_val: float | None = None, step: float = 1, **kwargs):
        super().__init__(name=name, widget_type="number_input", **kwargs)
        self.value = value
        self.min_val = min_val
        self.max_val = max_val
        self.step = step

    def set_value(self, value: float) -> None:
        """Set the numeric value with clamping."""
        if self.min_val is not None:
            value = max(value, self.min_val)
        if self.max_val is not None:
            value = min(value, self.max_val)
        self.value = value
        self.trigger("change", new=value)

    def increment(self) -> None:
        """Increment by step."""
        self.set_value(self.value + self.step)

    def decrement(self) -> None:
        """Decrement by step."""
        self.set_value(self.value - self.step)

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d.update(value=self.value, min_val=self.min_val, max_val=self.max_val, step=self.step)
        return d


class Select(Widget):
    """A dropdown select input."""

    def __init__(self, name: str = "", options: list[str] | None = None, **kwargs):
        super().__init__(name=name, widget_type="select", **kwargs)
        self.options: list[str] = options or []
        self.selected: str = ""
        self._change_handlers: list[Callable] = []

    def set_selected(self, value: str) -> None:
        """Set the selected option."""
        if value in self.options:
            old = self.selected
            self.selected = value
            self.trigger("change", old=old, new=value)
            for handler in self._change_handlers:
                handler(self, old=old, new=value)

    def add_option(self, option: str) -> None:
        """Add an option to the select."""
        self.options.append(option)

    def remove_option(self, option: str) -> None:
        """Remove an option from the select."""
        if option in self.options:
            self.options.remove(option)
            if self.selected == option:
                self.selected = ""

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d.update(options=self.options, selected=self.selected)
        return d


class Checkbox(Widget):
    """A checkbox input."""

    def __init__(self, name: str = "", label: str = "", checked: bool = False, **kwargs):
        super().__init__(name=name, widget_type="checkbox", **kwargs)
        self.label = label or name
        self.checked = checked

    def toggle(self) -> None:
        """Toggle the checkbox state."""
        self.checked = not self.checked
        self.trigger("change", checked=self.checked)

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d.update(label=self.label, checked=self.checked)
        return d


class Toggle(Widget):
    """A toggle switch."""

    def __init__(self, name: str = "", label: str = "", on: bool = False, **kwargs):
        super().__init__(name=name, widget_type="toggle", **kwargs)
        self.label = label or name
        self.on = on

    def toggle(self) -> None:
        """Toggle the switch."""
        self.on = not self.on
        self.trigger("change", on=self.on)

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d.update(label=self.label, on=self.on)
        return d


# ── Table Component ──────────────────────────────────────────────────────

@dataclass
class Column:
    """Table column definition."""
    key: str
    title: str
    sortable: bool = True
    width: str = "auto"


class Table(Widget):
    """A data table with sorting and pagination."""

    def __init__(self, name: str = "", columns: list[Column] | None = None,
                 data: list[dict[str, Any]] | None = None, page_size: int = 10, **kwargs):
        super().__init__(name=name, widget_type="table", **kwargs)
        self.columns: list[Column] = columns or []
        self.data: list[dict[str, Any]] = data or []
        self.page_size = page_size
        self._page: int = 0
        self._sort_key: str = ""
        self._sort_asc: bool = True

    @property
    def page(self) -> int:
        return self._page

    @property
    def total_pages(self) -> int:
        if not self.data:
            return 0
        return max(1, (len(self.data) + self.page_size - 1) // self.page_size)

    def get_page_data(self) -> list[dict[str, Any]]:
        """Get data for the current page."""
        sorted_data = self._get_sorted_data()
        start = self._page * self.page_size
        end = start + self.page_size
        return sorted_data[start:end]

    def _get_sorted_data(self) -> list[dict[str, Any]]:
        """Get sorted data based on current sort settings."""
        if not self._sort_key:
            return self.data[:]
        return sorted(
            self.data,
            key=lambda row: row.get(self._sort_key, ""),
            reverse=not self._sort_asc,
        )

    def sort_by(self, key: str) -> None:
        """Sort by a column key. Toggles asc/desc if already sorted."""
        if self._sort_key == key:
            self._sort_asc = not self._sort_asc
        else:
            self._sort_key = key
            self._sort_asc = True
        self.trigger("sort", key=key, ascending=self._sort_asc)

    def next_page(self) -> None:
        """Go to the next page."""
        if self._page < self.total_pages - 1:
            self._page += 1
            self.trigger("page_change", page=self._page)

    def prev_page(self) -> None:
        """Go to the previous page."""
        if self._page > 0:
            self._page -= 1
            self.trigger("page_change", page=self._page)

    def go_to_page(self, page: int) -> None:
        """Go to a specific page."""
        if 0 <= page < self.total_pages:
            self._page = page
            self.trigger("page_change", page=self._page)

    def add_row(self, row: dict[str, Any]) -> None:
        """Add a row to the table."""
        self.data.append(row)
        self.trigger("data_change")

    def remove_row(self, index: int) -> None:
        """Remove a row by index."""
        if 0 <= index < len(self.data):
            self.data.pop(index)
            self.trigger("data_change")

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d.update(
            columns=[c.__dict__ for c in self.columns],
            page=self._page,
            total_pages=self.total_pages,
            total_rows=len(self.data),
            sort_key=self._sort_key,
            sort_asc=self._sort_asc,
        )
        return d


# ── Chart Components ─────────────────────────────────────────────────────

class BarChart(Widget):
    """A bar chart widget."""

    def __init__(self, name: str = "", data: dict[str, float] | None = None, **kwargs):
        super().__init__(name=name, widget_type="bar_chart", **kwargs)
        self.data: dict[str, float] = data or {}

    def set_data(self, data: dict[str, float]) -> None:
        """Set chart data."""
        self.data = data
        self.trigger("data_change")

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d["data"] = self.data
        return d


class LineChart(Widget):
    """A line chart widget."""

    def __init__(self, name: str = "", series: dict[str, list[float]] | None = None, **kwargs):
        super().__init__(name=name, widget_type="line_chart", **kwargs)
        self.series: dict[str, list[float]] = series or {}

    def add_point(self, series_name: str, value: float) -> None:
        """Add a data point to a series."""
        if series_name not in self.series:
            self.series[series_name] = []
        self.series[series_name].append(value)
        self.trigger("data_change")

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d["series"] = self.series
        return d


class PieChart(Widget):
    """A pie/donut chart widget."""

    def __init__(self, name: str = "", data: dict[str, float] | None = None, **kwargs):
        super().__init__(name=name, widget_type="pie_chart", **kwargs)
        self.data: dict[str, float] = data or {}

    @property
    def total(self) -> float:
        return sum(self.data.values())

    def get_percentages(self) -> dict[str, float]:
        """Get percentage for each slice."""
        t = self.total
        if t == 0:
            return {k: 0.0 for k in self.data}
        return {k: (v / t) * 100 for k, v in self.data.items()}

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d["data"] = self.data
        d["percentages"] = self.get_percentages()
        return d


class Gauge(Widget):
    """A gauge/meter widget."""

    def __init__(self, name: str = "", value: float = 0, min_val: float = 0,
                 max_val: float = 100, unit: str = "", **kwargs):
        super().__init__(name=name, widget_type="gauge", **kwargs)
        self.value = value
        self.min_val = min_val
        self.max_val = max_val
        self.unit = unit

    @property
    def percentage(self) -> float:
        """Get the current value as a percentage."""
        range_ = self.max_val - self.min_val
        if range_ == 0:
            return 0
        return ((self.value - self.min_val) / range_) * 100

    def set_value(self, value: float) -> None:
        """Set the gauge value with clamping."""
        self.value = max(self.min_val, min(self.max_val, value))
        self.trigger("change", value=self.value)

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d.update(value=self.value, min_val=self.min_val, max_val=self.max_val,
                unit=self.unit, percentage=self.percentage)
        return d


# ── Card & Stat Components ───────────────────────────────────────────────

class Card(Panel):
    """A card panel with a title and content area."""

    def __init__(self, name: str = "", title: str = "", subtitle: str = "", **kwargs):
        super().__init__(name=name, **kwargs)
        self.title = title or name
        self.subtitle = subtitle
        self.widget_type = "card"

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d.update(title=self.title, subtitle=self.subtitle)
        return d


class StatCard(Card):
    """A statistic display card."""

    def __init__(self, name: str = "", title: str = "", value: str = "",
                 change: float | None = None, **kwargs):
        super().__init__(name=name, title=title, **kwargs)
        self.value = value
        self.change = change  # Percentage change
        self.widget_type = "stat_card"

    @property
    def is_positive(self) -> bool | None:
        if self.change is None:
            return None
        return self.change >= 0

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d.update(value=self.value, change=self.change, is_positive=self.is_positive)
        return d


# ── Form Container ───────────────────────────────────────────────────────

class Form(Panel):
    """A form container with validation."""

    def __init__(self, name: str = "", title: str = "", **kwargs):
        super().__init__(name=name, **kwargs)
        self.title = title or name
        self.widget_type = "form"
        self._inputs: dict[str, Widget] = {}

    def add_input(self, input_widget: Widget) -> Widget:
        """Add an input widget to the form."""
        self.add_child(input_widget)
        self._inputs[input_widget.name] = input_widget
        return input_widget

    def get_values(self) -> dict[str, Any]:
        """Get all form values as a dictionary."""
        values = {}
        for name, widget in self._inputs.items():
            if isinstance(widget, TextInput):
                values[name] = widget.value
            elif isinstance(widget, NumberInput):
                values[name] = widget.value
            elif isinstance(widget, Select):
                values[name] = widget.selected
            elif isinstance(widget, Checkbox):
                values[name] = widget.checked
            elif isinstance(widget, Toggle):
                values[name] = widget.on
        return values

    def validate(self) -> bool:
        """Validate all inputs in the form."""
        for widget in self._inputs.values():
            if isinstance(widget, TextInput) and not widget.validate():
                return False
        return True

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d.update(title=self.title, inputs=list(self._inputs.keys()))
        return d
