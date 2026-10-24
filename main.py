"""My Life — Premium Self-Improvement Android & Desktop Application.
Built with Python & Flet, featuring Modern Neumorphism, Local JSON Storage,
Five Life Aspects, Daily Decay, and 7-Day History Tracking.
Matches the official modern neumorphism reference design.
"""

import datetime
from typing import Optional
import flet as ft

from core.constants import (
    ASPECT_KEYS,
    ASPECT_DETAILS,
    REFERENCE_DATE,
)
from core.data_manager import DataManager
from core.theme import ThemeManager, ThemeColors
from components.neumorphic import NeumorphicCard, NeumorphicBadge
from components.aspect_card import AspectCard
from components.aspect_detail_modal import build_aspect_detail_view
from components.history_view import HistoryView
from components.settings_view import SettingsView


def format_indonesian_date(date_obj: datetime.date) -> str:
    """Format a date into Indonesian locale string, e.g. 'Selasa, 22 Oktober 2026'."""
    days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    months = [
        "", "Januari", "Februari", "Maret", "April", "Mei", "Juni",
        "Juli", "Agustus", "September", "Oktober", "November", "Desember"
    ]
    day_name = days[date_obj.weekday()]
    month_name = months[date_obj.month]
    return f"{day_name}, {date_obj.day} {month_name} {date_obj.year}"


def main(page: ft.Page):
    """Application main entry point (synchronous lifecycle)."""
    page.title = "My Life — Progress, not perfection"
    page.padding = 0
    page.spacing = 0

    # Configure window sizing for desktop preview (Mobile 9:19 viewport ratio)
    page.window.width = 412
    page.window.height = 840
    page.window.min_width = 360
    page.window.min_height = 640

    # Custom font from assets and invisible scrollbar configuration
    page.fonts = {
        "ComicRelief": "fonts/ComicRelief-Regular.ttf",
        "ComicReliefBold": "fonts/ComicRelief-Bold.ttf",
    }
    scrollbar_cfg = ft.ScrollbarTheme(
        thickness=0,
        thumb_visibility=False,
        track_visibility=False,
        thumb_color="transparent",
        track_color="transparent",
        track_border_color="transparent",
    )
    page.theme = ft.Theme(font_family="ComicRelief", scrollbar_theme=scrollbar_cfg)
    page.dark_theme = ft.Theme(font_family="ComicRelief", scrollbar_theme=scrollbar_cfg)

    # 1. Initialize Data Manager and apply daily decay on startup
    data_manager = DataManager()
    today_str = datetime.date.today().isoformat()
    data_manager.apply_daily_decay(today_str)

    # 2. Initialize Theme Manager
    initial_pref = data_manager.data.get("theme", "auto")
    theme_manager = ThemeManager(initial_preference=initial_pref)
    theme_manager.update_platform_brightness(page.platform_brightness)

    # App Navigation State
    current_tab_index = 0
    active_aspect_detail: Optional[str] = None

    # Root structural controls
    content_area = ft.Container(expand=True)
    nav_bar_container = ft.Container()

    def open_aspect_detail(aspect_key: str):
        nonlocal active_aspect_detail
        active_aspect_detail = aspect_key
        render_current_view()

    def close_aspect_detail():
        nonlocal active_aspect_detail
        active_aspect_detail = None
        render_current_view()

    # Dynamic UI Renderers
    def build_dashboard_view(colors: ThemeColors) -> ft.Control:
        """Build Home / Dashboard matching modern neumorphism reference."""
        today_date = datetime.date.today()
        date_str_formatted = format_indonesian_date(today_date)
        summary = data_manager.get_summary()
        scores = data_manager.data["scores"]
        progress = data_manager.data["progress"]

        # 1. Header Card (Wrapping "My Life", Date, Subtitle, and Quick Theme Switcher)
        header_left = ft.Column(
            controls=[
                ft.Text("My Life", size=22, weight=ft.FontWeight.W_800, color=colors.accent_primary),
                ft.Text(date_str_formatted, size=11, weight=ft.FontWeight.W_500, color=colors.text_secondary),
                ft.Text("Jadi 1% lebih baik setiap hari.", size=11, color=colors.text_secondary),
            ],
            spacing=2,
            expand=True,
        )

        # Quick Theme Capsule Pill (Putih, Gelap, Auto)
        def make_quick_icon(icon_name: str, val: str):
            is_active = theme_manager.preference == val
            return ft.Container(
                content=ft.Icon(
                    getattr(ft.Icons, icon_name),
                    size=14,
                    color=colors.accent_primary,
                    opacity=1.0 if is_active else 0.55,
                ),
                padding=ft.Padding.symmetric(horizontal=6, vertical=4),
                border_radius=10,
                bgcolor=colors.card_surface if is_active else "transparent",
                shadow=colors.subtle_shadow(depth=1, blur=3) if is_active else [],
                on_click=lambda e, v=val: handle_theme_change(v),
            )

        quick_theme_pill = ft.Container(
            content=ft.Row(
                controls=[
                    make_quick_icon("LIGHT_MODE_ROUNDED", "light"),
                    make_quick_icon("DARK_MODE_ROUNDED", "dark"),
                    make_quick_icon("BRIGHTNESS_AUTO_ROUNDED", "auto"),
                ],
                spacing=2,
            ),
            bgcolor=colors.pressed_surface,
            border_radius=14,
            padding=3,
            shadow=colors.pressed_shadow(),
            border=None,
        )

        header_row = ft.Row(
            controls=[header_left, quick_theme_pill],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        header_card = NeumorphicCard(
            content=header_row,
            colors=colors,
            padding=ft.Padding.symmetric(horizontal=16, vertical=12),
            border_radius=20,
            margin=ft.Margin.only(bottom=10),
            elevated=False,
        )

        # 2. Side-by-Side Summary Cards (Both matching Card Jiwa's darker surface color)
        avg_val = summary["average"]
        total_val = summary["total"]

        # Left Card (~58% width): Rata-Rata Hari Ini
        card_avg_content = ft.Column(
            controls=[
                ft.Text(
                    "Rata-Rata Hari Ini",
                    size=13,
                    weight=ft.FontWeight.W_700,
                    color=colors.accent_primary,
                ),
                ft.Row(
                    controls=[
                        ft.Text(
                            f"{avg_val:.1f}",
                            size=28,
                            weight=ft.FontWeight.W_900,
                            color=colors.accent_primary,
                        ),
                        ft.Text(
                            " / 10",
                            size=13,
                            weight=ft.FontWeight.W_700,
                            color=colors.accent_primary,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.END,
                    spacing=1,
                ),
            ],
            spacing=4,
        )

        card_avg = NeumorphicCard(
            content=card_avg_content,
            colors=colors,
            padding=ft.Padding.symmetric(horizontal=14, vertical=12),
            border_radius=18,
            margin=ft.Margin.only(right=4),
            elevated=False,
        )

        # Right Card (~42% width): Total (Matching font size 13 bold and uniform accent color)
        card_total_content = ft.Column(
            controls=[
                ft.Text(
                    "Total",
                    size=13,
                    weight=ft.FontWeight.W_700,
                    color=colors.accent_primary,
                ),
                ft.Row(
                    controls=[
                        ft.Text(
                            f"{total_val}",
                            size=28,
                            weight=ft.FontWeight.W_900,
                            color=colors.accent_primary,
                        ),
                        ft.Text(
                            " / 50",
                            size=13,
                            weight=ft.FontWeight.W_700,
                            color=colors.accent_primary,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.END,
                    spacing=1,
                ),
            ],
            spacing=4,
        )

        card_total = NeumorphicCard(
            content=card_total_content,
            colors=colors,
            padding=ft.Padding.symmetric(horizontal=14, vertical=12),
            border_radius=18,
            margin=ft.Margin.only(left=4),
            elevated=False,
        )

        summary_row = ft.Row(
            controls=[
                ft.Container(content=card_avg, expand=3),
                ft.Container(content=card_total, expand=2),
            ],
            spacing=0,
        )

        # 3. Section Heading Card: Lima pilar hidup
        section_heading_content = ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.GRID_VIEW_ROUNDED,
                            size=15,
                            color=colors.accent_primary,
                        ),
                        ft.Text(
                            "Lima Pilar Hidup",
                            size=13,
                            weight=ft.FontWeight.W_700,
                            color=colors.accent_primary,
                        ),
                    ],
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                NeumorphicBadge(
                    text="5 Aspek",
                    colors=colors,
                    text_size=10,
                    bold=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        section_heading_card = NeumorphicCard(
            content=section_heading_content,
            colors=colors,
            padding=ft.Padding.symmetric(horizontal=14, vertical=10),
            border_radius=16,
            margin=ft.Margin.only(top=4, bottom=10),
            elevated=False,
        )

        # 4. Five Aspect Cards (Sleek Horizontal)
        aspect_cards: list[ft.Control] = []
        for key in ASPECT_KEYS:
            card = AspectCard(
                aspect_key=key,
                score=scores[key],
                progress=progress[key],
                colors=colors,
                page=page,
                data_manager=data_manager,
                on_change=lambda: render_current_view(),
                on_open_detail=open_aspect_detail,
            )
            aspect_cards.append(card)

        dashboard_column = ft.Column(
            controls=[
                header_card,
                ft.Container(height=4),
                summary_row,
                ft.Container(height=4),
                section_heading_card,
                *aspect_cards,
                ft.Container(height=80),  # bottom safe spacing for compact floating navigation bar
            ],
            spacing=0,
            scroll=ft.ScrollMode.HIDDEN,
        )

        return ft.Container(
            content=dashboard_column,
            padding=ft.Padding.only(left=18, right=18, top=36, bottom=14),
            expand=True,
        )

    def build_navigation_bar(colors: ThemeColors) -> ft.Control:
        """Neumorphic custom Floating Bottom Navigation Bar (Minimalist Capsule Pill).
        Features sleek compact dimensions, neat outside shadows, and clear icons.
        """
        tabs = [
            ("Beranda", ft.Icons.HOME_ROUNDED, 0),
            ("Riwayat", ft.Icons.HISTORY_ROUNDED, 1),
            ("Pengaturan", ft.Icons.SETTINGS_ROUNDED, 2),
        ]

        def on_nav_click(idx: int):
            nonlocal current_tab_index, active_aspect_detail
            active_aspect_detail = None  # close detail if navigating tabs
            if current_tab_index != idx:
                current_tab_index = idx
                render_current_view()

        nav_items = []
        for label, icon, idx in tabs:
            is_active = (current_tab_index == idx) and (active_aspect_detail is None)
            icon_color = colors.accent_primary
            label_color = colors.accent_primary

            # Sleek, minimalist icon + text with clear active prominence
            item_content = ft.Column(
                controls=[
                    ft.Icon(icon, size=16, color=icon_color),
                    ft.Text(
                        label,
                        size=9.5,
                        weight=ft.FontWeight.W_700 if is_active else ft.FontWeight.W_500,
                        color=label_color,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
                opacity=1.0 if is_active else 0.55,
            )

            # Active item has neat, subtle elevated outside shadow
            if is_active:
                bg_color = colors.card_elevated if colors.is_dark else "#FFFFFF"
                shadow = colors.subtle_shadow(depth=1, blur=4)
            else:
                bg_color = "transparent"
                shadow = []

            item = ft.Container(
                content=item_content,
                padding=ft.Padding.symmetric(horizontal=12, vertical=4),
                border_radius=15,
                bgcolor=bg_color,
                shadow=shadow,
                border=None,
                on_click=lambda e, i=idx: on_nav_click(i),
                animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            )
            nav_items.append(item)

        floating_card = ft.Container(
            content=ft.Row(
                controls=nav_items,
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=colors.card_surface,
            height=50,
            border_radius=25,
            padding=ft.Padding.symmetric(horizontal=6, vertical=2),
            shadow=colors.floating_nav_shadow(),
            border=None,
        )

        return floating_card

    def handle_theme_change(pref: str):
        """Called when theme switcher is toggled."""
        data_manager.set_theme_preference(pref)
        theme_manager.set_preference(pref)
        apply_theme_to_page()

    def handle_data_reset():
        """Called after user confirms reset in SettingsView."""
        data_manager.reset_to_initial(datetime.date.today().isoformat())
        render_current_view()

    def apply_theme_to_page():
        """Apply active theme to page and re-render full interface."""
        colors = theme_manager.colors
        page.theme_mode = ft.ThemeMode.DARK if theme_manager.is_dark else ft.ThemeMode.LIGHT
        page.bgcolor = colors.bg_main
        render_current_view()

    def render_current_view():
        """Render the active view or aspect detail view."""
        colors = theme_manager.colors
        page.bgcolor = colors.bg_main

        # Update Floating Navigation Bar
        nav_bar_container.content = build_navigation_bar(colors)

        # Check if an Aspect Detail screen is actively opened
        if active_aspect_detail is not None:
            content_area.content = build_aspect_detail_view(
                aspect_key=active_aspect_detail,
                colors=colors,
                data_manager=data_manager,
                on_back=close_aspect_detail,
                on_score_change=render_current_view,
            )
        elif current_tab_index == 0:
            content_area.content = build_dashboard_view(colors)
        elif current_tab_index == 1:
            history_7d = data_manager.get_last_7_days_history()
            activities = data_manager.data.get("click_history", [])
            content_area.content = HistoryView(
                history_7d=history_7d,
                activities=activities,
                colors=colors,
                on_refresh=render_current_view,
            )
        elif current_tab_index == 2:
            content_area.content = SettingsView(
                page=page,
                theme_manager=theme_manager,
                data_manager=data_manager,
                on_theme_changed=handle_theme_change,
                on_data_reset=handle_data_reset,
            )

        page.update()

    # Platform Brightness Change Listener
    def on_platform_brightness_change(e):
        theme_manager.update_platform_brightness(page.platform_brightness)
        if theme_manager.preference == "auto":
            apply_theme_to_page()

    page.on_platform_brightness_change = on_platform_brightness_change

    # Root Layout Construction with True Floating Navigation
    nav_bar_container.bottom = 14
    nav_bar_container.left = 32
    nav_bar_container.right = 32

    root_layout = ft.Stack(
        controls=[
            content_area,
            nav_bar_container,
        ],
        expand=True,
    )

    # Mount initial layout and render view
    colors = theme_manager.colors
    page.theme_mode = ft.ThemeMode.DARK if theme_manager.is_dark else ft.ThemeMode.LIGHT
    page.bgcolor = colors.bg_main
    nav_bar_container.content = build_navigation_bar(colors)
    content_area.content = build_dashboard_view(colors)

    page.add(root_layout)
    page.update()


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
