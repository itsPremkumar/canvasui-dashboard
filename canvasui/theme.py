"""Theme system for CanvasUI — Dark/Light mode support."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Theme:
    """Base theme."""
    name: str = "base"
    background: str = "#ffffff"
    foreground: str = "#000000"
    accent: str = "#3b82f6"
    border: str = "#e5e7eb"
    text_primary: str = "#111827"
    text_secondary: str = "#6b7280"
    success: str = "#10b981"
    warning: str = "#f59e0b"
    error: str = "#ef4444"
    custom: dict[str, str] = field(default_factory=dict)

    def get(self, key: str) -> str:
        """Get a theme value by key."""
        if hasattr(self, key):
            return getattr(self, key)
        return self.custom.get(key, "")

    def set(self, key: str, value: str) -> None:
        """Set a custom theme value."""
        self.custom[key] = value

    def to_dict(self) -> dict[str, Any]:
        """Convert theme to dictionary."""
        return {
            "name": self.name,
            "background": self.background,
            "foreground": self.foreground,
            "accent": self.accent,
            "border": self.border,
            "text_primary": self.text_primary,
            "text_secondary": self.text_secondary,
            "success": self.success,
            "warning": self.warning,
            "error": self.error,
            "custom": self.custom,
        }


class DarkTheme(Theme):
    """Dark mode theme."""

    def __init__(self):
        super().__init__(
            name="dark",
            background="#1a1a2e",
            foreground="#eaeaea",
            accent="#6366f1",
            border="#374151",
            text_primary="#f9fafb",
            text_secondary="#9ca3af",
            success="#34d399",
            warning="#fbbf24",
            error="#f87171",
        )


class LightTheme(Theme):
    """Light mode theme."""

    def __init__(self):
        super().__init__(
            name="light",
            background="#ffffff",
            foreground="#111827",
            accent="#3b82f6",
            border="#e5e7eb",
            text_primary="#111827",
            text_secondary="#6b7280",
            success="#10b981",
            warning="#f59e0b",
            error="#ef4444",
        )
