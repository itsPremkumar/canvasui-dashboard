# CanvasUI — Dashboard Component System

A lightweight, extensible dashboard component system with dark/light mode support.

## Features

- **Component hierarchy** — Canvas, Panel, Widget with event bubbling
- **Event bus** — Decoupled pub/sub communication
- **Layout managers** — Grid and flexbox layouts
- **Theme system** — Dark/Light mode with customizable tokens
- **Zero dependencies** — Pure Python 3.11+

## Quick Start

```python
from canvasui.canvas import Canvas, Panel, Widget

canvas = Canvas("main")
panel = canvas.add_panel("Grid Status", x=0, y=0, width=800, height=600)
widget = panel.add_widget("Load Meter", widget_type="gauge")

def on_click(component, **kwargs):
    print(f"Clicked: {component.name}")

widget.on("click", on_click)
canvas.handle_click("widget_0")
```

## Tests

```bash
pytest tests/ -v
```

## License

MIT
