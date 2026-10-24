"""Splash Screen component for My Life application.
Provides a modern branded entry screen featuring the growth leaf logo,
tagline, and smooth transition to the main dashboard.
"""

from typing import Callable
import flet as ft
from core.theme import ThemeColors


class SplashScreen(ft.Container):
    """Initial splash screen view."""

    def __init__(
        self,
        colors: ThemeColors,
        on_finish: Callable[[], None],
    ):
        self.colors = colors
        self.on_finish = on_finish

        super().__init__(
            content=self._build_content(),
            bgcolor=colors.bg_main,
            alignment=ft.Alignment(0, 0),
            on_click=lambda e: on_finish(),
        )

    def _build_content(self) -> ft.Control:
        return ft.Column(
            controls=[
                ft.Container(
                    content=ft.Image(
                        src="assets/logo.png",
                        width=110,
                        height=110,
                        fit=ft.BoxFit.CONTAIN,
                    ),
                    width=130,
                    height=130,
                    bgcolor=self.colors.card_surface,
                    border_radius=65,
                    alignment=ft.Alignment(0, 0),
                    shadow=self.colors.raised_shadow(depth=6, blur=18),
                    border=ft.Border.all(1, self.colors.border_subtle),
                    animate=ft.Animation(400, ft.AnimationCurve.EASE_OUT),
                ),
                ft.Container(height=16),
                ft.Text(
                    "My Life",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color=self.colors.text_primary,
                ),
                ft.Text(
                    "Progress, not perfection.",
                    size=14,
                    italic=True,
                    color=self.colors.accent_primary,
                    weight=ft.FontWeight.W_500,
                ),
                ft.Container(height=24),
                ft.ProgressRing(
                    width=22,
                    height=22,
                    stroke_width=2.5,
                    color=self.colors.accent_primary,
                ),
                ft.Container(height=8),
                ft.Text(
                    "Memuat lima pilar hidup...",
                    size=11,
                    color=self.colors.text_secondary,
                ),
                ft.Container(height=14),
                ft.TextButton(
                    content=ft.Row(
                        controls=[
                            ft.Text("Mulai Sekarang", size=13, weight=ft.FontWeight.W_600, color=self.colors.accent_primary),
                            ft.Icon(ft.Icons.ARROW_FORWARD, size=16, color=self.colors.accent_primary),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=4,
                    ),
                    on_click=lambda e: self.on_finish(),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )
