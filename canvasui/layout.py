"""Layout managers for CanvasUI."""
from __future__ import annotations

from typing import Any

from .canvas import Component, Panel


class GridLayout:
    """Grid-based layout manager."""

    def __init__(self, columns: int = 12, rows: int = 8, gap: int = 8):
        self.columns = columns
        self.rows = rows
        self.gap = gap
        self._grid: dict[tuple[int, int], Component] = {}

    def place(self, component: Component, col: int, row: int, colspan: int = 1, rowspan: int = 1) -> None:
        """Place a component in the grid."""
        if isinstance(component, Panel):
            component.x = col * (100 + self.gap)
            component.y = row * (100 + self.gap)
            component.width = colspan * 100
            component.height = rowspan * 100
        self._grid[(col, row)] = component

    def get_at(self, col: int, row: int) -> Component | None:
        """Get component at grid position."""
        return self._grid.get((col, row))

    def remove(self, col: int, row: int) -> None:
        """Remove component from grid position."""
        self._grid.pop((col, row), None)

    def get_all(self) -> list[Component]:
        """Get all placed components."""
        return list(self._grid.values())


class FlexLayout:
    """Flexbox-style layout manager."""

    def __init__(self, direction: str = "row", gap: int = 8):
        self.direction = direction
        self.gap = gap
        self._items: list[Component] = []

    def add(self, component: Component, flex: int = 1) -> None:
        """Add component with flex weight."""
        self._items.append((component, flex))
        self._reflow()

    def remove(self, component: Component) -> None:
        """Remove a component."""
        self._items = [(c, f) for c, f in self._items if c is not component]

    def _reflow(self) -> None:
        """Recalculate positions."""
        offset = 0
        for component, flex in self._items:
            if isinstance(component, Panel):
                if self.direction == "row":
                    component.x = offset
                    offset += component.width + self.gap
                else:
                    component.y = offset
                    offset += component.height + self.gap

    def get_items(self) -> list[tuple[Component, int]]:
        """Get all items with flex values."""
        return self._items[:]
