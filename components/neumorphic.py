"""Neumorphic UI building blocks for My Life application.
Provides pure monolithic neumorphism matching modern reference manifesto:
- Monochromatic continuous base color surfaces
- Soft opposing dual shadows (Soft Light x Shadow x Depth)
- Seamless edges without harsh 1px borders
- Tactile raised buttons and recessed groove tracks
"""

from typing import Callable, Optional, List, Any
import flet as ft
from core.theme import ThemeColors


class NeumorphicCard(ft.Container):
    """A soft, quiet neumorphic raised card container."""

    def __init__(
        self,
        content: ft.Control,
        colors: ThemeColors,
        padding: Any = 16,
        border_radius: int = 20,
        margin: Optional[ft.Margin] = None,
        on_click: Optional[Callable] = None,
        elevated: bool = False,
        shadow: Optional[List[ft.BoxShadow]] = None,
        expand: Optional[bool] = None,
    ):
        surface = colors.card_elevated if elevated else colors.card_surface
        super().__init__(
            content=content,
            bgcolor=surface,
            border_radius=border_radius,
            padding=padding,
            margin=margin if margin is not None else ft.Margin.only(bottom=10),
            shadow=shadow if shadow is not None else colors.raised_shadow(),
            border=None,
            animate=ft.Animation(160, ft.AnimationCurve.EASE_OUT),
            on_click=on_click,
            expand=expand,
        )


class NeumorphicButton(ft.Container):
    """Tactile neumorphic button with comfortable touch target and soft dual shadows."""

    def __init__(
        self,
        icon: Any,
        colors: ThemeColors,
        on_click: Optional[Callable] = None,
        size: int = 44,
        icon_size: int = 20,
        icon_color: Optional[str] = None,
        tooltip: Optional[str] = None,
        disabled: bool = False,
        is_pressed: bool = False,
        bgcolor: Optional[str] = None,
    ):
        self.colors = colors
        self.is_disabled = disabled

        if disabled:
            btn_bg = colors.pressed_surface
            color = colors.text_secondary
            shadow = []
            opacity = 0.35
        elif is_pressed:
            btn_bg = colors.pressed_surface
            color = icon_color or colors.accent_primary
            shadow = colors.pressed_shadow()
            opacity = 1.0
        else:
            btn_bg = bgcolor or colors.card_surface
            color = icon_color or colors.text_primary
            shadow = colors.subtle_shadow(depth=2, blur=6)
            opacity = 1.0

        icon_control = ft.Icon(
            icon,
            size=icon_size,
            color=color,
            opacity=opacity,
        )

        super().__init__(
            content=icon_control,
            width=size,
            height=size,
            bgcolor=btn_bg,
            border_radius=size // 2,
            alignment=ft.Alignment(0, 0),
            shadow=shadow,
            border=None,
            animate=ft.Animation(140, ft.AnimationCurve.EASE_OUT),
            on_click=None if disabled else on_click,
            tooltip=tooltip,
        )


class NeumorphicProgressDots(ft.Container):
    """Recessed 10-dot groove track representing progress (0 to 9 clicks).
    Active dots emit a controlled subtle accent glow.
    """

    def __init__(
        self,
        current_progress: int,
        accent_color: str,
        colors: ThemeColors,
        dot_width: int = 12,
        dot_height: int = 7,
        spacing: int = 3,
        padding_h: int = 8,
        padding_v: int = 5,
        alignment: ft.MainAxisAlignment = ft.MainAxisAlignment.START,
    ):
        dots: List[ft.Control] = []
        for i in range(10):
            is_active = i < current_progress
            dot_color = accent_color if is_active else (
                colors.border_subtle if colors.is_dark else "#D2DCE6"
            )
            dot_shadow = (
                [ft.BoxShadow(spread_radius=0, blur_radius=3, color=accent_color, offset=ft.Offset(0, 0))]
                if is_active
                else [
                    ft.BoxShadow(spread_radius=0, blur_radius=2, color=colors.shadow_dark, offset=ft.Offset(1, 1))
                ]
            )

            dot = ft.Container(
                width=dot_width,
                height=dot_height,
                border_radius=dot_height / 2,
                bgcolor=dot_color,
                shadow=dot_shadow,
                animate=ft.Animation(180, ft.AnimationCurve.EASE_OUT),
            )
            dots.append(dot)

        track_row = ft.Row(
            controls=dots,
            alignment=alignment,
            spacing=0 if alignment == ft.MainAxisAlignment.SPACE_BETWEEN else spacing,
        )

        super().__init__(
            content=track_row,
            bgcolor=colors.progress_track,
            border_radius=11,
            padding=ft.Padding.symmetric(horizontal=padding_h, vertical=padding_v),
            shadow=colors.pressed_shadow(),
            border=None,
        )


class NeumorphicBadge(ft.Container):
    """A soft pill badge for tags, status indicators, and scores with inset or raised tactile depth."""

    def __init__(
        self,
        text: str,
        colors: ThemeColors,
        accent_color: Optional[str] = None,
        text_size: int = 11,
        bold: bool = True,
        elevated: bool = True,
    ):
        color = accent_color or (colors.text_primary if colors.is_dark else colors.accent_primary)
        bg = (colors.card_elevated if colors.is_dark else colors.card_surface) if elevated else colors.pressed_surface
        shadow = colors.subtle_shadow(depth=2, blur=5) if elevated else colors.pressed_shadow()

        super().__init__(
            content=ft.Text(
                text,
                size=text_size,
                weight=ft.FontWeight.W_700 if bold else ft.FontWeight.NORMAL,
                color=color,
            ),
            bgcolor=bg,
            border_radius=12,
            padding=ft.Padding.symmetric(horizontal=8, vertical=3),
            shadow=shadow,
            border=None,
        )
