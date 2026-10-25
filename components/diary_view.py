"""Diary View component for My Life application.
Provides a modern Neumorphic journaling and diary experience:
- Tactile write card with Title, Mood Selector, and Content
- Inset groove fields matching monolithic Neumorphic design
- Saved diary entries feed with dates, moods, and deletion
- Clean adherence to Light Mode (Jiwa Green) and Dark Mode (Crisp White)
"""

import datetime
import calendar
import math
from typing import Callable, Any, List, Optional
import flet as ft
from core.theme import ThemeColors
from components.neumorphic import NeumorphicCard, NeumorphicBadge, NeumorphicButton

MONTH_NAMES_ID = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember"
]

DAY_NAMES_ID = ["MIN", "SEN", "SEL", "RAB", "KAM", "JUM", "SAB"]


def format_diary_date(iso_date: str) -> str:
    """Format YYYY-MM-DD to DD Mmm YYYY (e.g. 25 Oktober 2026)."""
    parts = iso_date.split("-")
    if len(parts) == 3:
        try:
            day = int(parts[2])
            month_idx = int(parts[1]) - 1
            year = parts[0]
            if 0 <= month_idx < 12:
                return f"{day} {MONTH_NAMES_ID[month_idx]} {year}"
            return iso_date
        except Exception:
            return iso_date
    return iso_date


class DiaryView(ft.Container):
    """Full-screen Neumorphic Diary and Journaling View."""

    def __init__(
        self,
        page: ft.Page,
        colors: ThemeColors,
        data_manager: Any,
        on_change: Optional[Callable[[], None]] = None,
    ):
        self.app_page = page
        self.colors = colors
        self.data_manager = data_manager
        self.on_change = on_change
        self.selected_mood = "Bersyukur"
        self.is_writing_expanded = False
        self.selected_date = datetime.date.today()
        now_dt = datetime.datetime.now()
        self.selected_time = f"{now_dt.hour:02d}:{now_dt.minute:02d}"

        super().__init__(
            content=self._build_content(),
            padding=ft.Padding.only(top=52, bottom=0),
            expand=True,
        )

    def _select_mood(self, mood: str):
        self.selected_mood = mood
        self.content = self._build_content()
        self.update()

    def _show_snack(self, message: str, bgcolor: str = "#0D9488"):
        snack = ft.SnackBar(
            content=ft.Text(message, color="#FFFFFF"),
            bgcolor=bgcolor,
            duration=2000,
        )
        if hasattr(self.app_page, "show_dialog"):
            self.app_page.show_dialog(snack)
        elif hasattr(self.app_page, "open"):
            self.app_page.open(snack)
        else:
            self.app_page.snack_bar = snack
            self.app_page.snack_bar.open = True
            self.app_page.update()

    def _save_diary(
        self,
        title: str,
        content: str,
        custom_date: Optional[str] = None,
        custom_time: Optional[str] = None,
    ):
        if not content.strip():
            self._show_snack("Isi catatan tidak boleh kosong.", bgcolor="#EF4444")
            return

        date_to_save = custom_date or self.selected_date.strftime("%Y-%m-%d")
        time_to_save = custom_time or self.selected_time

        self.data_manager.add_diary(
            title=title.strip(),
            content=content.strip(),
            mood=self.selected_mood,
            custom_date=date_to_save,
            custom_time=time_to_save,
        )

        self._show_snack(
            "Catatan diary berhasil disimpan!",
            bgcolor=self.colors.accent_primary if not self.colors.is_dark else "#0F766E",
        )

        # Reset selection to current date and time
        self.selected_date = datetime.date.today()
        now_dt = datetime.datetime.now()
        self.selected_time = f"{now_dt.hour:02d}:{now_dt.minute:02d}"

        if self.on_change:
            self.on_change()
        else:
            self.content = self._build_content()
            self.update()

    def _delete_diary(self, diary_id: str):
        self.data_manager.delete_diary(diary_id)
        self._show_snack("Catatan telah dihapus.", bgcolor="#6B7280")
        if self.on_change:
            self.on_change()
        else:
            self.content = self._build_content()
            self.update()

    def _show_diary_detail_dialog(self, diary: dict):
        d_id = diary.get("id", "")
        d_title = diary.get("title", "")
        d_content = diary.get("content", "")
        d_mood = diary.get("mood", "Bersyukur")
        d_date = diary.get("date", "")
        d_created = diary.get("created_at", "")
        time_str = d_created[11:16] if len(d_created) >= 16 else ""
        date_str = format_diary_date(d_date) if d_date else ""
        full_time = f"{date_str} · {time_str}" if time_str else date_str

        close_btn = NeumorphicButton(
            icon=ft.Icons.CLOSE_ROUNDED,
            colors=self.colors,
            size=32,
            icon_size=16,
            icon_color=self.colors.text_secondary,
            on_click=lambda e: self.app_page.pop_dialog(),
            tooltip="Tutup",
        )

        header_row = ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        NeumorphicBadge(
                            text=d_mood,
                            colors=self.colors,
                            text_size=10.5,
                            bold=True,
                            elevated=True,
                        ),
                        ft.Text(
                            full_time,
                            size=11,
                            weight=ft.FontWeight.W_500,
                            color=self.colors.text_secondary,
                        ),
                    ],
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                close_btn,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        modal_controls: List[ft.Control] = [header_row]

        if d_title:
            modal_controls.append(ft.Container(height=4))
            modal_controls.append(
                ft.Text(
                    d_title,
                    size=15,
                    weight=ft.FontWeight.W_800,
                    color=self.colors.text_primary,
                )
            )

        modal_controls.append(ft.Container(height=6))

        scrollable_text = ft.Column(
            controls=[
                ft.Text(
                    d_content,
                    size=12.5,
                    weight=ft.FontWeight.W_400,
                    color=self.colors.text_primary,
                    selectable=True,
                )
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
            spacing=4,
        )

        reading_box = ft.Container(
            content=scrollable_text,
            bgcolor="#FFFFFF" if not self.colors.is_dark else self.colors.pressed_surface,
            border_radius=16,
            padding=14,
            height=240,
            border=None,
            shadow=self.colors.subtle_shadow(depth=1, blur=3) if not self.colors.is_dark else self.colors.pressed_shadow(),
        )

        modal_controls.append(reading_box)
        modal_controls.append(ft.Container(height=8))

        done_btn = NeumorphicCard(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.CHECK_ROUNDED, size=15, color=self.colors.accent_primary),
                    ft.Text(
                        "Selesai Membaca",
                        size=12,
                        weight=ft.FontWeight.W_700,
                        color=self.colors.text_primary if self.colors.is_dark else self.colors.accent_primary,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=6,
            ),
            colors=self.colors,
            padding=ft.Padding.symmetric(horizontal=16, vertical=10),
            border_radius=12,
            on_click=lambda e: self.app_page.pop_dialog(),
            elevated=True,
            expand=True,
        )

        del_btn_dialog = ft.Container(
            content=ft.Icon(
                ft.Icons.DELETE_OUTLINE_ROUNDED,
                size=18,
                color="#EF4444",
            ),
            padding=8,
            border_radius=10,
            bgcolor=self.colors.card_surface,
            shadow=self.colors.subtle_shadow(depth=1, blur=3),
            tooltip="Hapus catatan",
            on_click=lambda e: (self.app_page.pop_dialog(), self._delete_diary(d_id)),
        )

        action_row = ft.Row(
            controls=[del_btn_dialog, done_btn],
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        modal_controls.append(action_row)

        detail_card = NeumorphicCard(
            content=ft.Column(
                controls=modal_controls,
                spacing=2,
                tight=True,
            ),
            colors=self.colors,
            padding=ft.Padding.symmetric(horizontal=16, vertical=16),
            border_radius=22,
            margin=0,
        )

        dialog = ft.AlertDialog(
            content=ft.Container(
                content=detail_card,
                width=340,
                padding=0,
            ),
            content_padding=0,
            inset_padding=ft.Padding.symmetric(horizontal=12, vertical=20),
            bgcolor="transparent",
            shape=ft.RoundedRectangleBorder(radius=22),
        )
        self.app_page.show_dialog(dialog)

    def _show_custom_calendar_dialog(self, label_ref: Optional[ft.Text] = None):
        """Custom Neumorphic Calendar Picker Modal matching reference date-picker.js:
        - View: 'calendar', 'months', 'years'
        - Month button in header opens 12-month picker
        - Year button in header opens 12-year decade picker
        - Clicking any date instantly selects it, closes modal, and updates label & view
        - Zero edge clipping with tailored padding
        """
        view_year = self.selected_date.year
        view_month = self.selected_date.month
        current_view = "calendar"
        year_base = (view_year // 12) * 12
        cal_wrap_width = 350
        cal_inner_width = 318

        calendar_container = ft.Container(
            width=cal_inner_width,
            padding=ft.Padding.symmetric(horizontal=3),
        )

        calendar_card = NeumorphicCard(
            content=calendar_container,
            colors=self.colors,
            padding=ft.Padding.symmetric(horizontal=16, vertical=14),
            border_radius=22,
            margin=0,
        )

        dialog = ft.AlertDialog(
            content=ft.Container(
                content=calendar_card,
                width=cal_wrap_width,
                padding=0,
            ),
            content_padding=0,
            inset_padding=ft.Padding.symmetric(horizontal=12, vertical=20),
            bgcolor="transparent",
            shape=ft.RoundedRectangleBorder(radius=22),
        )

        def close_dialog(e=None):
            if hasattr(self.app_page, "pop_dialog"):
                self.app_page.pop_dialog()
            elif hasattr(self.app_page, "close"):
                self.app_page.close(dialog)
            else:
                dialog.open = False
            self.app_page.update()

        def on_date_click(y: int, m: int, d: int):
            self.selected_date = datetime.date(y, m, d)
            if label_ref:
                label_ref.value = format_diary_date(self.selected_date.strftime("%Y-%m-%d"))
            close_dialog()
            self.update()

        def set_view(new_view: str):
            nonlocal current_view
            current_view = new_view
            render_view()
            calendar_container.update()

        def render_view():
            nonlocal view_year, view_month, year_base

            if current_view == "months":
                # Header for Months View
                back_btn = NeumorphicButton(
                    icon=ft.Icons.ARROW_BACK_ROUNDED,
                    colors=self.colors,
                    size=34,
                    icon_size=18,
                    icon_color=self.colors.text_primary,
                    bgcolor="#FFFFFF" if not self.colors.is_dark else self.colors.card_surface,
                    on_click=lambda e: set_view("calendar"),
                    tooltip="Kembali ke kalender",
                )
                header_row = ft.Row(
                    controls=[
                        back_btn,
                        ft.Text(
                            f"Pilih Bulan ({view_year})",
                            size=14.5,
                            weight=ft.FontWeight.W_800,
                            color=self.colors.text_primary if self.colors.is_dark else self.colors.accent_primary,
                        ),
                        ft.Container(width=34),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                )
                header_card = NeumorphicCard(
                    content=header_row,
                    colors=self.colors,
                    padding=ft.Padding.symmetric(horizontal=10, vertical=7),
                    border_radius=16,
                    margin=ft.Margin.only(bottom=6),
                    elevated=False,
                )

                month_cells = []
                for idx, m_name in enumerate(MONTH_NAMES_ID):
                    m_num = idx + 1
                    is_active = (m_num == view_month)

                    def make_month_click(chosen_m):
                        return lambda e: select_month(chosen_m)

                    cell = ft.Container(
                        content=ft.Text(
                            m_name[:3] if len(m_name) > 4 else m_name,
                            size=12,
                            weight=ft.FontWeight.W_700 if is_active else ft.FontWeight.W_600,
                            color="#FFFFFF" if is_active else (self.colors.text_primary if self.colors.is_dark else self.colors.accent_primary),
                            text_align=ft.TextAlign.CENTER,
                        ),
                        width=88,
                        height=42,
                        border_radius=12,
                        bgcolor=self.colors.accent_primary if is_active else self.colors.card_surface,
                        alignment=ft.Alignment(0, 0),
                        shadow=self.colors.subtle_shadow(depth=2, blur=4) if is_active else self.colors.subtle_shadow(depth=1, blur=2),
                        on_click=make_month_click(m_num),
                        tooltip=m_name,
                    )
                    month_cells.append(cell)

                def select_month(chosen_m: int):
                    nonlocal view_month
                    view_month = chosen_m
                    set_view("calendar")

                month_rows = [
                    ft.Row(controls=month_cells[i : i + 3], alignment=ft.MainAxisAlignment.SPACE_EVENLY)
                    for i in range(0, 12, 3)
                ]

                calendar_container.content = ft.Column(
                    controls=[
                        header_card,
                        ft.Container(height=4),
                        *month_rows,
                        ft.Container(height=4),
                    ],
                    spacing=8,
                    tight=True,
                )

            elif current_view == "years":
                # Header for Years View with decade navigation
                def prev_decade(e):
                    nonlocal year_base
                    year_base -= 12
                    render_view()
                    calendar_container.update()

                def next_decade(e):
                    nonlocal year_base
                    year_base += 12
                    render_view()
                    calendar_container.update()

                prev_decade_btn = NeumorphicButton(
                    icon=ft.Icons.CHEVRON_LEFT_ROUNDED,
                    colors=self.colors,
                    size=34,
                    icon_size=18,
                    icon_color=self.colors.text_primary,
                    bgcolor="#FFFFFF" if not self.colors.is_dark else self.colors.card_surface,
                    on_click=prev_decade,
                    tooltip="Dekade sebelumnya",
                )
                next_decade_btn = NeumorphicButton(
                    icon=ft.Icons.CHEVRON_RIGHT_ROUNDED,
                    colors=self.colors,
                    size=34,
                    icon_size=18,
                    icon_color=self.colors.text_primary,
                    bgcolor="#FFFFFF" if not self.colors.is_dark else self.colors.card_surface,
                    on_click=next_decade,
                    tooltip="Dekade berikutnya",
                )
                header_row = ft.Row(
                    controls=[
                        prev_decade_btn,
                        ft.Text(
                            f"{year_base} - {year_base + 11}",
                            size=14.5,
                            weight=ft.FontWeight.W_800,
                            color=self.colors.text_primary if self.colors.is_dark else self.colors.accent_primary,
                        ),
                        next_decade_btn,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                )
                header_card = NeumorphicCard(
                    content=header_row,
                    colors=self.colors,
                    padding=ft.Padding.symmetric(horizontal=10, vertical=7),
                    border_radius=16,
                    margin=ft.Margin.only(bottom=6),
                    elevated=False,
                )

                year_cells = []
                for yr in range(year_base, year_base + 12):
                    is_active = (yr == view_year)

                    def make_year_click(chosen_yr):
                        return lambda e: select_year(chosen_yr)

                    cell = ft.Container(
                        content=ft.Text(
                            str(yr),
                            size=12,
                            weight=ft.FontWeight.W_700 if is_active else ft.FontWeight.W_600,
                            color="#FFFFFF" if is_active else self.colors.text_primary,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        width=88,
                        height=42,
                        border_radius=12,
                        bgcolor=self.colors.accent_primary if is_active else self.colors.card_surface,
                        alignment=ft.Alignment(0, 0),
                        shadow=self.colors.subtle_shadow(depth=2, blur=4) if is_active else self.colors.subtle_shadow(depth=1, blur=2),
                        on_click=make_year_click(yr),
                    )
                    year_cells.append(cell)

                def select_year(chosen_yr: int):
                    nonlocal view_year
                    view_year = chosen_yr
                    set_view("calendar")

                year_rows = [
                    ft.Row(controls=year_cells[i : i + 3], alignment=ft.MainAxisAlignment.SPACE_EVENLY)
                    for i in range(0, 12, 3)
                ]

                calendar_container.content = ft.Column(
                    controls=[
                        header_card,
                        ft.Container(height=4),
                        *year_rows,
                        ft.Container(height=4),
                    ],
                    spacing=8,
                    tight=True,
                )

            else:
                # Standard Calendar View
                month_name = MONTH_NAMES_ID[view_month - 1]

                def prev_month(e):
                    nonlocal view_year, view_month
                    if view_month == 1:
                        view_month = 12
                        view_year -= 1
                    else:
                        view_month -= 1
                    render_view()
                    calendar_container.update()

                def next_month(e):
                    nonlocal view_year, view_month
                    if view_month == 12:
                        view_month = 1
                        view_year += 1
                    else:
                        view_month += 1
                    render_view()
                    calendar_container.update()

                month_btn = ft.Container(
                    content=ft.Text(
                        month_name,
                        size=14,
                        weight=ft.FontWeight.W_800,
                        color=self.colors.accent_primary,
                    ),
                    padding=ft.Padding.symmetric(horizontal=12, vertical=6),
                    border_radius=12,
                    bgcolor="#FFFFFF" if not self.colors.is_dark else self.colors.card_surface,
                    shadow=self.colors.subtle_shadow(depth=2, blur=4),
                    on_click=lambda e: set_view("months"),
                    tooltip="Pilih bulan",
                )

                year_btn = ft.Container(
                    content=ft.Text(
                        f"{view_year}",
                        size=14,
                        weight=ft.FontWeight.W_800,
                        color=self.colors.accent_primary,
                    ),
                    padding=ft.Padding.symmetric(horizontal=12, vertical=6),
                    border_radius=12,
                    bgcolor="#FFFFFF" if not self.colors.is_dark else self.colors.card_surface,
                    shadow=self.colors.subtle_shadow(depth=2, blur=4),
                    on_click=lambda e: set_view("years"),
                    tooltip="Pilih tahun",
                )

                prev_btn = NeumorphicButton(
                    icon=ft.Icons.CHEVRON_LEFT_ROUNDED,
                    colors=self.colors,
                    size=34,
                    icon_size=18,
                    icon_color=self.colors.text_primary,
                    bgcolor="#FFFFFF" if not self.colors.is_dark else self.colors.card_surface,
                    on_click=prev_month,
                    tooltip="Bulan sebelumnya",
                )
                next_btn = NeumorphicButton(
                    icon=ft.Icons.CHEVRON_RIGHT_ROUNDED,
                    colors=self.colors,
                    size=34,
                    icon_size=18,
                    icon_color=self.colors.text_primary,
                    bgcolor="#FFFFFF" if not self.colors.is_dark else self.colors.card_surface,
                    on_click=next_month,
                    tooltip="Bulan berikutnya",
                )

                header_row = ft.Row(
                    controls=[
                        prev_btn,
                        ft.Row(controls=[month_btn, year_btn], spacing=6),
                        next_btn,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                )

                header_card = NeumorphicCard(
                    content=header_row,
                    colors=self.colors,
                    padding=ft.Padding.symmetric(horizontal=10, vertical=7),
                    border_radius=16,
                    margin=ft.Margin.only(bottom=8),
                    elevated=False,
                )

                day_headers = [
                    ft.Container(
                        content=ft.Text(
                            d,
                            size=10,
                            weight=ft.FontWeight.W_700,
                            color=self.colors.text_secondary,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        width=34,
                        alignment=ft.Alignment(0, 0),
                    )
                    for d in DAY_NAMES_ID
                ]
                days_header_row = ft.Row(
                    controls=day_headers,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                )

                first_weekday = (datetime.date(view_year, view_month, 1).isoweekday() % 7)
                days_in_cur_month = calendar.monthrange(view_year, view_month)[1]

                if view_month == 1:
                    p_year, p_month = view_year - 1, 12
                else:
                    p_year, p_month = view_year, view_month - 1
                days_in_prev_month = calendar.monthrange(p_year, p_month)[1]

                cells = []
                for i in range(first_weekday - 1, -1, -1):
                    day_num = days_in_prev_month - i
                    cells.append(("prev", p_year, p_month, day_num))

                for day_num in range(1, days_in_cur_month + 1):
                    cells.append(("cur", view_year, view_month, day_num))

                if len(cells) % 7 != 0:
                    remaining = 7 - (len(cells) % 7)
                    if view_month == 12:
                        n_year, n_month = view_year + 1, 1
                    else:
                        n_year, n_month = view_year, view_month + 1
                    for day_num in range(1, remaining + 1):
                        cells.append(("next", n_year, n_month, day_num))

                grid_rows = []
                for r in range(0, len(cells), 7):
                    row_items = []
                    for cell_type, y, m, d in cells[r : r + 7]:
                        is_selected = (
                            self.selected_date.year == y
                            and self.selected_date.month == m
                            and self.selected_date.day == d
                        )

                        def make_click(target_y, target_m, target_d):
                            return lambda e: on_date_click(target_y, target_m, target_d)

                        if cell_type == "cur":
                            if is_selected:
                                cell_content = ft.Container(
                                    content=ft.Text(
                                        str(d),
                                        size=12,
                                        weight=ft.FontWeight.W_800,
                                        color="#FFFFFF",
                                    ),
                                    width=34,
                                    height=34,
                                    border_radius=17,
                                    bgcolor=self.colors.accent_primary,
                                    alignment=ft.Alignment(0, 0),
                                    shadow=[
                                        ft.BoxShadow(
                                            spread_radius=0,
                                            blur_radius=5,
                                            color=self.colors.accent_primary,
                                            offset=ft.Offset(0, 1),
                                        )
                                    ],
                                    on_click=make_click(y, m, d),
                                )
                            else:
                                cell_content = ft.Container(
                                    content=ft.Text(
                                        str(d),
                                        size=12,
                                        weight=ft.FontWeight.W_600,
                                        color=self.colors.text_primary,
                                    ),
                                    width=34,
                                    height=34,
                                    border_radius=17,
                                    bgcolor="#FFFFFF" if not self.colors.is_dark else self.colors.card_surface,
                                    alignment=ft.Alignment(0, 0),
                                    shadow=self.colors.subtle_shadow(depth=1, blur=3),
                                    on_click=make_click(y, m, d),
                                )
                        else:
                            cell_content = ft.Container(
                                content=ft.Text(
                                    str(d),
                                    size=12,
                                    weight=ft.FontWeight.W_400,
                                    color=self.colors.text_secondary,
                                    opacity=0.35,
                                ),
                                width=34,
                                height=34,
                                alignment=ft.Alignment(0, 0),
                                on_click=make_click(y, m, d),
                            )
                        row_items.append(cell_content)

                    grid_rows.append(
                        ft.Row(
                            controls=row_items,
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        )
                    )

                grid_column = ft.Column(
                    controls=grid_rows,
                    spacing=7,
                    tight=True,
                )

                today = datetime.date.today()
                today_btn = ft.Container(
                    content=ft.Text(
                        "Pilih Hari Ini",
                        size=12,
                        weight=ft.FontWeight.W_700,
                        color=self.colors.accent_primary,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    padding=ft.Padding.symmetric(vertical=8),
                    border_radius=12,
                    bgcolor="#FFFFFF" if not self.colors.is_dark else self.colors.card_surface,
                    alignment=ft.Alignment(0, 0),
                    shadow=self.colors.subtle_shadow(depth=1, blur=3),
                    margin=0,
                    on_click=lambda e: on_date_click(today.year, today.month, today.day),
                )

                calendar_container.content = ft.Column(
                    controls=[
                        header_card,
                        ft.Container(height=10),
                        days_header_row,
                        ft.Container(height=3),
                        grid_column,
                        ft.Container(height=18),
                        today_btn,
                    ],
                    spacing=0,
                    tight=True,
                )

        render_view()
        self.app_page.show_dialog(dialog)

    def _show_custom_time_dialog(self, label_ref: Optional[ft.Text] = None):
        """100% Bespoke Neumorphic Circular Clock Dialog (Jam Bulat).
        - Digital mode toggle between Jam (Hour) & Menit (Minute)
        - AM/PM toggle pill
        - Circular recessed Neumorphic dial dish with 12 radial positions
        - Hour mode: quick tap switches to Minute mode automatically
        - Minute mode: 5-minute clock positions + fine-tuning steppers (-1m, +1m)
        - Soft dual opposing shadows & theme color fidelity
        """
        parts = self.selected_time.split(":")
        try:
            curr_h = int(parts[0]) if len(parts) > 0 else 12
            curr_m = int(parts[1]) if len(parts) > 1 else 0
        except Exception:
            curr_h, curr_m = 12, 0

        active_mode = "hour"
        dial_hour = curr_h
        dial_minute = curr_m
        is_pm = dial_hour >= 12

        time_container = ft.Container(
            width=290,
            padding=0,
        )

        time_card = NeumorphicCard(
            content=time_container,
            colors=self.colors,
            padding=ft.Padding.only(left=14, right=14, top=14, bottom=14),
            border_radius=22,
            margin=0,
        )

        dialog = ft.AlertDialog(
            content=ft.Container(
                content=time_card,
                width=318,
                padding=0,
            ),
            content_padding=0,
            inset_padding=ft.Padding.symmetric(horizontal=12, vertical=20),
            bgcolor="transparent",
            shape=ft.RoundedRectangleBorder(radius=22),
        )

        def close_dialog(e=None):
            if hasattr(self.app_page, "pop_dialog"):
                self.app_page.pop_dialog()
            elif hasattr(self.app_page, "close"):
                self.app_page.close(dialog)
            else:
                dialog.open = False
            self.app_page.update()

        def confirm_time(e=None):
            self.selected_time = f"{dial_hour:02d}:{dial_minute:02d}"
            if label_ref:
                label_ref.value = self.selected_time
            close_dialog()
            self.update()

        def set_mode(mode: str):
            nonlocal active_mode
            active_mode = mode
            render_time_picker()
            time_container.update()

        def set_am_pm(pm: bool):
            nonlocal is_pm, dial_hour
            is_pm = pm
            if is_pm and dial_hour < 12:
                dial_hour += 12
            elif not is_pm and dial_hour >= 12:
                dial_hour -= 12
            render_time_picker()
            time_container.update()

        def step_minute(delta: int):
            nonlocal dial_minute
            dial_minute = (dial_minute + delta) % 60
            render_time_picker()
            time_container.update()

        def render_time_picker():
            nonlocal dial_hour, dial_minute, active_mode, is_pm

            # 1. Header Card
            close_btn = NeumorphicButton(
                icon=ft.Icons.CLOSE_ROUNDED,
                colors=self.colors,
                size=34,
                icon_size=16,
                icon_color=self.colors.text_secondary,
                bgcolor="#FFFFFF" if not self.colors.is_dark else self.colors.card_surface,
                on_click=close_dialog,
                tooltip="Tutup",
            )
            header_row = ft.Row(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.SCHEDULE_ROUNDED, size=18, color=self.colors.accent_primary),
                            ft.Text(
                                "Pilih Jam",
                                size=15,
                                weight=ft.FontWeight.W_800,
                                color=self.colors.text_primary if self.colors.is_dark else self.colors.accent_primary,
                            ),
                        ],
                        spacing=6,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    close_btn,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
            header_card = NeumorphicCard(
                content=header_row,
                colors=self.colors,
                padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                border_radius=16,
                margin=ft.Margin.only(bottom=6),
                elevated=False,
            )

            # 2. Digital Display Box (Hour : Minute + AM/PM)
            hour_active = (active_mode == "hour")
            minute_active = (active_mode == "minute")

            hour_box = ft.Container(
                content=ft.Text(
                    f"{dial_hour:02d}",
                    size=24,
                    weight=ft.FontWeight.W_800 if hour_active else ft.FontWeight.W_600,
                    color=self.colors.accent_primary if hour_active else self.colors.text_secondary,
                    text_align=ft.TextAlign.CENTER,
                ),
                width=66,
                height=50,
                border_radius=14,
                alignment=ft.Alignment(0, 0),
                bgcolor=self.colors.card_surface if hour_active else self.colors.pressed_surface,
                shadow=self.colors.subtle_shadow(depth=2, blur=4) if hour_active else self.colors.pressed_shadow(),
                on_click=lambda e: set_mode("hour"),
                tooltip="Atur jam",
            )

            colon_text = ft.Text(":", size=22, weight=ft.FontWeight.W_800, color=self.colors.accent_primary)

            minute_box = ft.Container(
                content=ft.Text(
                    f"{dial_minute:02d}",
                    size=24,
                    weight=ft.FontWeight.W_800 if minute_active else ft.FontWeight.W_600,
                    color=self.colors.accent_primary if minute_active else self.colors.text_secondary,
                    text_align=ft.TextAlign.CENTER,
                ),
                width=66,
                height=50,
                border_radius=14,
                alignment=ft.Alignment(0, 0),
                bgcolor=self.colors.card_surface if minute_active else self.colors.pressed_surface,
                shadow=self.colors.subtle_shadow(depth=2, blur=4) if minute_active else self.colors.pressed_shadow(),
                on_click=lambda e: set_mode("minute"),
                tooltip="Atur menit",
            )

            am_btn = ft.Container(
                content=ft.Text(
                    "AM",
                    size=11,
                    weight=ft.FontWeight.W_800 if not is_pm else ft.FontWeight.W_600,
                    color="#FFFFFF" if not is_pm else self.colors.text_secondary,
                    text_align=ft.TextAlign.CENTER,
                ),
                width=48,
                height=22,
                border_radius=8,
                alignment=ft.Alignment(0, 0),
                bgcolor=self.colors.accent_primary if not is_pm else "transparent",
                shadow=self.colors.subtle_shadow(depth=1, blur=2) if not is_pm else [],
                on_click=lambda e: set_am_pm(False),
            )

            pm_btn = ft.Container(
                content=ft.Text(
                    "PM",
                    size=11,
                    weight=ft.FontWeight.W_800 if is_pm else ft.FontWeight.W_600,
                    color="#FFFFFF" if is_pm else self.colors.text_secondary,
                    text_align=ft.TextAlign.CENTER,
                ),
                width=48,
                height=22,
                border_radius=8,
                alignment=ft.Alignment(0, 0),
                bgcolor=self.colors.accent_primary if is_pm else "transparent",
                shadow=self.colors.subtle_shadow(depth=1, blur=2) if is_pm else [],
                on_click=lambda e: set_am_pm(True),
            )

            ampm_pill = ft.Container(
                content=ft.Column(
                    controls=[am_btn, pm_btn],
                    spacing=2,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                width=56,
                height=50,
                border_radius=12,
                padding=3,
                bgcolor="#FFFFFF" if not self.colors.is_dark else self.colors.pressed_surface,
                shadow=self.colors.subtle_shadow(depth=1, blur=3) if not self.colors.is_dark else self.colors.pressed_shadow(),
                alignment=ft.Alignment(0, 0),
            )

            digital_row = ft.Row(
                controls=[
                    ft.Row(controls=[hour_box, colon_text, minute_box], spacing=6, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    ampm_pill,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )

            # 3. Circular Dial (Jam Bulat Neumorphic)
            dial_size = 186
            cx, cy = dial_size / 2, dial_size / 2
            R = 72  # Memberikan jarak renggang ~5px dari batas luar dial (wrap)
            dial_controls: List[ft.Control] = [
                ft.Container(
                    width=8,
                    height=8,
                    border_radius=4,
                    bgcolor=self.colors.accent_primary,
                    left=cx - 4,
                    top=cy - 4,
                )
            ]

            if active_mode == "hour":
                base_hours = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23] if is_pm else [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

                for idx, h_val in enumerate(base_hours):
                    angle_deg = idx * 30 - 90
                    angle_rad = math.radians(angle_deg)
                    px = cx + R * math.cos(angle_rad) - 16
                    py = cy + R * math.sin(angle_rad) - 16

                    is_sel = (dial_hour == h_val)

                    def make_hour_click(val):
                        return lambda e: on_select_hour(val)

                    btn = ft.Container(
                        content=ft.Text(
                            f"{h_val:02d}",
                            size=11.5,
                            weight=ft.FontWeight.W_800 if is_sel else ft.FontWeight.W_600,
                            color="#FFFFFF" if is_sel else self.colors.text_primary,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        width=32,
                        height=32,
                        border_radius=16,
                        left=px,
                        top=py,
                        alignment=ft.Alignment(0, 0),
                        bgcolor=self.colors.accent_primary if is_sel else ("#FFFFFF" if not self.colors.is_dark else self.colors.card_surface),
                        shadow=(
                            [ft.BoxShadow(spread_radius=0, blur_radius=5, color=self.colors.accent_primary, offset=ft.Offset(0, 1))]
                            if is_sel
                            else self.colors.subtle_shadow(depth=2, blur=4)
                        ),
                        on_click=make_hour_click(h_val),
                    )
                    dial_controls.append(btn)

                def on_select_hour(val: int):
                    nonlocal dial_hour, active_mode
                    dial_hour = val
                    active_mode = "minute"
                    render_time_picker()
                    time_container.update()

            else:
                minute_increments = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]

                for idx, m_val in enumerate(minute_increments):
                    angle_deg = idx * 30 - 90
                    angle_rad = math.radians(angle_deg)
                    px = cx + R * math.cos(angle_rad) - 16
                    py = cy + R * math.sin(angle_rad) - 16

                    is_sel = (dial_minute == m_val)

                    def make_min_click(val):
                        return lambda e: on_select_minute(val)

                    btn = ft.Container(
                        content=ft.Text(
                            f"{m_val:02d}",
                            size=11.5,
                            weight=ft.FontWeight.W_800 if is_sel else ft.FontWeight.W_600,
                            color="#FFFFFF" if is_sel else self.colors.text_primary,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        width=32,
                        height=32,
                        border_radius=16,
                        left=px,
                        top=py,
                        alignment=ft.Alignment(0, 0),
                        bgcolor=self.colors.accent_primary if is_sel else ("#FFFFFF" if not self.colors.is_dark else self.colors.card_surface),
                        shadow=(
                            [ft.BoxShadow(spread_radius=0, blur_radius=5, color=self.colors.accent_primary, offset=ft.Offset(0, 1))]
                            if is_sel
                            else self.colors.subtle_shadow(depth=2, blur=4)
                        ),
                        on_click=make_min_click(m_val),
                    )
                    dial_controls.append(btn)

                def on_select_minute(val: int):
                    nonlocal dial_minute
                    dial_minute = val
                    render_time_picker()
                    time_container.update()

            dial_stack = ft.Stack(
                controls=dial_controls,
                width=dial_size,
                height=dial_size,
            )

            dial_disc = ft.Container(
                content=dial_stack,
                width=dial_size,
                height=dial_size,
                border_radius=dial_size // 2,
                bgcolor="#FFFFFF" if not self.colors.is_dark else self.colors.card_surface,
                shadow=self.colors.subtle_shadow(depth=2, blur=6) if not self.colors.is_dark else self.colors.pressed_shadow(),
                alignment=ft.Alignment(0, 0),
            )

            def make_step_chip(label: str, delta: int):
                return ft.Container(
                    content=ft.Text(
                        label,
                        size=10.5,
                        weight=ft.FontWeight.W_600,
                        color=self.colors.accent_primary if not self.colors.is_dark else self.colors.text_primary,
                    ),
                    padding=ft.Padding.symmetric(horizontal=8, vertical=4),
                    border_radius=8,
                    bgcolor=self.colors.card_surface,
                    shadow=self.colors.subtle_shadow(depth=1, blur=2),
                    on_click=lambda e: step_minute(delta),
                )

            stepper_row = ft.Row(
                controls=[
                    make_step_chip("-5m", -5),
                    make_step_chip("-1m", -1),
                    ft.Text(f"{dial_minute:02d}m", size=11, weight=ft.FontWeight.W_700, color=self.colors.accent_primary),
                    make_step_chip("+1m", 1),
                    make_step_chip("+5m", 5),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=6,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )

            batal_btn = ft.Container(
                content=ft.Text(
                    "Batal",
                    size=12,
                    weight=ft.FontWeight.W_600,
                    color=self.colors.text_secondary,
                ),
                padding=ft.Padding.symmetric(horizontal=16, vertical=8),
                border_radius=12,
                bgcolor=self.colors.card_surface,
                shadow=self.colors.subtle_shadow(depth=1, blur=2),
                on_click=close_dialog,
            )

            confirm_btn = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.CHECK_ROUNDED, size=15, color="#FFFFFF"),
                        ft.Text(
                            "Pilih Jam",
                            size=12,
                            weight=ft.FontWeight.W_700,
                            color="#FFFFFF",
                        ),
                    ],
                    spacing=4,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                padding=ft.Padding.symmetric(horizontal=16, vertical=8),
                border_radius=12,
                bgcolor=self.colors.accent_primary,
                shadow=self.colors.subtle_shadow(depth=1, blur=3),
                on_click=confirm_time,
            )

            action_row = ft.Row(
                controls=[batal_btn, confirm_btn],
                alignment=ft.MainAxisAlignment.END,
                spacing=8,
            )

            time_container.content = ft.Column(
                controls=[
                    header_card,
                    ft.Container(height=4),
                    digital_row,
                    ft.Container(height=6),
                    ft.Row(controls=[dial_disc], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Container(height=4),
                    stepper_row,
                    ft.Container(height=6),
                    action_row,
                ],
                spacing=4,
                tight=True,
            )

        render_time_picker()
        self.app_page.show_dialog(dialog)

    def _build_content(self) -> ft.Control:
        diaries = self.data_manager.get_diaries()

        # 1. Header Card: Catatan Diary
        header_card = NeumorphicCard(
            content=ft.Row(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(
                                ft.Icons.AUTO_STORIES_ROUNDED,
                                size=20,
                                color=self.colors.accent_primary,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        "Catatan Diary",
                                        size=18,
                                        weight=ft.FontWeight.W_800,
                                        color=self.colors.text_primary if self.colors.is_dark else self.colors.accent_primary,
                                    ),
                                    ft.Text(
                                        "Refleksi & kedamaian pikiran",
                                        size=12,
                                        weight=ft.FontWeight.W_500,
                                        color=self.colors.text_secondary,
                                    ),
                                ],
                                spacing=2,
                            ),
                        ],
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    NeumorphicBadge(
                        text=f"{len(diaries)} Catatan",
                        colors=self.colors,
                        text_size=10,
                        bold=True,
                        elevated=True,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            colors=self.colors,
            padding=ft.Padding.symmetric(horizontal=16, vertical=12),
            border_radius=18,
            margin=ft.Margin.only(left=18, right=18, top=4, bottom=10),
            elevated=False,
        )

        # 2. Mood Options Row
        moods = ["Bersyukur", "Tenang", "Semangat", "Reflektif", "Santai"]
        mood_chips: List[ft.Control] = []
        for m in moods:
            is_active = self.selected_mood == m
            chip = ft.Container(
                content=ft.Text(
                    m,
                    size=10.5,
                    weight=ft.FontWeight.W_700 if is_active else ft.FontWeight.W_500,
                    color="#FFFFFF" if is_active and not self.colors.is_dark else ((self.colors.text_primary if is_active else self.colors.text_secondary) if self.colors.is_dark else self.colors.accent_primary),
                    no_wrap=True,
                ),
                padding=ft.Padding.symmetric(horizontal=6, vertical=4),
                border_radius=11,
                bgcolor=self.colors.accent_primary if is_active and not self.colors.is_dark else (self.colors.card_elevated if is_active else "transparent"),
                shadow=self.colors.subtle_shadow(depth=1, blur=3) if is_active else [],
                on_click=lambda e, mood_val=m: self._select_mood(mood_val),
                animate=ft.Animation(160, ft.AnimationCurve.EASE_OUT),
            )
            mood_chips.append(chip)

        mood_pill = ft.Container(
            content=ft.Row(
                controls=mood_chips,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor="#FFFFFF" if not self.colors.is_dark else self.colors.pressed_surface,
            border_radius=14,
            padding=ft.Padding.symmetric(horizontal=3, vertical=3),
            border=None,
            shadow=self.colors.subtle_shadow(depth=1, blur=2) if not self.colors.is_dark else self.colors.pressed_shadow(),
        )

        # 3. Writing Card Fields
        date_display_text = ft.Text(
            format_diary_date(self.selected_date.strftime("%Y-%m-%d")),
            size=12,
            weight=ft.FontWeight.W_600,
            color=self.colors.text_primary,
            no_wrap=True,
            overflow=ft.TextOverflow.ELLIPSIS,
            expand=True,
        )

        date_btn = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.CALENDAR_MONTH_ROUNDED, size=16, color=self.colors.accent_primary),
                    date_display_text,
                    ft.Icon(ft.Icons.ARROW_DROP_DOWN_ROUNDED, size=18, color=self.colors.text_secondary),
                ],
                spacing=6,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor="#FFFFFF" if not self.colors.is_dark else self.colors.card_surface,
            border_radius=14,
            padding=ft.Padding.symmetric(horizontal=12, vertical=10),
            shadow=self.colors.subtle_shadow(depth=1, blur=2),
            expand=True,
            on_click=lambda e: self._show_custom_calendar_dialog(date_display_text),
            tooltip="Pilih tanggal catatan",
        )

        time_display_text = ft.Text(
            self.selected_time,
            size=12,
            weight=ft.FontWeight.W_600,
            color=self.colors.text_primary,
            no_wrap=True,
        )

        time_btn = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.SCHEDULE_ROUNDED, size=16, color=self.colors.accent_primary),
                    time_display_text,
                    ft.Icon(ft.Icons.ARROW_DROP_DOWN_ROUNDED, size=16, color=self.colors.text_secondary),
                ],
                spacing=4,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            bgcolor="#FFFFFF" if not self.colors.is_dark else self.colors.card_surface,
            border_radius=14,
            padding=ft.Padding.symmetric(horizontal=8, vertical=10),
            shadow=self.colors.subtle_shadow(depth=1, blur=2),
            width=96,
            on_click=lambda e: self._show_custom_time_dialog(time_display_text),
            tooltip="Pilih jam catatan (jam bulat)",
        )

        date_time_row = ft.Row(
            controls=[date_btn, time_btn],
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        title_field = ft.TextField(
            hint_text="Judul catatan (opsional)...",
            hint_style=ft.TextStyle(size=13, color=self.colors.text_secondary),
            text_style=ft.TextStyle(size=13, weight=ft.FontWeight.W_600, color=self.colors.text_primary),
            border=ft.NoInputBorder() if hasattr(ft, "NoInputBorder") else None,
            cursor_color=self.colors.accent_primary,
            dense=True,
            content_padding=ft.Padding.symmetric(horizontal=14, vertical=10),
        )

        title_container = ft.Container(
            content=title_field,
            bgcolor="#FFFFFF" if not self.colors.is_dark else self.colors.pressed_surface,
            border_radius=14,
            border=None,
            shadow=self.colors.subtle_shadow(depth=1, blur=3) if not self.colors.is_dark else self.colors.pressed_shadow(),
        )

        content_field = ft.TextField(
            hint_text="Tuliskan apa yang kamu rasakan, syukuri, atau pelajari hari ini...",
            hint_style=ft.TextStyle(size=12.5, color=self.colors.text_secondary),
            text_style=ft.TextStyle(size=13, weight=ft.FontWeight.W_500, color=self.colors.text_primary),
            border=ft.NoInputBorder() if hasattr(ft, "NoInputBorder") else None,
            cursor_color=self.colors.accent_primary,
            multiline=True,
            min_lines=3,
            max_lines=6,
            dense=True,
            content_padding=ft.Padding.symmetric(horizontal=14, vertical=12),
        )

        content_container = ft.Container(
            content=content_field,
            bgcolor="#FFFFFF" if not self.colors.is_dark else self.colors.pressed_surface,
            border_radius=14,
            border=None,
            shadow=self.colors.subtle_shadow(depth=1, blur=3) if not self.colors.is_dark else self.colors.pressed_shadow(),
        )

        save_btn_content = ft.Row(
            controls=[
                ft.Icon(ft.Icons.CHECK_ROUNDED, size=16, color=self.colors.accent_primary),
                ft.Text(
                    "Simpan Catatan",
                    size=12.5,
                    weight=ft.FontWeight.W_700,
                    color=self.colors.text_primary if self.colors.is_dark else self.colors.accent_primary,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=6,
        )

        save_btn = ft.Container(
            content=save_btn_content,
            bgcolor="#FFFFFF" if not self.colors.is_dark else self.colors.card_elevated,
            border_radius=14,
            padding=ft.Padding.symmetric(horizontal=16, vertical=10),
            margin=ft.Margin.only(top=4, bottom=0),
            shadow=self.colors.subtle_shadow(depth=1, blur=2),
            alignment=ft.Alignment(0, 0),
            on_click=lambda e: self._save_diary(
                title_field.value or "",
                content_field.value or "",
            ),
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
        )

        write_card_content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.EDIT_NOTE_ROUNDED, size=16, color=self.colors.accent_primary),
                                ft.Text(
                                    "Tulis Diary Hari Ini",
                                    size=13.5,
                                    weight=ft.FontWeight.W_700,
                                    color=self.colors.text_primary if self.colors.is_dark else self.colors.accent_primary,
                                ),
                            ],
                            spacing=6,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        NeumorphicBadge(
                            text=format_diary_date(datetime.date.today().isoformat()),
                            colors=self.colors,
                            text_size=10,
                            bold=True,
                            elevated=True,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=2),
                mood_pill,
                ft.Container(height=2),
                date_time_row,
                ft.Container(height=2),
                title_container,
                ft.Container(height=2),
                content_container,
                ft.Container(height=2),
                save_btn,
            ],
            spacing=4,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

        write_card = NeumorphicCard(
            content=write_card_content,
            colors=self.colors,
            padding=14,
            border_radius=18,
            margin=ft.Margin.only(left=18, right=18, bottom=10),
        )

        # 4. Section Heading: Riwayat Catatan
        history_heading_content = ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.BOOKMARK_BORDER_ROUNDED,
                            size=15,
                            color=self.colors.accent_primary,
                        ),
                        ft.Text(
                            "Riwayat Catatan",
                            size=13,
                            weight=ft.FontWeight.W_700,
                            color=self.colors.text_primary if self.colors.is_dark else self.colors.accent_primary,
                        ),
                    ],
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                NeumorphicBadge(
                    text="Tersimpan",
                    colors=self.colors,
                    text_size=10,
                    bold=True,
                    elevated=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        history_heading_card = NeumorphicCard(
            content=history_heading_content,
            colors=self.colors,
            padding=ft.Padding.symmetric(horizontal=14, vertical=10),
            border_radius=16,
            margin=ft.Margin.only(left=18, right=18, top=0, bottom=10),
            elevated=False,
        )

        # 5. List of Saved Diaries
        diary_cards: List[ft.Control] = []
        if not diaries:
            empty_card = NeumorphicCard(
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.Icons.AUTO_STORIES_OUTLINED, size=32, color=self.colors.text_secondary),
                        ft.Container(height=4),
                        ft.Text(
                            "Belum ada catatan diary.",
                            size=13,
                            weight=ft.FontWeight.W_700,
                            color=self.colors.text_primary if self.colors.is_dark else self.colors.accent_primary,
                        ),
                        ft.Text(
                            "Tuliskan refleksi, rasa syukur, atau kejadian berkesan hari ini di atas.",
                            size=11.5,
                            color=self.colors.text_secondary,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2,
                ),
                colors=self.colors,
                padding=ft.Padding.symmetric(horizontal=16, vertical=20),
                border_radius=18,
                margin=ft.Margin.only(left=18, right=18, bottom=10),
            )
            diary_cards.append(empty_card)
        else:
            for d in diaries:
                d_id = d.get("id", "")
                d_title = d.get("title", "")
                d_content = d.get("content", "")
                d_mood = d.get("mood", "Bersyukur")
                d_date = d.get("date", "")
                d_created = d.get("created_at", "")
                time_str = d_created[11:16] if len(d_created) >= 16 else ""
                date_str = format_diary_date(d_date) if d_date else ""
                full_time = f"{date_str} · {time_str}" if time_str else date_str

                # Delete button (red trash icon)
                del_btn = ft.Container(
                    content=ft.Icon(
                        ft.Icons.DELETE_OUTLINE_ROUNDED,
                        size=16,
                        color="#EF4444",
                    ),
                    padding=4,
                    border_radius=8,
                    on_click=lambda e, target_id=d_id: self._delete_diary(target_id),
                    tooltip="Hapus catatan",
                )

                card_rows: List[ft.Control] = [
                    # Card Top Row: Mood Badge, Date, Delete
                    ft.Row(
                        controls=[
                            ft.Row(
                                controls=[
                                    NeumorphicBadge(
                                        text=d_mood,
                                        colors=self.colors,
                                        text_size=10,
                                        bold=True,
                                        elevated=True,
                                    ),
                                    ft.Text(
                                        full_time,
                                        size=11,
                                        weight=ft.FontWeight.W_500,
                                        color=self.colors.text_secondary,
                                    ),
                                ],
                                spacing=8,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            del_btn,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ]

                if d_title:
                    card_rows.append(ft.Container(height=2))
                    card_rows.append(
                        ft.Text(
                            d_title,
                            size=13.5,
                            weight=ft.FontWeight.W_700,
                            color=self.colors.text_primary,
                        )
                    )

                card_rows.append(ft.Container(height=4))

                # If note is long, truncate preview and provide Detail button for popup
                is_long = len(d_content) > 100 or ("\n" in d_content)
                if is_long:
                    card_rows.append(
                        ft.Text(
                            d_content,
                            size=12.5,
                            weight=ft.FontWeight.W_400,
                            color=self.colors.text_primary,
                            max_lines=3,
                            overflow=ft.TextOverflow.ELLIPSIS,
                            selectable=True,
                        )
                    )
                    detail_btn = ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.AUTO_STORIES_OUTLINED, size=13, color=self.colors.accent_primary),
                                ft.Text(
                                    "Baca Catatan Lengkap",
                                    size=11,
                                    weight=ft.FontWeight.W_700,
                                    color=self.colors.text_primary if self.colors.is_dark else self.colors.accent_primary,
                                ),
                                ft.Icon(ft.Icons.CHEVRON_RIGHT_ROUNDED, size=13, color=self.colors.accent_primary),
                            ],
                            spacing=4,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=ft.Padding.symmetric(horizontal=10, vertical=6),
                        border_radius=10,
                        bgcolor=self.colors.card_elevated if self.colors.is_dark else self.colors.card_surface,
                        shadow=self.colors.subtle_shadow(depth=1, blur=3),
                        on_click=lambda e, entry=d: self._show_diary_detail_dialog(entry),
                        tooltip="Buka popup catatan lengkap",
                    )
                    card_rows.append(ft.Container(height=4))
                    card_rows.append(
                        ft.Row(
                            controls=[detail_btn],
                            alignment=ft.MainAxisAlignment.END,
                        )
                    )
                else:
                    card_rows.append(
                        ft.Text(
                            d_content,
                            size=12.5,
                            weight=ft.FontWeight.W_400,
                            color=self.colors.text_primary,
                            selectable=True,
                        )
                    )

                item_card = NeumorphicCard(
                    content=ft.Column(controls=card_rows, spacing=2),
                    colors=self.colors,
                    padding=14,
                    border_radius=18,
                    margin=ft.Margin.only(left=18, right=18, bottom=10),
                )
                diary_cards.append(item_card)

        controls = [
            header_card,
            write_card,
            history_heading_card,
            *diary_cards,
            ft.Container(height=80),  # Safe bottom padding for floating navigation bar
        ]

        return ft.Column(
            controls=controls,
            spacing=0,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
