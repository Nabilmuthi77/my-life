"""History & Analytics View component for My Life application.
Provides dedicated tabs matching reference design:
- Tab 0: 'Grafik 7 Hari' with full Y-axis chart and 'Ringkasan per hari'
- Tab 1: 'Aktivitas Terbaru' with chronological click stream and emblems
- Seamless view that never cuts off or clips content
"""

from typing import List, Dict, Any, Optional
import flet as ft
from core.constants import ASPECT_KEYS, ASPECT_DETAILS, STATUS_BAR_SPACER_HEIGHT
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


def format_activity_ts(ts: str) -> str:
    """Format timestamp into 'DD Mmm · HH:MM' or 'DD Mmm' in Indonesian."""
    if not ts:
        return ""
    months = ["", "Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agt", "Sep", "Okt", "Nov", "Des"]
    try:
        if "T" in ts:
            date_part, time_part = ts.split("T", 1)
            parts = date_part.split("-")
            if len(parts) == 3:
                day = int(parts[2])
                month_idx = int(parts[1])
                month_name = months[month_idx] if 1 <= month_idx <= 12 else str(month_idx)
                time_hm = time_part[:5]
                if time_hm == "00:00":
                    return f"{day} {month_name}"
                return f"{day} {month_name} · {time_hm}"
        elif len(ts) >= 10 and "-" in ts:
            parts = ts[:10].split("-")
            if len(parts) == 3:
                day = int(parts[2])
                month_idx = int(parts[1])
                month_name = months[month_idx] if 1 <= month_idx <= 12 else str(month_idx)
                return f"{day} {month_name}"
    except Exception:
        pass
    return ts[:16] if len(ts) >= 16 else ts


def extract_clean_activity_message(msg: str) -> str:
    """Extract clean concise description from activity message."""
    if not msg:
        return "+1 progres"
    clean = msg
    for sep in [" — ", " - ", " – "]:
        if sep in clean:
            parts = clean.split(sep, 1)
            if parts[1].strip():
                clean = parts[1].strip()
            break
    return clean


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
            padding=0,
            bgcolor=colors.bg_main,
            expand=True,
        )

    def _switch_subtab(self, idx: int):
        self.active_subtab = idx
        self.content = self._build_layout()
        try:
            self.update()
        except RuntimeError:
            pass

    def _build_layout(self) -> ft.Control:
        # 1. Header Segmented Control
        def make_tab_btn(label: str, icon_name: str, idx: int):
            is_active = self.active_subtab == idx
            bg = (self.colors.card_elevated if self.colors.is_dark else self.colors.accent_primary) if is_active else "transparent"
            text_col = (self.colors.text_primary if self.colors.is_dark else "#FFFFFF") if is_active else self.colors.text_secondary
            shadow = self.colors.subtle_shadow(depth=1, blur=3) if is_active else []

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
                opacity=1.0 if is_active else 0.7,
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
            bgcolor="#FFFFFF" if not self.colors.is_dark else self.colors.pressed_surface,
            border_radius=15,
            padding=3,
            margin=ft.Margin.only(left=18, right=18),
            border=None,
            shadow=self.colors.subtle_shadow(depth=1, blur=3) if not self.colors.is_dark else self.colors.pressed_shadow(),
        )

        active_content = self._build_active_subtab_content()

        return ft.Column(
            controls=[
                ft.Container(height=STATUS_BAR_SPACER_HEIGHT),  # Status bar clearance spacer
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

        header_card = NeumorphicCard(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text(
                                "Riwayat 7 Hari",
                                size=17,
                                weight=ft.FontWeight.W_800,
                                color=self.colors.text_primary if self.colors.is_dark else self.colors.accent_primary,
                            ),
                            ft.Text(
                                f"Rata-rata skor: {avg_7d:.1f} / 10",
                                size=12,
                                weight=ft.FontWeight.W_500,
                                color=self.colors.text_secondary,
                            ),
                        ],
                        spacing=2,
                    ),
                    NeumorphicBadge(
                        text=f"{avg_7d:.1f} / 10",
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

        summary_heading_content = ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.CALENDAR_MONTH_ROUNDED,
                            size=15,
                            color=self.colors.accent_primary,
                        ),
                        ft.Text(
                            "Ringkasan per hari",
                            size=13,
                            weight=ft.FontWeight.W_700,
                            color=self.colors.text_primary if self.colors.is_dark else self.colors.accent_primary,
                        ),
                    ],
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                NeumorphicBadge(
                    text="7 Hari",
                    colors=self.colors,
                    text_size=10,
                    bold=True,
                    elevated=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        summary_heading_card = NeumorphicCard(
            content=summary_heading_content,
            colors=self.colors,
            padding=ft.Padding.symmetric(horizontal=14, vertical=10),
            border_radius=16,
            margin=ft.Margin.only(left=18, right=18, top=0, bottom=10),
            elevated=False,
        )

        controls = [
            header_card,
            self._build_chart_card(),
            summary_heading_card,
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
        header_card = NeumorphicCard(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text(
                                "Aktivitas Terbaru",
                                size=17,
                                weight=ft.FontWeight.W_800,
                                color=self.colors.text_primary if self.colors.is_dark else self.colors.accent_primary,
                            ),
                            ft.Text(
                                "Langkah kecil menuju perbaikan.",
                                size=12,
                                weight=ft.FontWeight.W_500,
                                color=self.colors.text_secondary,
                            ),
                        ],
                        spacing=2,
                    ),
                    NeumorphicBadge(
                        text="Aktivitas",
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

        controls = [
            header_card,
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
                margin=ft.Margin.only(left=18, right=18, bottom=10),
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
                            border_radius=ft.BorderRadius(top_left=6, top_right=6, bottom_left=2, bottom_right=2),
                            shadow=[
                                ft.BoxShadow(
                                    spread_radius=0,
                                    blur_radius=3,
                                    color=self.colors.accent_primary,
                                    offset=ft.Offset(0, -1),
                                )
                            ] if self.colors.is_dark else None,
                            animate=ft.Animation(240, ft.AnimationCurve.EASE_OUT),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
                width=18,
                height=chart_height,
                bgcolor="#FFFFFF" if not self.colors.is_dark else self.colors.progress_track,
                border_radius=9,
                shadow=self.colors.subtle_shadow(depth=1, blur=2) if not self.colors.is_dark else self.colors.pressed_shadow(),
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
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
            margin=ft.Margin.only(left=18, right=18, bottom=10),
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
            margin=ft.Margin.only(left=18, right=18, bottom=10),
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
                margin=ft.Margin.only(left=18, right=18, bottom=10),
            )

        activity_rows: List[ft.Control] = []
        recent_acts = self.activities[:15]

        for idx, act in enumerate(recent_acts):
            asp = act.get("aspect", "jiwa")
            is_decay = (asp == "all" or act.get("type") == "daily_decay")

            if is_decay:
                title_text = "Pergantian Hari"
                icon_name = "UPDATE_ROUNDED"
                icon_color = "#F59E0B" if not self.colors.is_dark else "#FBBF24"
                icon_bg = "#FEF3C7" if not self.colors.is_dark else "#2E2310"
            else:
                asp_info = ASPECT_DETAILS.get(asp, {})
                title_text = asp_info.get("name", asp.capitalize())
                icon_name = asp_info.get("icon_name", "SPA_ROUNDED")
                icon_color = self.colors.get_aspect_icon_color(asp)
                icon_bg = self.colors.get_aspect_bg_color(asp)

            ts = act.get("timestamp", "")
            formatted_ts = format_activity_ts(ts)

            msg = act.get("message", "+1 progres")
            clean_desc = extract_clean_activity_message(msg)

            # Score badge logic: prioritize 'score' then fallback to 'score_after'
            score_val = act.get("score")
            if score_val is None:
                score_val = act.get("score_after")

            if score_val is not None:
                badge_text = f"{score_val}/10"
                badge_color = self.colors.text_primary
            elif is_decay:
                badge_text = "-1 Poin"
                badge_color = "#F43F5E" if not self.colors.is_dark else "#FB7185"
            else:
                badge_text = ""
                badge_color = self.colors.text_secondary

            emblem = ft.Container(
                content=ft.Icon(
                    getattr(ft.Icons, icon_name, ft.Icons.SPA_ROUNDED),
                    size=16,
                    color=icon_color,
                ),
                width=36,
                height=36,
                border_radius=18,
                bgcolor=icon_bg,
                alignment=ft.Alignment(0, 0),
            )

            # Line 1: Title (left) & Score / Result (right)
            line1_controls = [
                ft.Text(
                    title_text,
                    size=13,
                    weight=ft.FontWeight.W_700,
                    color=self.colors.text_primary,
                    expand=True,
                    overflow=ft.TextOverflow.ELLIPSIS,
                    max_lines=1,
                ),
            ]
            if badge_text:
                line1_controls.append(
                    ft.Text(
                        badge_text,
                        size=12,
                        weight=ft.FontWeight.W_700,
                        color=badge_color,
                    )
                )

            # Line 2: Action description (left) & Timestamp (right)
            line2_controls = [
                ft.Text(
                    clean_desc,
                    size=11,
                    color=self.colors.text_secondary,
                    expand=True,
                    overflow=ft.TextOverflow.ELLIPSIS,
                    max_lines=1,
                ),
            ]
            if formatted_ts:
                line2_controls.append(
                    ft.Text(
                        formatted_ts,
                        size=10,
                        color=self.colors.text_secondary,
                    )
                )

            info_col = ft.Column(
                controls=[
                    ft.Row(
                        controls=line1_controls,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls=line2_controls,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                spacing=3,
                expand=True,
            )

            row = ft.Container(
                content=ft.Row(
                    controls=[
                        emblem,
                        info_col,
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.Padding.symmetric(vertical=3),
            )
            activity_rows.append(row)
            if idx < len(recent_acts) - 1:
                activity_rows.append(
                    ft.Divider(height=1, thickness=0.8, color=self.colors.border_subtle)
                )

        return NeumorphicCard(
            content=ft.Column(controls=activity_rows, spacing=6),
            colors=self.colors,
            padding=14,
            border_radius=18,
            margin=ft.Margin.only(left=18, right=18, bottom=10),
        )
