"""Design tokens for CanvasUI — Theme and token system.

Extends the base Theme system with a comprehensive token hierarchy:
- Color tokens (semantic + palette)
- Typography tokens (font families, sizes, weights, line heights)
- Spacing tokens (margin, padding, gap scales)
- Shadow tokens (elevation levels)
- Border radius tokens
- Breakpoint tokens
- Z-index tokens
- Motion tokens (durations, easings)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from canvasui.theme import Theme, DarkTheme, LightTheme


# ── Color Palette ──────────────────────────────────────────────────────────

@dataclass
class ColorPalette:
    """A color palette with shades 50-950."""
    _shades: dict[int, str] = field(default_factory=dict)

    def shade(self, level: int) -> str:
        """Get a specific shade (50, 100, 200, ..., 950)."""
        if level not in self._shades:
            raise KeyError(f"Shade {level} not in palette. Available: {sorted(self._shades.keys())}")
        return self._shades[level]

    def __getitem__(self, level: int) -> str:
        return self.shade(level)

    @property
    def lightest(self) -> str:
        return self._shades[min(self._shades)]

    @property
    def darkest(self) -> str:
        return self._shades[max(self._shades)]


def _gray_palette() -> ColorPalette:
    return ColorPalette(_shades={
        50: "#f9fafb", 100: "#f3f4f6", 200: "#e5e7eb", 300: "#d1d5db",
        400: "#9ca3af", 500: "#6b7280", 600: "#4b5563", 700: "#374151",
        800: "#1f2937", 900: "#111827", 950: "#030712",
    })


def _blue_palette() -> ColorPalette:
    return ColorPalette(_shades={
        50: "#eff6ff", 100: "#dbeafe", 200: "#bfdbfe", 300: "#93c5fd",
        400: "#60a5fa", 500: "#3b82f6", 600: "#2563eb", 700: "#1d4ed8",
        800: "#1e40af", 900: "#1e3a8a", 950: "#172554",
    })


def _green_palette() -> ColorPalette:
    return ColorPalette(_shades={
        50: "#f0fdf4", 100: "#dcfce7", 200: "#bbf7d0", 300: "#86efac",
        400: "#4ade80", 500: "#22c55e", 600: "#16a34a", 700: "#15803d",
        800: "#166534", 900: "#14532d", 950: "#052e16",
    })


def _red_palette() -> ColorPalette:
    return ColorPalette(_shades={
        50: "#fef2f2", 100: "#fee2e2", 200: "#fecaca", 300: "#fca5a5",
        400: "#f87171", 500: "#ef4444", 600: "#dc2626", 700: "#b91c1c",
        800: "#991b1b", 900: "#7f1d1d", 950: "#450a0a",
    })


def _yellow_palette() -> ColorPalette:
    return ColorPalette(_shades={
        50: "#fffbeb", 100: "#fef3c7", 200: "#fde68a", 300: "#fcd34d",
        400: "#fbbf24", 500: "#f59e0b", 600: "#d97706", 700: "#b45309",
        800: "#92400e", 900: "#78350f", 950: "#451a03",
    })


def _purple_palette() -> ColorPalette:
    return ColorPalette(_shades={
        50: "#faf5ff", 100: "#f3e8ff", 200: "#e9d5ff", 300: "#d8b4fe",
        400: "#c084fc", 500: "#a855f7", 600: "#9333ea", 700: "#7e22ce",
        800: "#6b21a8", 900: "#581c87", 950: "#3b0764",
    })


# ── Typography Tokens ─────────────────────────────────────────────────────

@dataclass
class TypographyTokens:
    """Typography scale and font definitions."""
    font_family_sans: str = "Inter, system-ui, -apple-system, sans-serif"
    font_family_mono: str = "JetBrains Mono, Fira Code, monospace"
    font_family_serif: str = "Georgia, serif"

    font_size_xs: str = "0.75rem"    # 12px
    font_size_sm: str = "0.875rem"   # 14px
    font_size_base: str = "1rem"     # 16px
    font_size_lg: str = "1.125rem"   # 18px
    font_size_xl: str = "1.25rem"    # 20px
    font_size_2xl: str = "1.5rem"    # 24px
    font_size_3xl: str = "1.875rem"  # 30px
    font_size_4xl: str = "2.25rem"   # 36px

    font_weight_normal: int = 400
    font_weight_medium: int = 500
    font_weight_semibold: int = 600
    font_weight_bold: int = 700

    line_height_tight: str = "1.25"
    line_height_normal: str = "1.5"
    line_height_relaxed: str = "1.75"

    letter_spacing_tight: str = "-0.025em"
    letter_spacing_normal: str = "0"
    letter_spacing_wide: str = "0.025em"


# ── Spacing Tokens ────────────────────────────────────────────────────────

@dataclass
class SpacingTokens:
    """Spacing scale for margin, padding, and gaps."""
    space_0: str = "0"
    space_1: str = "0.25rem"   # 4px
    space_2: str = "0.5rem"    # 8px
    space_3: str = "0.75rem"   # 12px
    space_4: str = "1rem"      # 16px
    space_5: str = "1.25rem"   # 20px
    space_6: str = "1.5rem"    # 24px
    space_8: str = "2rem"      # 32px
    space_10: str = "2.5rem"   # 40px
    space_12: str = "3rem"     # 48px
    space_16: str = "4rem"     # 64px
    space_20: str = "5rem"     # 80px
    space_24: str = "6rem"     # 96px

    def __getitem__(self, key: str) -> str:
        return getattr(self, key, "")


# ── Shadow Tokens ─────────────────────────────────────────────────────────

@dataclass
class ShadowTokens:
    """Elevation shadow levels."""
    shadow_none: str = "none"
    shadow_sm: str = "0 1px 2px 0 rgb(0 0 0 / 0.05)"
    shadow_md: str = "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)"
    shadow_lg: str = "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)"
    shadow_xl: str = "0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)"
    shadow_2xl: str = "0 25px 50px -12px rgb(0 0 0 / 0.25)"


# ── Border Radius Tokens ─────────────────────────────────────────────────

@dataclass
class RadiusTokens:
    """Border radius scale."""
    radius_none: str = "0"
    radius_sm: str = "0.125rem"   # 2px
    radius_md: str = "0.375rem"   # 6px
    radius_lg: str = "0.5rem"     # 8px
    radius_xl: str = "0.75rem"    # 12px
    radius_2xl: str = "1rem"      # 16px
    radius_full: str = "9999px"


# ── Breakpoint Tokens ────────────────────────────────────────────────────

@dataclass
class BreakpointTokens:
    """Responsive breakpoints."""
    breakpoint_sm: str = "640px"
    breakpoint_md: str = "768px"
    breakpoint_lg: str = "1024px"
    breakpoint_xl: str = "1280px"
    breakpoint_2xl: str = "1536px"


# ── Z-Index Tokens ───────────────────────────────────────────────────────

@dataclass
class ZIndexTokens:
    """Z-index scale for layering."""
    z_auto: str = "auto"
    z_0: str = "0"
    z_10: str = "10"
    z_20: str = "20"
    z_30: str = "30"
    z_40: str = "40"
    z_50: str = "50"


# ── Motion Tokens ────────────────────────────────────────────────────────

@dataclass
class MotionTokens:
    """Animation durations and easing curves."""
    duration_fast: str = "150ms"
    duration_normal: str = "250ms"
    duration_slow: str = "350ms"
    duration_slower: str = "500ms"

    ease_linear: str = "linear"
    ease_in: str = "cubic-bezier(0.4, 0, 1, 1)"
    ease_out: str = "cubic-bezier(0, 0, 0.2, 1)"
    ease_in_out: str = "cubic-bezier(0.4, 0, 0.2, 1)"


# ── Design Token System ──────────────────────────────────────────────────

@dataclass
class DesignTokenSystem:
    """Complete design token system combining all token categories."""
    # Color palettes
    gray: ColorPalette = field(default_factory=_gray_palette)
    blue: ColorPalette = field(default_factory=_blue_palette)
    green: ColorPalette = field(default_factory=_green_palette)
    red: ColorPalette = field(default_factory=_red_palette)
    yellow: ColorPalette = field(default_factory=_yellow_palette)
    purple: ColorPalette = field(default_factory=_purple_palette)

    # Token categories
    typography: TypographyTokens = field(default_factory=TypographyTokens)
    spacing: SpacingTokens = field(default_factory=SpacingTokens)
    shadows: ShadowTokens = field(default_factory=ShadowTokens)
    radius: RadiusTokens = field(default_factory=RadiusTokens)
    breakpoints: BreakpointTokens = field(default_factory=BreakpointTokens)
    z_index: ZIndexTokens = field(default_factory=ZIndexTokens)
    motion: MotionTokens = field(default_factory=MotionTokens)

    # Semantic color tokens (resolved from theme)
    theme: Theme = field(default_factory=LightTheme)

    def resolve_color(self, token: str) -> str:
        """Resolve a semantic color token to a hex value.

        Supports:
        - Named theme tokens: 'background', 'foreground', 'accent', etc.
        - Palette references: 'blue.500', 'gray.900', etc.
        - Raw hex: '#ff0000'
        """
        # Raw hex pass-through
        if token.startswith("#"):
            return token

        # Palette reference: "blue.500"
        if "." in token:
            parts = token.split(".", 1)
            palette_name, shade_str = parts[0], parts[1]
            palette = getattr(self, palette_name, None)
            if isinstance(palette, ColorPalette):
                try:
                    return palette.shade(int(shade_str))
                except (ValueError, KeyError):
                    pass
            return token

        # Theme attribute
        return self.theme.get(token)

    def resolve_spacing(self, token: str) -> str:
        """Resolve a spacing token to a CSS value."""
        return getattr(self.spacing, token, token)

    def resolve_shadow(self, token: str) -> str:
        """Resolve a shadow token to a CSS value."""
        return getattr(self.shadows, token, token)

    def resolve_radius(self, token: str) -> str:
        """Resolve a radius token to a CSS value."""
        return getattr(self.radius, token, token)

    def to_dict(self) -> dict[str, Any]:
        """Convert the entire token system to a dictionary."""
        return {
            "colors": {
                "gray": self.gray._shades,
                "blue": self.blue._shades,
                "green": self.green._shades,
                "red": self.red._shades,
                "yellow": self.yellow._shades,
                "purple": self.purple._shades,
            },
            "typography": self.typography.__dict__,
            "spacing": self.spacing.__dict__,
            "shadows": self.shadows.__dict__,
            "radius": self.radius.__dict__,
            "breakpoints": self.breakpoints.__dict__,
            "z_index": self.z_index.__dict__,
            "motion": self.motion.__dict__,
            "theme": self.theme.to_dict(),
        }


def create_light_tokens() -> DesignTokenSystem:
    """Create a light-mode design token system."""
    return DesignTokenSystem(theme=LightTheme())


def create_dark_tokens() -> DesignTokenSystem:
    """Create a dark-mode design token system."""
    return DesignTokenSystem(theme=DarkTheme())
