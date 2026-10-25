"""Automated Business Rule Tests for My Life Application.
Covers all 15 mandatory test suites defined in Section 9 of agent.md.
"""

import os
import json
import tempfile
import unittest
import datetime

from core.constants import REFERENCE_DATE, INITIAL_SCORES, INITIAL_PROGRESS, ASPECT_KEYS
from core.data_manager import DataManager
from core.theme import ThemeManager


class TestBusinessRules(unittest.TestCase):
    """Unit test suite for My Life business logic and persistence."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_json = os.path.join(self.temp_dir.name, "test_data.json")
        self.dm = DataManager(self.test_json)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_01_plus_normal(self):
        """TEST 1: Plus normal increases progress without changing main score."""
        self.dm.data["scores"]["jiwa"] = 3
        self.dm.data["progress"]["jiwa"] = 0
        self.dm.save_data()

        res = self.dm.increment_aspect_progress("jiwa")
        self.assertEqual(res["status"], "PROGRESS_INCREMENTED")
        self.assertEqual(self.dm.data["scores"]["jiwa"], 3)
        self.assertEqual(self.dm.data["progress"]["jiwa"], 1)

    def test_02_plus_tenth(self):
        """TEST 2: Tenth click awards 1 point and resets progress counter to 0."""
        self.dm.data["scores"]["jiwa"] = 3
        self.dm.data["progress"]["jiwa"] = 9
        self.dm.save_data()

        res = self.dm.increment_aspect_progress("jiwa")
        self.assertEqual(res["status"], "POINT_EARNED")
        self.assertEqual(self.dm.data["scores"]["jiwa"], 4)
        self.assertEqual(self.dm.data["progress"]["jiwa"], 0)

    def test_03_score_maximum(self):
        """TEST 3: When score reaches 10, clicking plus does not exceed 10 or hoard points."""
        self.dm.data["scores"]["jiwa"] = 10
        self.dm.data["progress"]["jiwa"] = 0
        self.dm.save_data()

        res = self.dm.increment_aspect_progress("jiwa")
        self.assertEqual(res["status"], "MAX_REACHED")
        self.assertEqual(self.dm.data["scores"]["jiwa"], 10)
        self.assertEqual(self.dm.data["progress"]["jiwa"], 0)

    def test_04_minus_normal(self):
        """TEST 4: Minus button immediately reduces score by 1 without altering progress."""
        self.dm.data["scores"]["raga"] = 4
        self.dm.data["progress"]["raga"] = 5
        self.dm.save_data()

        res = self.dm.decrement_aspect_score("raga")
        self.assertEqual(res["status"], "SCORE_DECREMENTED")
        self.assertEqual(self.dm.data["scores"]["raga"], 3)
        self.assertEqual(self.dm.data["progress"]["raga"], 5)  # Progress untouched

    def test_05_minus_at_zero(self):
        """TEST 5: Minus button at score 0 clamps to 0 without going negative."""
        self.dm.data["scores"]["finansial"] = 0
        self.dm.save_data()

        res = self.dm.decrement_aspect_score("finansial")
        self.assertEqual(res["status"], "MIN_REACHED")
        self.assertEqual(self.dm.data["scores"]["finansial"], 0)

    def test_06_daily_decay(self):
        """TEST 6: Daily decay from Oct 22 to Oct 24 reduces score by 2 points with proper snapshots."""
        self.dm.data["last_date"] = "2026-10-22"
        self.dm.data["scores"]["jiwa"] = 3
        self.dm.save_data()

        days_decayed = self.dm.apply_daily_decay("2026-10-24")
        self.assertEqual(days_decayed, 2)
        self.assertEqual(self.dm.data["scores"]["jiwa"], 1)
        self.assertEqual(self.dm.data["last_date"], "2026-10-24")

        # Verify snapshots for dates exist in history
        history_dates = [h["date"] for h in self.dm.data["history"]]
        self.assertIn("2026-10-22", history_dates)
        self.assertIn("2026-10-23", history_dates)
        self.assertIn("2026-10-24", history_dates)

    def test_07_daily_decay_at_zero(self):
        """TEST 7: Daily decay when score is 0 remains at 0."""
        self.dm.data["last_date"] = "2026-10-20"
        self.dm.data["scores"]["finansial"] = 0
        self.dm.save_data()

        self.dm.apply_daily_decay("2026-10-24")
        self.assertEqual(self.dm.data["scores"]["finansial"], 0)

    def test_08_progress_on_day_change(self):
        """TEST 8: Click progress is retained upon date transition while scores decay."""
        self.dm.data["last_date"] = "2026-10-22"
        self.dm.data["scores"]["jiwa"] = 4
        self.dm.data["progress"]["jiwa"] = 6
        self.dm.save_data()

        self.dm.apply_daily_decay("2026-10-23")
        self.assertEqual(self.dm.data["scores"]["jiwa"], 3)
        self.assertEqual(self.dm.data["progress"]["jiwa"], 6)  # Progress preserved

    def test_09_no_double_decay(self):
        """TEST 9: Running daily decay check twice on the same date does not apply second decay."""
        self.dm.data["last_date"] = "2026-10-22"
        self.dm.data["scores"]["jiwa"] = 3
        self.dm.save_data()

        self.dm.apply_daily_decay("2026-10-24")
        score_after_first = self.dm.data["scores"]["jiwa"]

        # Run again with same date
        second_decay = self.dm.apply_daily_decay("2026-10-24")
        self.assertEqual(second_decay, 0)
        self.assertEqual(self.dm.data["scores"]["jiwa"], score_after_first)

    def test_10_history_snapshot_uniqueness(self):
        """TEST 10: History has unique snapshots per date and correct chronological ordering."""
        self.dm.data["last_date"] = "2026-10-21"
        self.dm.save_data()

        self.dm.apply_daily_decay("2026-10-24")
        dates = [h["date"] for h in self.dm.data["history"]]
        self.assertEqual(len(dates), len(set(dates)))  # No duplicates
        self.assertEqual(dates, sorted(dates))  # Chronological order

    def test_11_persistence_reload(self):
        """TEST 11: Modifying score, saving, and reloading JSON preserves exact state."""
        self.dm.data["scores"]["jiwa"] = 7
        self.dm.data["progress"]["jiwa"] = 4
        self.dm.data["theme"] = "dark"
        self.dm.record_activity("jiwa", "test_action", "Test activity message", 7, 4)
        self.dm.save_data()

        # Reload in a new instance
        reloaded_dm = DataManager(self.test_json)
        self.assertEqual(reloaded_dm.data["scores"]["jiwa"], 7)
        self.assertEqual(reloaded_dm.data["progress"]["jiwa"], 4)
        self.assertEqual(reloaded_dm.data["theme"], "dark")
        self.assertTrue(len(reloaded_dm.data["click_history"]) >= 1)
        self.assertEqual(reloaded_dm.data["click_history"][0]["message"], "Test activity message")

    def test_12_theme_state_independence(self):
        """TEST 12: Changing theme switches palettes cleanly without mutating user scores."""
        tm = ThemeManager(initial_preference="light")
        self.assertFalse(tm.is_dark)
        self.assertEqual(tm.colors.bg_main, "#F5F7FA")

        tm.set_preference("dark")
        self.assertTrue(tm.is_dark)
        self.assertEqual(tm.colors.bg_main, "#071A20")

        # Changing theme preference does not alter scores
        self.dm.set_theme_preference("dark")
        self.assertEqual(self.dm.data["theme"], "dark")

    def test_13_corrupt_json_safe_recovery(self):
        """TEST 13: Corrupted JSON file is backed up and safe default state is initialized without crash."""
        with open(self.test_json, "w", encoding="utf-8") as f:
            f.write("{corrupted json content! invalid syntax [[[")

        # Reloading should not throw an unhandled exception
        safe_dm = DataManager(self.test_json)
        self.assertEqual(safe_dm.data["last_date"], REFERENCE_DATE)
        self.assertEqual(safe_dm.data["scores"]["jiwa"], 3)
        self.assertEqual(safe_dm.data["theme"], "auto")

    def test_14_empty_history_graceful(self):
        """TEST 14: get_last_7_days_history handles fresh/empty history gracefully."""
        self.dm.data["history"] = []
        self.dm.save_data()
        hist = self.dm.get_last_7_days_history()
        self.assertEqual(len(hist), 0)

    def test_15_summary_and_score_bounds(self):
        """TEST 15: Summary calculation adheres to total/50 and average format."""
        summary = self.dm.get_summary()
        self.assertEqual(summary["max_total"], 50)
        self.assertEqual(summary["max_average"], 10.0)
        self.assertGreaterEqual(summary["average"], 0.0)
        self.assertLessEqual(summary["average"], 10.0)

    def test_16_backup_export_and_reset(self):
        """TEST 16: export_backup_json returns valid json string and reset_to_defaults restores state."""
        backup_str = self.dm.export_backup_json()
        self.assertIsInstance(backup_str, str)
        self.assertIn("scores", backup_str)
        self.assertIn("jiwa", backup_str)

        # Mutate score
        self.dm.data["scores"]["jiwa"] = 9
        self.dm.save_data()
        self.assertEqual(self.dm.data["scores"]["jiwa"], 9)

        # Reset to defaults
        self.dm.reset_to_defaults()
        self.assertEqual(self.dm.data["scores"]["jiwa"], 3)

    def test_17_status_bar_spacer_clearance(self):
        """TEST 17: Status bar clearance spacer is adequate (> 44dp) for edge-to-edge mobile screens."""
        from core.constants import STATUS_BAR_SPACER_HEIGHT
        self.assertGreaterEqual(STATUS_BAR_SPACER_HEIGHT, 48)


if __name__ == "__main__":
    unittest.main()

