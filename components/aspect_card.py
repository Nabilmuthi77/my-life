"""Aspect Card component for My Life dashboard.
Provides cohesive, sleek horizontal neumorphic cards matching Screen 2 of reference design:
- Pastel circular emblem with aspect icon
- Aspect title, description, and chevron
- Score fraction (e.g. 3/10) with recessed 10-dots progress track
- Tactile minus and plus buttons with haptic feedback
- Tap card to open full Aspect Detail view
"""

from typing import Callable, Any, Optional
import flet as ft
from core.constants import ASPECT_DETAILS, MAX_SCORE, MIN_SCORE
from core.theme import ThemeColors
from components.neumorphic import NeumorphicCard, NeumorphicButton, NeumorphicProgressDots


class AspectCard(ft.Container):
    """Cohesive, sleek interactive card for one of the 5 life aspects."""

    def __init__(
        self,
        aspect_key: str,
        score: int,
        progress: int,
        colors: ThemeColors,
        page: ft.Page,
        data_manager: Any,
        on_change: Callable[[], None],
        on_open_detail: Optional[Callable[[str], None]] = None,
    ):
        self.aspect_key = aspect_key
        self.score = score
        self.progress = progress
        self.colors = colors
        self.app_page = page
        self.data_manager = data_manager
        self.on_change = on_change
        self.on_open_detail = on_open_detail

        aspect_info = ASPECT_DETAILS.get(aspect_key, {})
        icon_name = aspect_info.get("icon_name", "SPA_ROUNDED")
        icon_color = colors.get_aspect_icon_color(aspect_key)
        icon_bg = colors.get_aspect_bg_color(aspect_key)

        # 1. Left Pastel Circular Emblem (Tactile sculpted disc)
        icon_emblem = ft.Container(
            content=ft.Icon(
                getattr(ft.Icons, icon_name, ft.Icons.SPA_ROUNDED),
                size=20,
                color=icon_color,
            ),
            width=42,
            height=42,
            border_radius=21,
            bgcolor=icon_bg,
            alignment=ft.Alignment(0, 0),
            shadow=colors.subtle_shadow(depth=2, blur=5),
        )

        # 2. Center Column: Title, Subtitle, Chevron + Score and Progress Dots
        title_row = ft.Row(
            controls=[
                ft.Text(
                    aspect_info.get("name", ""),
                    size=14,
                    weight=ft.FontWeight.W_700,
                    color=colors.text_primary,
                ),
                ft.Text(
                    aspect_info.get("description", ""),
                    size=11,
                    color=colors.text_secondary,
                    no_wrap=True,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
                ft.Icon(
                    ft.Icons.CHEVRON_RIGHT_ROUNDED,
                    size=15,
                    color=colors.text_secondary,
                ),
            ],
            spacing=4,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        score_and_dots_row = ft.Row(
            controls=[
                ft.Text(
                    f"{score}/10",
                    size=11,
                    weight=ft.FontWeight.W_700,
                    color=colors.text_primary,
                ),
                NeumorphicProgressDots(
                    current_progress=progress,
                    accent_color=icon_color,
                    colors=colors,
                    dot_width=6,
                    dot_height=6,
                    spacing=3,
                    padding_h=6,
                    padding_v=3,
                ),
            ],
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        center_info = ft.Column(
            controls=[title_row, score_and_dots_row],
            spacing=4,
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # 3. Right Tactile Action Buttons
        is_min = score <= MIN_SCORE
        is_max = score >= MAX_SCORE

        minus_btn = NeumorphicButton(
            icon=ft.Icons.REMOVE_ROUNDED,
            colors=colors,
            on_click=self._handle_minus,
            size=34,
            icon_size=16,
            icon_color=colors.text_secondary if is_min else colors.text_primary,
            tooltip="Kurang 1 poin" if not is_min else "Skor sudah 0",
            disabled=is_min,
        )

        plus_btn = NeumorphicButton(
            icon=ft.Icons.ADD_ROUNDED,
            colors=colors,
            on_click=self._handle_plus,
            size=38,
            icon_size=18,
            icon_color=colors.text_secondary if is_max else icon_color,
            tooltip="Tambah progres (+1)" if not is_max else "Skor sudah 10",
            disabled=is_max,
        )

        action_buttons = ft.Row(
            controls=[minus_btn, plus_btn],
            spacing=5,
            alignment=ft.MainAxisAlignment.END,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        card_row = ft.Row(
            controls=[
                icon_emblem,
                center_info,
                action_buttons,
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        card_container = NeumorphicCard(
            content=card_row,
            colors=colors,
            padding=ft.Padding.symmetric(horizontal=12, vertical=10),
            border_radius=18,
            margin=ft.Margin.only(bottom=9),
            on_click=self._open_detail,
        )

        super().__init__(content=card_container)

    def _handle_minus(self, e):
        self.data_manager.decrement_aspect_score(self.aspect_key)
        self.on_change()

    def _handle_plus(self, e):
        self.data_manager.increment_aspect_progress(self.aspect_key)
        self.on_change()

    def _open_detail(self, e):
        if self.on_open_detail:
            self.on_open_detail(self.aspect_key)
        else:
            from components.aspect_detail_modal import show_aspect_detail_modal
            data = self.data_manager.data
            show_aspect_detail_modal(
                page=self.app_page,
                aspect_key=self.aspect_key,
                score=data["scores"][self.aspect_key],
                progress=data["progress"][self.aspect_key],
                history_7d=self.data_manager.get_last_7_days_history(),
                activities=data.get("click_history", []),
                colors=self.colors,
                on_score_change=self.on_change,
                data_manager=self.data_manager,
            )
