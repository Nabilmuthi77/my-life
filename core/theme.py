"""Theme and Neumorphism Design System for My Life app.
Provides pure cool-white light mode and deep blue-green dark mode,
soft opposing shadows, low-contrast surfaces, and unified aspect styling.
"""

from typing import List, Any, Optional
import flet as ft
from core.constants import ASPECT_DETAILS


class ThemeColors:
    """Color tokens and shadow generators for active theme."""

    def __init__(self, is_dark: bool):
        self.is_dark = is_dark

        if is_dark:
            # Dark Theme: Deep nocturnal blue-green / dark teal
            self.bg_main = "#071A20"
            self.card_surface = "#0A2028"      # Calm, velvety 1-step elevated surface
            self.card_elevated = "#0E2A34"
            self.pressed_surface = "#041217"   # Inset groove
            self.text_primary = "#2DD4BF"      # Cyan-blue text ('biru' all text)
            self.text_secondary = "#2DD4BF"    # Cyan-blue text ('biru' all text)
            self.icon_neutral = "#2DD4BF"
            self.accent_primary = "#2DD4BF"     # Controlled cyan-teal
            self.accent_secondary = "#38BDF8"   # Subtle sky accent
            self.border_subtle = "#0E2833"
            self.shadow_bright = "#0B2129"      # Very subtle soft light (calm, not high/harsh)
            self.shadow_dark = "#030C0F"        # Gentle diffused ambient drop
            self.progress_track = "#041217"
            self.nav_bg = "#0A2028"
        else:
            # Light Theme: Pure Monochromatic Neumorphism (Soft Light x Shadow x Depth)
            self.bg_main = "#F5F7FA"
            self.card_surface = "#F5F7FA"      # Monochromatic base surface
            self.card_elevated = "#F8FAFC"     # Subtle lift
            self.pressed_surface = "#DFE7F0"   # Inset groove
            self.text_primary = "#0D9488"      # Crisp ocean cyan-teal ('biru' all text)
            self.text_secondary = "#0D9488"    # Crisp ocean cyan-teal ('biru' all text)
            self.icon_neutral = "#0D9488"
            self.accent_primary = "#0D9488"     # Controlled cool teal
            self.accent_secondary = "#14B8A6"
            self.border_subtle = "#E2E8F0"
            self.shadow_bright = "#FFFFFF"      # Crisp pure white specular highlight
            self.shadow_dark = "#CCD6E2"        # Soft diffused ambient shadow
            self.progress_track = "#E6ECF3"
            self.nav_bg = "#F5F7FA"

    def aspect_color(self, aspect: str) -> str:
        """Cohesive accent color for aspect cards (unified aesthetic)."""
        return self.accent_primary

    def get_aspect_icon_color(self, aspect: str) -> str:
        """Get soft accent icon color for a specific aspect."""
        info = ASPECT_DETAILS.get(aspect, {})
        return info.get("dark_color" if self.is_dark else "light_color", self.accent_primary)

    def get_aspect_bg_color(self, aspect: str) -> str:
        """Get soft pastel background emblem color for a specific aspect."""
        info = ASPECT_DETAILS.get(aspect, {})
        return info.get("dark_bg" if self.is_dark else "light_bg", self.pressed_surface)

    def raised_shadow(self, depth: Optional[int] = None, blur: Optional[int] = None) -> List[ft.BoxShadow]:
        """Generate soft opposing neumorphic dual shadows."""
        if self.is_dark:
            d = min(depth, 1) if depth is not None else 1
            b = min(blur, 6) if blur is not None else 5
            return [
                ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=b,
                    color=self.shadow_bright,
                    offset=ft.Offset(-d, -d),
                ),
                ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=b + 2,
                    color=self.shadow_dark,
                    offset=ft.Offset(d + 1, d + 1),
                ),
            ]
        else:
            d = depth if depth is not None else 5
            b = blur if blur is not None else 14
            return [
                ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=b,
                    color=self.shadow_bright,
                    offset=ft.Offset(-d, -d),
                ),
                ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=b,
                    color=self.shadow_dark,
                    offset=ft.Offset(d, d),
                ),
            ]

    def subtle_shadow(self, depth: Optional[int] = None, blur: Optional[int] = None) -> List[ft.BoxShadow]:
        """Subtle shadow for buttons, chips, and small controls."""
        if self.is_dark:
            d = depth if depth is not None else 1
            b = blur if blur is not None else 5
            return [
                ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=b,
                    color=self.shadow_bright,
                    offset=ft.Offset(-d, -d),
                ),
                ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=b + 1,
                    color=self.shadow_dark,
                    offset=ft.Offset(d, d),
                ),
            ]
        else:
            d = depth if depth is not None else 3
            b = blur if blur is not None else 8
            return [
                ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=b,
                    color=self.shadow_bright,
                    offset=ft.Offset(-d, -d),
                ),
                ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=b,
                    color=self.shadow_dark,
                    offset=ft.Offset(d, d),
                ),
            ]

    def pressed_shadow(self, depth: Optional[int] = None, blur: Optional[int] = None) -> List[ft.BoxShadow]:
        """Soft dual outside shadow (outside shadow as requested)."""
        d = depth if depth is not None else (1 if self.is_dark else 2)
        b = blur if blur is not None else 4
        return [
            ft.BoxShadow(
                spread_radius=0,
                blur_radius=b,
                color=self.shadow_bright,
                offset=ft.Offset(-d, -d),
            ),
            ft.BoxShadow(
                spread_radius=0,
                blur_radius=b + 1,
                color=self.shadow_dark,
                offset=ft.Offset(d, d),
            ),
        ]

    def floating_nav_shadow(self) -> List[ft.BoxShadow]:
        """Soft, compact floating shadow for minimalist floating bottom navigation capsule."""
        if self.is_dark:
            return [
                ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=12,
                    color="#02070A",
                    offset=ft.Offset(0, 4),
                ),
                ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=4,
                    color="#0B232C",
                    offset=ft.Offset(0, -1),
                ),
            ]
        else:
            return [
                ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=12,
                    color="#CCD6E2",
                    offset=ft.Offset(0, 4),
                ),
                ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=6,
                    color="#FFFFFF",
                    offset=ft.Offset(0, -1),
                ),
            ]


class ThemeManager:
    """Manages active theme state and resolves platform brightness."""

    def __init__(self, initial_preference: str = "auto"):
        self.preference = initial_preference  # 'auto', 'light', 'dark'
        self.platform_is_dark = False

    def update_platform_brightness(self, brightness: Any) -> None:
        """Update platform brightness from page.platform_brightness."""
        if brightness is not None:
            self.platform_is_dark = "dark" in str(brightness).lower()

    @property
    def is_dark(self) -> bool:
        """Determine if effective theme is dark."""
        if self.preference == "dark":
            return True
        elif self.preference == "light":
            return False
        else:
            return self.platform_is_dark

    @property
    def colors(self) -> ThemeColors:
        """Get current active ThemeColors instance."""
        return ThemeColors(self.is_dark)

    def set_preference(self, preference: str) -> ThemeColors:
        """Update preference and return newly active ThemeColors."""
        if preference in ("auto", "light", "dark"):
            self.preference = preference
        return self.colors
