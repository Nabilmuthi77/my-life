"""History & Analytics View component for My Life application.
Provides dedicated tabs matching reference design:
- Tab 0: 'Grafik 7 Hari' with full Y-axis chart and 'Ringkasan per hari'
- Tab 1: 'Aktivitas Terbaru' with chronological click stream and emblems
- Seamless view that never cuts off or clips content
"""

from typing import List, Dict, Any, Optional
import flet as ft
from core.constants import ASPECT_KEYS, ASPECT_DETAILS
from core.theme import ThemeColors
from components.neumorphic import NeumorphicCard, NeumorphicBadge


def format_short_date(date_str: str) -> str:
    """Format 'YYYY-MM-DD' into 'DD Mmm YYYY' in Indonesian."""
    months = ["", "Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agt", "Sep", "Okt", "Nov", "Des"]
    parts = date_str.split("-")
    if len(parts) == 3:
        try:
            day = int(parts[2])
            month_idx = int(parts[1])
            year = parts[0]
            return f"{day} {months[month_idx]} {year}"
        except Exception:
            return date_str
    return date_str


class HistoryView(ft.Container):
    """View displaying 7-day chart, daily breakdown, and recent activities."""

    def __init__(
        self,
        history_7d: List[Dict[str, Any]],
        activities: List[Dict[str, Any]],
        colors: ThemeColors,
        on_refresh: Optional[Any] = None,
    ):
        self.history_7d = history_7d
        self.activities = activities
        self.colors = colors
        self.active_subtab = 0  # 0: Grafik & Ringkasan, 1: Aktivitas Terbaru
        self.content_holder = ft.Container(expand=True)

        super().__init__(
            content=self._build_layout(),
            padding=ft.Padding.only(left=18, right=18, top=36, bottom=0),
            expand=True,
        )

    def _switch_subtab(self, idx: int):
        self.active_subtab = idx
        self.content = self._build_layout()
        self.update()

    def _build_layout(self) -> ft.Control:
        # 1. Header Segmented Control
        def make_tab_btn(label: str, icon_name: str, idx: int):
            is_active = self.active_subtab == idx
            bg = (self.colors.card_elevated if self.colors.is_dark else "#FFFFFF") if is_active else "transparent"
            text_col = self.colors.accent_primary
            shadow = self.colors.subtle_shadow(depth=1, blur=4) if is_active else []

            return ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(getattr(ft.Icons, icon_name), size=15, color=text_col),
                        ft.Text(label, size=12, weight=ft.FontWeight.W_700 if is_active else ft.FontWeight.W_500, color=text_col),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5,
                ),
                padding=ft.Padding.symmetric(vertical=8, horizontal=10),
                border_radius=12,
                bgcolor=bg,
                shadow=shadow,
                opacity=1.0 if is_active else 0.6,
                expand=True,
                animate=ft.Animation(160, ft.AnimationCurve.EASE_OUT),
                on_click=lambda e, i=idx: self._switch_subtab(i),
            )

        segment_pill = ft.Container(
            content=ft.Row(
                controls=[
                    make_tab_btn("Grafik 7 Hari", "BAR_CHART_ROUNDED", 0),
                    make_tab_btn("Aktivitas Terbaru", "BOLT_ROUNDED", 1),
                ],
                spacing=4,
            ),
            bgcolor=self.colors.pressed_surface,
            border_radius=15,
            padding=3,
            shadow=self.colors.pressed_shadow(),
        )

        active_content = self._build_active_subtab_content()

        return ft.Column(
            controls=[
                segment_pill,
                ft.Container(height=8),
                active_content,
            ],
            spacing=0,
            expand=True,
        )

    def _build_active_subtab_content(self) -> ft.Control:
        if self.active_subtab == 0:
            return self._build_graph_tab()
        else:
            return self._build_activities_tab()

    def _build_graph_tab(self) -> ft.Control:
        # Calculate overall 7-day average
        if self.history_7d:
            avg_sum = sum(float(item.get("average", 0.0)) for item in self.history_7d)
            avg_7d = avg_sum / len(self.history_7d)
        else:
            avg_7d = 0.0

        header_section = ft.Column(
            controls=[
                ft.Text(
                    "Riwayat 7 Hari",
                    size=22,
                    weight=ft.FontWeight.W_800,
                    color=self.colors.accent_primary,
                ),
                ft.Text(
                    f"Rata-rata skor: {avg_7d:.1f} / 10",
                    size=13,
                    weight=ft.FontWeight.W_500,
                    color=self.colors.text_secondary,
                ),
            ],
            spacing=2,
        )

        controls = [
            header_section,
            ft.Container(height=8),
            self._build_chart_card(),
            ft.Container(height=12),
            ft.Text(
                "Ringkasan per hari",
                size=15,
                weight=ft.FontWeight.W_700,
                color=self.colors.accent_primary,
            ),
            ft.Container(height=2),
            self._build_daily_summary_card(),
            ft.Container(height=80),  # Safe bottom padding for floating nav bar
        ]

        return ft.Column(
            controls=controls,
            spacing=0,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )

    def _build_activities_tab(self) -> ft.Control:
        header_section = ft.Column(
            controls=[
                ft.Text(
                    "Aktivitas Terbaru",
                    size=22,
                    weight=ft.FontWeight.W_800,
                    color=self.colors.accent_primary,
                ),
                ft.Text(
                    "Setiap klik adalah langkah kecil menuju perbaikan.",
                    size=13,
                    weight=ft.FontWeight.W_500,
                    color=self.colors.text_secondary,
                ),
            ],
            spacing=2,
        )

        controls = [
            header_section,
            ft.Container(height=10),
            self._build_activity_feed_card(),
            ft.Container(height=80),  # Safe bottom padding for floating nav bar
        ]

        return ft.Column(
            controls=controls,
            spacing=0,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )

    def _build_chart_card(self) -> ft.Control:
        """7-Day Neumorphic Bar Chart with complete Y-axis and glowing rounded bars."""
        if not self.history_7d:
            return NeumorphicCard(
                content=ft.Container(
                    content=ft.Text("Belum ada data riwayat.", size=12, italic=True, color=self.colors.text_secondary),
                    padding=16,
                    alignment=ft.Alignment(0, 0),
                ),
                colors=self.colors,
            )

        chart_height = 105
        bars_controls: List[ft.Control] = []

        # Complete Y-Axis column (10, 8, 6, 4, 2, 0)
        y_axis = ft.Column(
            controls=[
                ft.Text(f"{n}", size=9, color=self.colors.text_secondary)
                for n in [10, 8, 6, 4, 2, 0]
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            height=chart_height,
        )

        for item in self.history_7d[-7:]:
            avg = float(item.get("average", 0.0))
            d_str = item.get("date", "")
            parts = d_str.split("-")
            date_label = f"{parts[2]}/{parts[1]}" if len(parts) == 3 else d_str

            fill_h = max(5, int((avg / 10.0) * chart_height))
            bar_color = self.colors.accent_primary

            bar_elem = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            height=fill_h,
                            bgcolor=bar_color,
                            border_radius=ft.BorderRadius(top_left=5, top_right=5, bottom_left=2, bottom_right=2),
                            shadow=[
                                ft.BoxShadow(
                                    spread_radius=0,
                                    blur_radius=4,
                                    color=self.colors.accent_primary if self.colors.is_dark else "#C8D3E0",
                                    offset=ft.Offset(0, -1),
                                )
                            ],
                            animate=ft.Animation(240, ft.AnimationCurve.EASE_OUT),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
                width=18,
                height=chart_height,
                bgcolor=self.colors.progress_track,
                border_radius=ft.BorderRadius(top_left=6, top_right=6, bottom_left=3, bottom_right=3),
                shadow=self.colors.pressed_shadow(),
                border=None,
            )

            col = ft.Column(
                controls=[
                    bar_elem,
                    ft.Text(date_label, size=9, color=self.colors.text_secondary),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            )
            bars_controls.append(col)

        chart_row = ft.Row(
            controls=[
                y_axis,
                ft.Container(width=6),
                ft.Row(
                    controls=bars_controls,
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    vertical_alignment=ft.CrossAxisAlignment.END,
                    expand=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

        return NeumorphicCard(
            content=chart_row,
            colors=self.colors,
            padding=14,
            border_radius=18,
            elevated=True,
        )

    def _build_daily_summary_card(self) -> ft.Control:
        """Build 'Ringkasan per hari' rows matching Screen 4 of mockup."""
        if not self.history_7d:
            return ft.Text("Belum ada ringkasan.", size=12, color=self.colors.text_secondary)

        rows: List[ft.Control] = []
        reversed_history = list(reversed(self.history_7d[-7:]))

        for idx, item in enumerate(reversed_history):
            d_str = item.get("date", "")
            formatted_date = format_short_date(d_str)
            avg = float(item.get("average", 0.0))

            row = ft.Row(
                controls=[
                    ft.Text(
                        formatted_date,
                        size=13,
                        weight=ft.FontWeight.W_500,
                        color=self.colors.text_primary,
                    ),
                    ft.Text(
                        f"{avg:.1f}",
                        size=13,
                        weight=ft.FontWeight.W_700,
                        color=self.colors.text_primary,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
            rows.append(row)
            if idx < len(reversed_history) - 1:
                rows.append(ft.Divider(height=1, thickness=0.8, color=self.colors.border_subtle))

        return NeumorphicCard(
            content=ft.Column(controls=rows, spacing=8),
            colors=self.colors,
            padding=14,
            border_radius=18,
        )

    def _build_activity_feed_card(self) -> ft.Control:
        """Build 'Aktivitas Terbaru' feed matching Screen 5 of reference mockup."""
        if not self.activities:
            return NeumorphicCard(
                content=ft.Container(
                    content=ft.Text(
                        "Belum ada aktivitas klik hari ini.",
                        size=12,
                        color=self.colors.text_secondary,
                        italic=True,
                    ),
                    padding=16,
                    alignment=ft.Alignment(0, 0),
                ),
                colors=self.colors,
            )

        activity_rows: List[ft.Control] = []
        recent_acts = self.activities[:15]

        for idx, act in enumerate(recent_acts):
            asp = act.get("aspect", "jiwa")
            asp_info = ASPECT_DETAILS.get(asp, {})
            icon_name = asp_info.get("icon_name", "SPA_ROUNDED")
            icon_color = self.colors.get_aspect_icon_color(asp)
            icon_bg = self.colors.get_aspect_bg_color(asp)

            ts = act.get("timestamp", "")
            time_part = ts[11:16] if len(ts) >= 16 else ""
            date_part = ts[8:10] if len(ts) >= 10 else ""
            formatted_ts = f"{date_part} Okt · {time_part}" if date_part else ts[:16]

            msg = act.get("message", "+1 progres")
            score_after = act.get("score_after", 0)

            emblem = ft.Container(
                content=ft.Icon(
                    getattr(ft.Icons, icon_name, ft.Icons.SPA_ROUNDED),
                    size=16,
                    color=icon_color,
                ),
                width=34,
                height=34,
                border_radius=17,
                bgcolor=icon_bg,
                alignment=ft.Alignment(0, 0),
            )

            info_col = ft.Column(
                controls=[
                    ft.Text(
                        asp_info.get("name", asp.capitalize()),
                        size=13,
                        weight=ft.FontWeight.W_700,
                        color=self.colors.text_primary,
                    ),
                    ft.Row(
                        controls=[
                            ft.Text(msg, size=11, color=self.colors.text_secondary),
                            ft.Text(f"· {formatted_ts}", size=10, color=self.colors.text_secondary),
                        ],
                        spacing=4,
                    ),
                ],
                spacing=1,
                expand=True,
            )

            score_badge = ft.Text(
                f"{score_after}/10",
                size=12,
                weight=ft.FontWeight.W_700,
                color=self.colors.text_primary,
            )

            row = ft.Row(
                controls=[
                    emblem,
                    info_col,
                    score_badge,
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
            activity_rows.append(row)
            if idx < len(recent_acts) - 1:
                activity_rows.append(ft.Divider(height=1, thickness=0.8, color=self.colors.border_subtle))

        return NeumorphicCard(
            content=ft.Column(controls=activity_rows, spacing=8),
            colors=self.colors,
            padding=14,
            border_radius=18,
        )
