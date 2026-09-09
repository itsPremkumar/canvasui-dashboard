"""Documentation site generator for CanvasUI.

Generates a complete static documentation site for the CanvasUI Dashboard Component System.
Produces HTML pages with:
- Component reference with live API docs
- Design token visualizer
- Getting started guide
- Interactive examples
- Theme preview (dark/light)
"""
from __future__ import annotations

import html
import os
from pathlib import Path
from typing import Any

from canvasui.canvas import Canvas, Component, Panel, Widget
from canvasui.events import EventBus, Event
from canvasui.layout import GridLayout, FlexLayout
from canvasui.theme import Theme, DarkTheme, LightTheme

try:
    from src.canvasui.design_tokens import DesignTokenSystem, create_light_tokens, create_dark_tokens
    from src.canvasui.components import (
        Button, TextInput, NumberInput, Select, Checkbox, Toggle,
        Table, Column, BarChart, LineChart, PieChart, Gauge,
        Card, StatCard, Form, IconButton,
    )
    HAS_EXTENSIONS = True
except ImportError:
    HAS_EXTENSIONS = False


# ── HTML Templates ───────────────────────────────────────────────────────

_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en" data-theme="{theme}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
:root {{
  --bg: {bg};
  --fg: {fg};
  --accent: {accent};
  --border: {border};
  --text-primary: {text_primary};
  --text-secondary: {text_secondary};
  --success: {success};
  --warning: {warning};
  --error: {error};
  --radius: 8px;
  --font: Inter, system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  font-family: var(--font);
  background: var(--bg);
  color: var(--text-primary);
  line-height: 1.6;
}}
.container {{ max-width: 1200px; margin: 0 auto; padding: 2rem; }}
h1 {{ font-size: 2rem; margin-bottom: 1rem; color: var(--text-primary); }}
h2 {{ font-size: 1.5rem; margin: 2rem 0 1rem; color: var(--text-primary); }}
h3 {{ font-size: 1.25rem; margin: 1.5rem 0 0.5rem; color: var(--accent); }}
p {{ color: var(--text-secondary); margin-bottom: 1rem; }}
a {{ color: var(--accent); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
code {{
  font-family: var(--font-mono);
  background: var(--border);
  padding: 0.2em 0.4em;
  border-radius: 4px;
  font-size: 0.9em;
}}
pre {{
  background: var(--fg);
  color: var(--bg);
  padding: 1rem;
  border-radius: var(--radius);
  overflow-x: auto;
  margin: 1rem 0;
}}
pre code {{ background: none; padding: 0; color: inherit; }}
.nav {{
  display: flex;
  gap: 1.5rem;
  padding: 1rem 2rem;
  border-bottom: 1px solid var(--border);
  background: var(--fg);
  position: sticky;
  top: 0;
  z-index: 100;
}}
.nav a {{ font-weight: 500; }}
.nav .brand {{ font-weight: 700; margin-right: auto; }}
.card {{
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.5rem;
  margin: 1rem 0;
}}
.token-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 0.75rem;
  margin: 1rem 0;
}}
.token-item {{
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  border: 1px solid var(--border);
  border-radius: 4px;
}}
.color-swatch {{
  width: 24px; height: 24px;
  border-radius: 4px;
  border: 1px solid var(--border);
}}
.component-list {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}}
.component-card {{
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1rem;
}}
.component-card h3 {{ margin-top: 0; }}
.badge {{
  display: inline-block;
  padding: 0.15em 0.5em;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
  background: var(--accent);
  color: white;
}}
table {{ width: 100%; border-collapse: collapse; margin: 1rem 0; }}
th, td {{ padding: 0.5rem; text-align: left; border-bottom: 1px solid var(--border); }}
th {{ background: var(--fg); font-weight: 600; }}
footer {{
  margin-top: 4rem;
  padding: 2rem;
  border-top: 1px solid var(--border);
  text-align: center;
  color: var(--text-secondary);
}}
</style>
</head>
<body>
<nav class="nav">
  <a href="index.html" class="brand">CanvasUI</a>
  <a href="getting-started.html">Getting Started</a>
  <a href="components.html">Components</a>
  <a href="tokens.html">Design Tokens</a>
  <a href="api.html">API Reference</a>
</nav>
<div class="container">
{content}
</div>
<footer>CanvasUI Dashboard Component System &mdash; MIT License</footer>
</body>
</html>
"""


# ── Site Generator ──────────────────────────────────────────────────────

class DocsSiteGenerator:
    """Generates a static documentation site for CanvasUI."""

    def __init__(self, output_dir: str | Path = "docs"):
        self.output_dir = Path(output_dir)
        self._pages_generated: list[str] = []

    def generate(self) -> list[str]:
        """Generate all documentation pages. Returns list of file paths."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._pages_generated = []

        self._generate_index()
        self._generate_getting_started()
        self._generate_components()
        self._generate_tokens()
        self._generate_api_reference()

        return self._pages_generated

    def _write_page(self, filename: str, title: str, content: str,
                    theme: str = "light") -> str:
        """Write an HTML page to the output directory."""
        if theme == "dark":
            bg, fg = "#1a1a2e", "#1f2937"
            text_primary, text_secondary = "#f9fafb", "#9ca3af"
        else:
            bg, fg = "#ffffff", "#f9fafb"
            text_primary, text_secondary = "#111827", "#6b7280"

        accent = "#3b82f6" if theme == "light" else "#6366f1"
        border = "#e5e7eb" if theme == "light" else "#374151"
        success = "#10b981" if theme == "light" else "#34d399"
        warning = "#f59e0b" if theme == "light" else "#fbbf24"
        error = "#ef4444" if theme == "light" else "#f87171"

        html_content = _PAGE_TEMPLATE.format(
            title=title,
            content=content,
            theme=theme,
            bg=bg, fg=fg, accent=accent, border=border,
            text_primary=text_primary, text_secondary=text_secondary,
            success=success, warning=warning, error=error,
        )

        path = self.output_dir / filename
        path.write_text(html_content, encoding="utf-8")
        self._pages_generated.append(str(path))
        return str(path)

    def _generate_index(self) -> None:
        """Generate the home page."""
        content = """
<h1>CanvasUI</h1>
<p>A lightweight, extensible dashboard component system with dark/light mode support. Build interactive dashboards in pure Python with zero dependencies.</p>

<h2>Features</h2>
<div class="card">
<ul>
<li><strong>Component hierarchy</strong> — Canvas, Panel, Widget with event bubbling</li>
<li><strong>Event bus</strong> — Decoupled pub/sub communication</li>
<li><strong>Layout managers</strong> — Grid and flexbox layouts</li>
<li><strong>Theme system</strong> — Dark/Light mode with customizable tokens</li>
<li><strong>Rich components</strong> — Buttons, forms, tables, charts, cards</li>
<li><strong>Design tokens</strong> — Complete token system for colors, typography, spacing</li>
<li><strong>Zero dependencies</strong> — Pure Python 3.11+</li>
</ul>
</div>

<h2>Quick Start</h2>
<pre><code>from canvasui.canvas import Canvas, Panel, Widget

canvas = Canvas("main")
panel = canvas.add_panel("Grid Status", x=0, y=0, width=800, height=600)
widget = panel.add_widget("Load Meter", widget_type="gauge")

def on_click(component, **kwargs):
    print(f"Clicked: {component.name}")

widget.on("click", on_click)
canvas.handle_click("widget_0")</code></pre>

<h2>Component Overview</h2>
<div class="component-list">
<div class="component-card"><h3>Buttons</h3><p>Primary, Secondary, Ghost, Danger, IconButton</p></div>
<div class="component-card"><h3>Forms</h3><p>TextInput, NumberInput, Select, Checkbox, Toggle</p></div>
<div class="component-card"><h3>Tables</h3><p>Sortable, paginated data tables</p></div>
<div class="component-card"><h3>Charts</h3><p>Bar, Line, Pie, Gauge</p></div>
<div class="component-card"><h3>Cards</h3><p>Card, StatCard with change indicators</p></div>
<div class="component-card"><h3>Containers</h3><p>Canvas, Panel, Form</p></div>
</div>
"""
        self._write_page("index.html", "CanvasUI — Dashboard Component System", content)

    def _generate_getting_started(self) -> None:
        """Generate the getting started page."""
        content = """
<h1>Getting Started</h1>

<h2>Installation</h2>
<p>CanvasUI is pure Python with zero dependencies. Just include the source:</p>
<pre><code>pip install canvasui</code></pre>
<p>Or copy the <code>canvasui/</code> directory into your project.</p>

<h2>Basic Usage</h2>
<pre><code>from canvasui.canvas import Canvas, Panel, Widget

# Create a canvas
canvas = Canvas("dashboard")

# Add a panel
panel = canvas.add_panel("Status", x=0, y=0, width=800, height=600)

# Add widgets
gauge = panel.add_widget("CPU", widget_type="gauge")
button = panel.add_widget("Refresh", widget_type="button")

# Handle events
gauge.on("click", lambda c, **kw: print(f"{c.name} clicked!"))
canvas.handle_click("CPU")</code></pre>

<h2>Working with Themes</h2>
<pre><code>from canvasui.theme import DarkTheme, LightTheme

dark = DarkTheme()
light = LightTheme()

print(dark.background)  # "#1a1a2e"
print(light.accent)     # "#3b82f6"</code></pre>

<h2>Design Tokens</h2>
<pre><code>from src.canvasui.design_tokens import create_dark_tokens

tokens = create_dark_tokens()
print(tokens.resolve_color("blue.500"))  # "#3b82f6"
print(tokens.resolve_spacing("space_4"))  # "1rem"
print(tokens.resolve_radius("radius_lg"))  # "0.5rem"</code></pre>

<h2>Building Forms</h2>
<pre><code>from src.canvasui.components import Form, TextInput, Toggle

form = Form("settings", title="Settings")
form.add_input(TextInput("name", placeholder="Your name"))
form.add_input(Toggle("dark_mode", label="Dark Mode"))

# Get values
values = form.get_values()</code></pre>

<h2>Creating Charts</h2>
<pre><code>from src.canvasui.components import BarChart, LineChart, Gauge

bar = BarChart("sales", data={"Jan": 100, "Feb": 150, "Mar": 200})
line = LineChart("traffic", series={"visits": [100, 200, 300]})
gauge = Gauge("cpu", value=75, max_val=100, unit="%")</code></pre>

<h2>Next Steps</h2>
<ul>
<li>Read the <a href="components.html">Component Reference</a></li>
<li>Explore <a href="tokens.html">Design Tokens</a></li>
<li>Browse the <a href="api.html">API Reference</a></li>
</ul>
"""
        self._write_page("getting-started.html", "Getting Started — CanvasUI", content)

    def _generate_components(self) -> None:
        """Generate the components reference page."""
        content = """
<h1>Components</h1>
<p>All CanvasUI components organized by category.</p>

<h2>Buttons</h2>
<div class="card">
<table>
<tr><th>Component</th><th>Type</th><th>Description</th></tr>
<tr><td><code>Button</code></td><td><code>button</code></td><td>Clickable button with variants: primary, secondary, ghost, danger</td></tr>
<tr><td><code>IconButton</code></td><td><code>icon_button</code></td><td>Button with an icon glyph</td></tr>
</table>
</div>

<h2>Form Inputs</h2>
<div class="card">
<table>
<tr><th>Component</th><th>Type</th><th>Description</th></tr>
<tr><td><code>TextInput</code></td><td><code>text_input</code></td><td>Text field with placeholder and validation</td></tr>
<tr><td><code>NumberInput</code></td><td><code>number_input</code></td><td>Numeric field with min/max/step</td></tr>
<tr><td><code>Select</code></td><td><code>select</code></td><td>Dropdown with options</td></tr>
<tr><td><code>Checkbox</code></td><td><code>checkbox</code></td><td>Boolean checkbox</td></tr>
<tr><td><code>Toggle</code></td><td><code>toggle</code></td><td>On/off switch</td></tr>
</table>
</div>

<h2>Data Display</h2>
<div class="card">
<table>
<tr><th>Component</th><th>Type</th><th>Description</th></tr>
<tr><td><code>Table</code></td><td><code>table</code></td><td>Sortable, paginated data table</td></tr>
<tr><td><code>BarChart</code></td><td><code>bar_chart</code></td><td>Vertical bar chart</td></tr>
<tr><td><code>LineChart</code></td><td><code>line_chart</code></td><td>Multi-series line chart</td></tr>
<tr><td><code>PieChart</code></td><td><code>pie_chart</code></td><td>Pie/donut chart</td></tr>
<tr><td><code>Gauge</code></td><td><code>gauge</code></td><td>Radial or linear gauge/meter</td></tr>
</table>
</div>

<h2>Cards & Containers</h2>
<div class="card">
<table>
<tr><th>Component</th><th>Type</th><th>Description</th></tr>
<tr><td><code>Card</code></td><td><code>card</code></td><td>Panel with title and subtitle</td></tr>
<tr><td><code>StatCard</code></td><td><code>stat_card</code></td><td>Metric display with change indicator</td></tr>
<tr><td><code>Form</code></td><td><code>form</code></td><td>Input container with validation</td></tr>
</table>
</div>

<h2>Core Components</h2>
<div class="card">
<table>
<tr><th>Component</th><th>Description</th></tr>
<tr><td><code>Canvas</code></td><td>Top-level container for all components</td></tr>
<tr><td><code>Panel</code></td><td>Rectangular panel with position and size</td></tr>
<tr><td><code>Widget</code></td><td>Leaf widget base class</td></tr>
</table>
</div>
"""
        self._write_page("components.html", "Components — CanvasUI", content)

    def _generate_tokens(self) -> None:
        """Generate the design tokens page."""
        # Build palette swatches
        palettes = {
            "Gray": {50: "#f9fafb", 100: "#f3f4f6", 200: "#e5e7eb", 300: "#d1d5db",
                     400: "#9ca3af", 500: "#6b7280", 600: "#4b5563", 700: "#374151",
                     800: "#1f2937", 900: "#111827", 950: "#030712"},
            "Blue": {50: "#eff6ff", 100: "#dbeafe", 200: "#bfdbfe", 300: "#93c5fd",
                     400: "#60a5fa", 500: "#3b82f6", 600: "#2563eb", 700: "#1d4ed8",
                     800: "#1e40af", 900: "#1e3a8a", 950: "#172554"},
            "Green": {50: "#f0fdf4", 100: "#dcfce7", 200: "#bbf7d0", 300: "#86efac",
                      400: "#4ade80", 500: "#22c55e", 600: "#16a34a", 700: "#15803d",
                      800: "#166534", 900: "#14532d", 950: "#052e16"},
            "Red": {50: "#fef2f2", 100: "#fee2e2", 200: "#fecaca", 300: "#fca5a5",
                    400: "#f87171", 500: "#ef4444", 600: "#dc2626", 700: "#b91c1c",
                    800: "#991b1b", 900: "#7f1d1d", 950: "#450a0a"},
        }

        sections = []
        for name, shades in palettes.items():
            swatches = "".join(
                f'<div class="token-item"><div class="color-swatch" style="background:{v}"></div>'
                f'<code>{name.lower()}.{k}</code><span>{v}</span></div>'
                for k, v in shades.items()
            )
            sections.append(f"<h3>{name}</h3><div class='token-grid'>{swatches}</div>")

        palette_html = "\n".join(sections)

        content = f"""
<h1>Design Tokens</h1>
<p>CanvasUI uses a comprehensive design token system for consistent styling across components.</p>

<h2>Color Palettes</h2>
{palette_html}

<h2>Semantic Tokens</h2>
<div class="card">
<table>
<tr><th>Token</th><th>Light</th><th>Dark</th></tr>
<tr><td><code>background</code></td><td>#ffffff</td><td>#1a1a2e</td></tr>
<tr><td><code>foreground</code></td><td>#111827</td><td>#eaeaea</td></tr>
<tr><td><code>accent</code></td><td>#3b82f6</td><td>#6366f1</td></tr>
<tr><td><code>border</code></td><td>#e5e7eb</td><td>#374151</td></tr>
<tr><td><code>text_primary</code></td><td>#111827</td><td>#f9fafb</td></tr>
<tr><td><code>text_secondary</code></td><td>#6b7280</td><td>#9ca3af</td></tr>
<tr><td><code>success</code></td><td>#10b981</td><td>#34d399</td></tr>
<tr><td><code>warning</code></td><td>#f59e0b</td><td>#fbbf24</td></tr>
<tr><td><code>error</code></td><td>#ef4444</td><td>#f87171</td></tr>
</table>
</div>

<h2>Spacing Scale</h2>
<div class="card">
<table>
<tr><th>Token</th><th>Value</th><th>Pixels</th></tr>
<tr><td><code>space_0</code></td><td>0</td><td>0</td></tr>
<tr><td><code>space_1</code></td><td>0.25rem</td><td>4px</td></tr>
<tr><td><code>space_2</code></td><td>0.5rem</td><td>8px</td></tr>
<tr><td><code>space_3</code></td><td>0.75rem</td><td>12px</td></tr>
<tr><td><code>space_4</code></td><td>1rem</td><td>16px</td></tr>
<tr><td><code>space_6</code></td><td>1.5rem</td><td>24px</td></tr>
<tr><td><code>space_8</code></td><td>2rem</td><td>32px</td></tr>
<tr><td><code>space_12</code></td><td>3rem</td><td>48px</td></tr>
<tr><td><code>space_16</code></td><td>4rem</td><td>64px</td></tr>
</table>
</div>

<h2>Border Radius</h2>
<div class="card">
<table>
<tr><th>Token</th><th>Value</th></tr>
<tr><td><code>radius_none</code></td><td>0</td></tr>
<tr><td><code>radius_sm</code></td><td>0.125rem (2px)</td></tr>
<tr><td><code>radius_md</code></td><td>0.375rem (6px)</td></tr>
<tr><td><code>radius_lg</code></td><td>0.5rem (8px)</td></tr>
<tr><td><code>radius_xl</code></td><td>0.75rem (12px)</td></tr>
<tr><td><code>radius_full</code></td><td>9999px</td></tr>
</table>
</div>
"""
        self._write_page("tokens.html", "Design Tokens — CanvasUI", content)

    def _generate_api_reference(self) -> None:
        """Generate the API reference page."""
        content = """
<h1>API Reference</h1>
<p>Complete API documentation for all CanvasUI classes and methods.</p>

<h2>canvasui.canvas</h2>
<div class="card">
<h3>Canvas</h3>
<p>Top-level container. Holds all components and provides selection/click handling.</p>
<pre><code>class Canvas:
    name: str
    children: list[Component]
    selection: list[Component]
    
    add(component: Component) -> Component
    add_panel(name, x, y, width, height) -> Panel
    add_widget(name, widget_type, parent) -> Widget
    find(name) -> Component | None
    select(name) -> bool
    handle_click(name) -> bool
    to_dict() -> dict</code></pre>

<h3>Panel</h3>
<p>Rectangular panel with position and dimensions.</p>
<pre><code>class Panel(Component):
    x: int
    y: int
    width: int
    height: int
    
    resize(width, height) -> None</code></pre>

<h3>Widget</h3>
<p>Leaf widget base class.</p>
<pre><code>class Widget(Component):
    widget_type: str</code></pre>
</div>

<h2>canvasui.events</h2>
<div class="card">
<h3>EventBus</h3>
<p>Central pub/sub event bus for decoupled communication.</p>
<pre><code>class EventBus:
    subscribe(event_name, handler) -> None
    unsubscribe(event_name, handler) -> None
    publish(event: Event) -> None
    clear() -> None</code></pre>
</div>

<h2>canvasui.theme</h2>
<div class="card">
<h3>Theme</h3>
<p>Base theme with semantic color tokens.</p>
<pre><code>class Theme:
    name: str
    background: str
    foreground: str
    accent: str
    ...  
    get(key) -> str
    set(key, value) -> None
    to_dict() -> dict</code></pre>
</div>

<h2>canvasui.components</h2>
<div class="card">
<p>Button, TextInput, NumberInput, Select, Checkbox, Toggle, Table, BarChart, LineChart, PieChart, Gauge, Card, StatCard, Form</p>
<p>See <a href="components.html">Components</a> for details.</p>
</div>
"""
        self._write_page("api.html", "API Reference — CanvasUI", content)

    def get_page_count(self) -> int:
        """Return the number of pages generated."""
        return len(self._pages_generated)


# ── Convenience Functions ───────────────────────────────────────────────

def generate_docs(output_dir: str | Path = "docs") -> list[str]:
    """Generate the complete CanvasUI documentation site.
    
    Args:
        output_dir: Directory to write the docs to.
        
    Returns:
        List of generated file paths.
    """
    generator = DocsSiteGenerator(output_dir)
    return generator.generate()
