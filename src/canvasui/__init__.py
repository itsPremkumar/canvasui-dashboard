"""CanvasUI Dashboard — Interactive dashboard framework.

This package provides:
- design_tokens.py: Theme and token system
- components.py: Component library (buttons, forms, tables, charts)
- docs_site.py: Documentation site generator
"""
from __future__ import annotations

__version__ = "1.0.0"

# Re-export core canvasui components
from canvasui.canvas import Canvas, Component, Panel, Widget
from canvasui.events import EventBus, Event
from canvasui.layout import GridLayout, FlexLayout
from canvasui.theme import Theme, DarkTheme, LightTheme

# Design tokens
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

# Components
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

# Docs site
from src.canvasui.docs_site import DocsSiteGenerator, generate_docs

__all__ = [
    # Core
    "Canvas", "Component", "Panel", "Widget",
    "EventBus", "Event",
    "GridLayout", "FlexLayout",
    "Theme", "DarkTheme", "LightTheme",
    # Design tokens
    "DesignTokenSystem", "ColorPalette",
    "TypographyTokens", "SpacingTokens", "ShadowTokens", "RadiusTokens",
    "BreakpointTokens", "ZIndexTokens", "MotionTokens",
    "create_light_tokens", "create_dark_tokens",
    # Components
    "Button", "IconButton",
    "TextInput", "NumberInput", "Select", "Checkbox", "Toggle",
    "Table", "Column",
    "BarChart", "LineChart", "PieChart", "Gauge",
    "Card", "StatCard", "Form",
    # Docs
    "DocsSiteGenerator", "generate_docs",
]
