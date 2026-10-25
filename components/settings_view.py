"""Settings View component for My Life application.
Matches Screen 6 ('Pengaturan') of reference design:
- Header and 'Tema Aplikasi' with Putih, Gelap, Auto radio options
- Menu action cards: Tentang Aplikasi, Backup Data, Reset Data
- Footer brand with logo, 'My Life', and 'Versi 1.0.4'
"""

import os
from typing import Callable, Any
import flet as ft
from core.theme import ThemeColors, ThemeManager
from components.neumorphic import NeumorphicCard, NeumorphicBadge


class SettingsView(ft.Container):
    """Settings page matching Screen 6 of reference mockup."""

    def __init__(
        self,
        page: ft.Page,
        theme_manager: ThemeManager,
        data_manager: Any,
        on_theme_changed: Callable[[str], None],
        on_data_reset: Callable[[], None],
    ):
        self.app_page = page
        self.theme_manager = theme_manager
        self.data_manager = data_manager
        self.on_theme_changed = on_theme_changed
        self.on_data_reset = on_data_reset
        self.colors = theme_manager.colors

        super().__init__(
            content=self._build_content(),
            padding=0,
            bgcolor=self.colors.bg_main,
            expand=True,
        )

    def _build_content(self) -> ft.Control:
        pref = self.theme_manager.preference

        # 1. Header Card: Pengaturan
        header_card = NeumorphicCard(
            content=ft.Row(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Icon(
                                    ft.Icons.SETTINGS_ROUNDED,
                                    size=20,
                                    color=self.colors.accent_primary,
                                ),
                                width=40,
                                height=40,
                                border_radius=12,
                                bgcolor="#FFFFFF" if not self.colors.is_dark else self.colors.card_elevated,
                                shadow=self.colors.subtle_shadow(depth=1, blur=2),
                                alignment=ft.Alignment(0, 0),
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        "Pengaturan",
                                        size=18,
                                        weight=ft.FontWeight.W_800,
                                        color=self.colors.text_primary if self.colors.is_dark else self.colors.accent_primary,
                                    ),
                                    ft.Text(
                                        "Preferensi & sistem aplikasi",
                                        size=12,
                                        weight=ft.FontWeight.W_500,
                                        color=self.colors.text_secondary,
                                    ),
                                ],
                                spacing=2,
                            ),
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    NeumorphicBadge(text="Sistem", colors=self.colors, text_size=10, bold=True, elevated=True),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            colors=self.colors,
            padding=ft.Padding.symmetric(horizontal=16, vertical=12),
            border_radius=18,
            margin=ft.Margin.only(left=18, right=18, bottom=10),
        )

        def make_theme_option(label: str, value: str):
            is_active = pref == value
            radio_icon = ft.Icons.RADIO_BUTTON_CHECKED_ROUNDED if is_active else ft.Icons.RADIO_BUTTON_OFF_ROUNDED
            radio_color = self.colors.accent_primary if is_active else self.colors.text_secondary

            return ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(radio_icon, size=20, color=radio_color),
                        ft.Text(
                            label,
                            size=13.5,
                            weight=ft.FontWeight.W_700 if is_active else ft.FontWeight.W_500,
                            color=self.colors.text_primary,
                        ),
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.Padding.symmetric(horizontal=14, vertical=11),
                border_radius=14,
                bgcolor=(
                    ("#FFFFFF" if not self.colors.is_dark else self.colors.card_elevated)
                    if is_active
                    else ft.Colors.TRANSPARENT
                ),
                shadow=self.colors.subtle_shadow(depth=1, blur=2) if is_active else None,
                on_click=lambda e: self.on_theme_changed(value),
                animate=ft.Animation(150, ft.AnimationCurve.EASE_IN_OUT),
            )

        # 2. Unified Section Card: Tema Aplikasi (Header + Options inside 1 NeumorphicCard)
        theme_section_card = NeumorphicCard(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Icon(
                                    ft.Icons.PALETTE_ROUNDED,
                                    size=18,
                                    color=self.colors.accent_primary,
                                ),
                                width=36,
                                height=36,
                                border_radius=18,
                                bgcolor="#FFFFFF" if not self.colors.is_dark else self.colors.card_elevated,
                                shadow=self.colors.subtle_shadow(depth=1, blur=2),
                                alignment=ft.Alignment(0, 0),
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        "Tema Aplikasi",
                                        size=13,
                                        weight=ft.FontWeight.W_700,
                                        color=self.colors.text_primary if self.colors.is_dark else self.colors.accent_primary,
                                    ),
                                    ft.Text(
                                        "Pilih tampilan aplikasi sesuai preferensimu.",
                                        size=11,
                                        color=self.colors.text_secondary,
                                    ),
                                ],
                                spacing=1,
                            ),
                        ],
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Container(height=4),
                    make_theme_option("Putih", "light"),
                    make_theme_option("Gelap", "dark"),
                    make_theme_option("Auto", "auto"),
                ],
                spacing=4,
            ),
            colors=self.colors,
            padding=ft.Padding.symmetric(horizontal=14, vertical=14),
            border_radius=18,
            margin=ft.Margin.only(left=18, right=18, bottom=10),
        )

        def make_action_card(icon_name: str, title: str, on_click: Callable):
            return NeumorphicCard(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Icon(getattr(ft.Icons, icon_name), size=18, color=self.colors.accent_primary),
                            width=34,
                            height=34,
                            border_radius=17,
                            bgcolor="#FFFFFF" if not self.colors.is_dark else self.colors.card_elevated,
                            shadow=self.colors.subtle_shadow(depth=1, blur=2),
                            alignment=ft.Alignment(0, 0),
                        ),
                        ft.Text(
                            title,
                            size=13,
                            weight=ft.FontWeight.W_700,
                            color=self.colors.text_primary if self.colors.is_dark else self.colors.accent_primary,
                            expand=True,
                        ),
                        ft.Icon(ft.Icons.CHEVRON_RIGHT_ROUNDED, size=18, color=self.colors.text_secondary),
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                colors=self.colors,
                padding=ft.Padding.symmetric(horizontal=14, vertical=10),
                border_radius=16,
                margin=ft.Margin.only(left=18, right=18, bottom=8),
                on_click=on_click,
            )

        # 3. Footer Brand Card (Lebar & Tulisan ke bawah sesuai permintaan)
        footer_content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(
                        ft.Icons.SPA_ROUNDED,
                        size=28,
                        color=self.colors.accent_primary,
                    ),
                    ft.Text(
                        "My Life",
                        size=14,
                        weight=ft.FontWeight.W_800,
                        color=self.colors.text_primary if self.colors.is_dark else self.colors.accent_primary,
                    ),
                    ft.Text(
                        "Versi 1.0.4",
                        size=11,
                        weight=ft.FontWeight.W_600,
                        color=self.colors.text_secondary if self.colors.is_dark else self.colors.accent_primary,
                    ),
                    ft.Text(
                        "Progress, not perfection",
                        size=10,
                        italic=True,
                        color=self.colors.text_secondary if self.colors.is_dark else self.colors.accent_primary,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=3,
            ),
            alignment=ft.Alignment(0, 0),
        )

        footer_card = NeumorphicCard(
            content=footer_content,
            colors=self.colors,
            padding=ft.Padding.symmetric(horizontal=16, vertical=16),
            border_radius=18,
            margin=ft.Margin.only(left=18, right=18, top=14, bottom=8),
        )

        controls = [
            ft.Container(height=28),  # Status bar clearance spacer inside scroll view
            header_card,
            theme_section_card,
            ft.Container(height=6),
            make_action_card("INFO_OUTLINE_ROUNDED", "Tentang Aplikasi", self._show_about_modal),
            make_action_card("BACKUP_ROUNDED", "Backup Data", self._show_backup_modal),
            footer_card,
            ft.Container(height=80),  # Safe spacing for floating nav bar
        ]

        return ft.Column(
            controls=controls,
            spacing=0,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )

    def _show_about_modal(self, e):
        dialog = ft.AlertDialog(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.SPA_ROUNDED, size=24, color=self.colors.accent_primary),
                                ft.Text("Tentang My Life", size=16, weight=ft.FontWeight.BOLD, color=self.colors.text_primary),
                            ],
                            spacing=8,
                        ),
                        ft.Divider(height=1, color=self.colors.border_subtle),
                        ft.Text(
                            "My Life adalah aplikasi pelacak perbaikan diri berbasis Flet & Python dengan estetika Modern Neumorphism.\n\n"
                            "Filosofi:\n"
                            "• 'Progress, not perfection.'\n"
                            "• 10x Klik = +1 Poin (maksimal 10)\n"
                            "• -1 Poin otomatis setiap hari (Daily Decay) untuk menjaga konsistensi latihan.\n\n"
                            "Data disimpan lokal 100% pada file my_life_data.json.",
                            size=12,
                            color=self.colors.text_secondary,
                        ),
                    ],
                    spacing=8,
                ),
                width=340,
                padding=10,
            ),
            bgcolor=self.colors.card_surface,
            shape=ft.RoundedRectangleBorder(radius=18),
        )
        self.app_page.show_dialog(dialog)

    def _show_backup_modal(self, e):
        file_path = self.data_manager.file_path
        raw_json = self.data_manager.export_backup_json()
        dialog = ft.AlertDialog(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.BACKUP_ROUNDED, size=22, color=self.colors.accent_primary),
                                ft.Text("Backup Data Lokal", size=16, weight=ft.FontWeight.BOLD, color=self.colors.text_primary),
                            ],
                            spacing=8,
                        ),
                        ft.Divider(height=1, color=self.colors.border_subtle),
                        ft.Text(f"Lokasi File:\n{file_path}", size=11, color=self.colors.text_secondary),
                        ft.Text("Isi JSON Data:", size=12, weight=ft.FontWeight.BOLD, color=self.colors.text_primary),
                        ft.TextField(
                            value=raw_json[:800] + ("..." if len(raw_json) > 800 else ""),
                            read_only=True,
                            multiline=True,
                            max_lines=6,
                            text_size=10,
                            bgcolor="#FFFFFF" if not self.colors.is_dark else self.colors.pressed_surface,
                            border_color=self.colors.border_subtle if not self.colors.is_dark else None,
                        ),
                    ],
                    spacing=6,
                ),
                width=340,
                padding=10,
            ),
            bgcolor=self.colors.card_surface,
            shape=ft.RoundedRectangleBorder(radius=18),
        )
        self.app_page.show_dialog(dialog)

    def _show_reset_modal(self, e):
        def confirm_reset(ev):
            self.app_page.pop_dialog()
            self.data_manager.reset_to_defaults()
            self.on_data_reset()

        dialog = ft.AlertDialog(
            title=ft.Text("Konfirmasi Reset", size=16, weight=ft.FontWeight.BOLD, color=self.colors.text_primary),
            content=ft.Text(
                "Apakah Anda yakin ingin mengembalikan seluruh data skor ke nilai bawaan? "
                "Riwayat klik akan dicadangkan secara aman.",
                size=12,
                color=self.colors.text_secondary,
            ),
            actions=[
                ft.TextButton("Batal", on_click=lambda ev: self.app_page.pop_dialog()),
                ft.FilledButton(
                    "Reset Data",
                    style=ft.ButtonStyle(bgcolor="#EF4444", color="#FFFFFF"),
                    on_click=confirm_reset,
                ),
            ],
            bgcolor=self.colors.card_surface,
            shape=ft.RoundedRectangleBorder(radius=18),
        )
        self.app_page.show_dialog(dialog)
