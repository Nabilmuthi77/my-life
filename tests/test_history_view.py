"""Unit tests for HistoryView helpers and activity feed formatting."""

import unittest
from components.history_view import format_activity_ts, extract_clean_activity_message, format_short_date, HistoryView
from core.theme import ThemeManager


class TestHistoryViewFormatting(unittest.TestCase):
    def test_format_activity_ts(self):
        # Full ISO with time
        self.assertEqual(format_activity_ts("2026-10-25T12:40:00"), "25 Okt · 12:40")
        # Midnight decay time (00:00) should cleanly show date only
        self.assertEqual(format_activity_ts("2026-10-25T00:00:00"), "25 Okt")
        self.assertEqual(format_activity_ts("2026-11-05T14:30:00"), "5 Nov · 14:30")
        # Date only
        self.assertEqual(format_activity_ts("2026-10-25"), "25 Okt")
        # Empty or invalid
        self.assertEqual(format_activity_ts(""), "")
        self.assertEqual(format_activity_ts("not-a-date"), "not-a-date")

    def test_extract_clean_activity_message(self):
        # Progress click message with em-dash
        self.assertEqual(
            extract_clean_activity_message("Prinsipal — Progres +1 (1/10)"),
            "Progres +1 (1/10)"
        )
        # Daily decay message with em-dash and date in parens
        self.assertEqual(
            extract_clean_activity_message("Pergantian hari (2026-10-25) — Semua skor berkurang 1"),
            "Semua skor berkurang 1"
        )
        # Point up message
        self.assertEqual(
            extract_clean_activity_message("Jiwa — Mendapat +1 poin (4/10)"),
            "Mendapat +1 poin (4/10)"
        )
        # Score down message
        self.assertEqual(
            extract_clean_activity_message("Raga — Poin -1 (3/10)"),
            "Poin -1 (3/10)"
        )
        # Hyphen fallback
        self.assertEqual(
            extract_clean_activity_message("Emosional - Progres +1 (2/10)"),
            "Progres +1 (2/10)"
        )
        # Arbitrary custom message without separator
        self.assertEqual(
            extract_clean_activity_message("Catatan aktivitas custom"),
            "Catatan aktivitas custom"
        )

    def test_history_view_activities_build(self):
        tm = ThemeManager("light")
        activities = [
            {
                "aspect": "prinsipal",
                "type": "progress_up",
                "message": "Prinsipal — Progres +1 (1/10)",
                "score": 0,
                "progress": 1,
                "timestamp": "2026-10-25T12:40:00",
            },
            {
                "aspect": "all",
                "type": "daily_decay",
                "message": "Pergantian hari (2026-10-25) — Semua skor berkurang 1",
                "score": None,
                "progress": None,
                "timestamp": "2026-10-25T00:00:00",
            },
        ]
        history_view = HistoryView(history_7d=[], activities=activities, colors=tm.colors)
        # Switch to tab 1 (Aktivitas Terbaru)
        history_view._switch_subtab(1)
        self.assertEqual(history_view.active_subtab, 1)
        # Ensure feed card builds without errors
        card = history_view._build_activity_feed_card()
        self.assertIsNotNone(card)


if __name__ == "__main__":
    unittest.main()
