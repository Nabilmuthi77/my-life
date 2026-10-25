"""Aspect Detail View and Modal dialog.
Matches Screen 3 of reference design:
- Back button, aspect title, and 'DAILY' badge
- Extruded circular hero disc with aspect icon
- Large score (e.g. 3 / 10)
- 10 recessed progress dots with clicks label (0/10 klik)
- Progress bar toward +1 point
- Big tactile minus (-) and plus (+) neumorphic buttons
- Inspirational quote card in Indonesian
"""

from typing import Callable, Dict, Any, List, Optional
import flet as ft
from core.constants import ASPECT_DETAILS, MAX_SCORE, MIN_SCORE
from core.theme import ThemeColors
from components.neumorphic import NeumorphicCard, NeumorphicButton, NeumorphicProgressDots, NeumorphicBadge


def build_aspect_detail_view(
    aspect_key: str,
    colors: ThemeColors,
    data_manager: Any,
    on_back: Callable[[], None],
    on_score_change: Callable[[], None],
) -> ft.Control:
    """Build full-screen Aspect Detail View matching Screen 3 of reference mockup."""
    aspect_info = ASPECT_DETAILS.get(aspect_key, {})
    icon_name = aspect_info.get("icon_name", "SPA_ROUNDED")
    icon_color = colors.get_aspect_icon_color(aspect_key)
    icon_bg = colors.get_aspect_bg_color(aspect_key)
    quote = aspect_info.get("quote", "Fokus pada progres harian secara konsisten.")

    data = data_manager.data
    current_score = data["scores"].get(aspect_key, 0)
    current_progress = data["progress"].get(aspect_key, 0)

    # Reactive controls
    score_display = ft.Text(
        f"{current_score}",
        size=44,
        weight=ft.FontWeight.W_900,
        color=icon_color,
    )
    score_denom = ft.Text(
        " / 10",
        size=18,
        weight=ft.FontWeight.W_600,
        color=icon_color,
    )

    dots_container = ft.Container(
        content=NeumorphicProgressDots(
            current_progress=current_progress,
            accent_color=icon_color,
            colors=colors,
            dot_width=22,
            dot_height=8,
            spacing=0,
            padding_h=12,
            padding_v=6,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
    )

    clicks_label = ft.Text(
        f"{current_progress}/10 klik",
        size=12,
        weight=ft.FontWeight.W_500,
        color=icon_color,
    )

    prog_fraction_label = ft.Text(
        f"{current_progress}/10",
        size=12,
        weight=ft.FontWeight.W_700,
        color=icon_color,
    )

    progress_bar = ft.ProgressBar(
        value=current_progress / 10.0,
        color=icon_color,
        bgcolor=colors.progress_track,
        height=7,
        border_radius=3.5,
    )

    def update_view():
        sc = data_manager.data["scores"].get(aspect_key, 0)
        pr = data_manager.data["progress"].get(aspect_key, 0)
        score_display.value = f"{sc}"
        clicks_label.value = f"{pr}/10 klik"
        prog_fraction_label.value = f"{pr}/10"
        progress_bar.value = pr / 10.0
        dots_container.content = NeumorphicProgressDots(
            current_progress=pr,
            accent_color=icon_color,
            colors=colors,
            dot_width=22,
            dot_height=8,
            spacing=0,
            padding_h=12,
            padding_v=6,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        on_score_change()

    def handle_minus(e):
        data_manager.decrement_aspect_score(aspect_key)
        update_view()

    def handle_plus(e):
        data_manager.increment_aspect_progress(aspect_key)
        update_view()

    # 1. Top Header Row: Back button, Aspect Name, DAILY badge
    back_btn = NeumorphicButton(
        icon=ft.Icons.CHEVRON_LEFT_ROUNDED,
        colors=colors,
        on_click=lambda e: on_back(),
        size=42,
        icon_size=20,
        icon_color=icon_color,
        tooltip="Kembali ke Beranda",
    )

    top_header = ft.Row(
        controls=[
            back_btn,
            ft.Text(
                aspect_info.get("name", ""),
                size=18,
                weight=ft.FontWeight.W_800,
                color=icon_color,
            ),
            NeumorphicBadge(
                text="DAILY",
                colors=colors,
                accent_color=icon_color,
                text_size=11,
                bold=True,
                elevated=True,
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # 2. Hero Centerpiece Dish (Smooth extruded dial matching reference design)
    hero_dish = ft.Container(
        content=ft.Icon(
            getattr(ft.Icons, icon_name, ft.Icons.SPA_ROUNDED),
            size=44,
            color=icon_color,
        ),
        width=96,
        height=96,
        border_radius=48,
        bgcolor=colors.card_surface,
        alignment=ft.Alignment(0, 0),
        shadow=colors.raised_shadow(depth=6, blur=18),
        border=None,
    )

    center_hero = ft.Column(
        controls=[
            hero_dish,
            ft.Container(height=4),
            ft.Text(
                aspect_info.get("description", ""),
                size=14,
                weight=ft.FontWeight.W_600,
                color=icon_color,
            ),
            ft.Row(
                controls=[score_display, score_denom],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.END,
                spacing=2,
            ),
            dots_container,
            clicks_label,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=6,
    )

    # 3. Progress Card toward +1 point
    progress_card_content = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Text(
                        "Progres menuju +1 poin",
                        size=12,
                        weight=ft.FontWeight.W_600,
                        color=icon_color,
                    ),
                    prog_fraction_label,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Container(height=2),
            progress_bar,
        ],
        spacing=6,
    )

    progress_card = NeumorphicCard(
        content=progress_card_content,
        colors=colors,
        padding=14,
        border_radius=16,
        margin=ft.Margin.only(bottom=14),
    )

    # 4. Big Tactile Buttons (Minus and Plus)
    big_minus_btn = NeumorphicButton(
        icon=ft.Icons.REMOVE_ROUNDED,
        colors=colors,
        on_click=handle_minus,
        size=60,
        icon_size=26,
        icon_color=icon_color,
        tooltip="Kurang 1 poin",
    )

    big_plus_btn = NeumorphicButton(
        icon=ft.Icons.ADD_ROUNDED,
        colors=colors,
        on_click=handle_plus,
        size=60,
        icon_size=28,
        icon_color=icon_color,
        tooltip="Tambah progres (+1)",
    )

    tactile_buttons_row = ft.Row(
        controls=[big_minus_btn, big_plus_btn],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # 5. Inspirational Quote Card
    quote_card_content = ft.Row(
        controls=[
            ft.Text(
                "“",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=icon_color,
            ),
            ft.Text(
                quote,
                size=12,
                italic=True,
                color=icon_color,
                expand=True,
            ),
        ],
        spacing=8,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    quote_card = NeumorphicCard(
        content=quote_card_content,
        colors=colors,
        padding=14,
        border_radius=16,
        margin=ft.Margin.only(top=14, bottom=16),
    )

    view_column = ft.Column(
        controls=[
            ft.Container(height=28),  # Status bar clearance spacer inside scroll view
            top_header,
            ft.Container(height=10),
            center_hero,
            ft.Container(height=12),
            progress_card,
            tactile_buttons_row,
            quote_card,
        ],
        scroll=ft.ScrollMode.HIDDEN,
        spacing=0,
        expand=True,
    )

    return ft.Container(
        content=view_column,
        padding=ft.Padding.only(left=20, right=20, top=0, bottom=16),
        bgcolor=colors.bg_main,
        expand=True,
    )


def show_aspect_detail_modal(
    page: ft.Page,
    aspect_key: str,
    score: int,
    progress: int,
    history_7d: List[Dict[str, Any]],
    activities: List[Dict[str, Any]],
    colors: ThemeColors,
    on_score_change: Callable[[], None],
    data_manager: Any,
) -> None:
    """Fallback modal dialog for backward compatibility."""
    view = build_aspect_detail_view(
        aspect_key=aspect_key,
        colors=colors,
        data_manager=data_manager,
        on_back=lambda: page.pop_dialog(),
        on_score_change=on_score_change,
    )

    dialog = ft.AlertDialog(
        content=ft.Container(content=view, width=380, height=580),
        bgcolor=colors.bg_main,
        shape=ft.RoundedRectangleBorder(radius=20),
    )
    page.show_dialog(dialog)
