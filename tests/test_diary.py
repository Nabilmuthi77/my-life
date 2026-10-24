"""Tests for Diary functionality in DataManager."""

import os
import unittest
import tempfile
import shutil
from core.data_manager import DataManager


class TestDiaryOperations(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_json = os.path.join(self.test_dir, "test_data.json")
        self.dm = DataManager(self.test_json)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_diary_add_and_get(self):
        diaries = self.dm.get_diaries()
        self.assertEqual(len(diaries), 0)

        entry = self.dm.add_diary(
            title="Refleksi Hari Ini",
            content="Hari ini bersyukur bisa belajar banyak hal baru.",
            mood="Bersyukur",
        )
        self.assertIn("id", entry)
        self.assertEqual(entry["title"], "Refleksi Hari Ini")
        self.assertEqual(entry["mood"], "Bersyukur")

        diaries_after = self.dm.get_diaries()
        self.assertEqual(len(diaries_after), 1)
        self.assertEqual(diaries_after[0]["id"], entry["id"])

    def test_diary_delete(self):
        entry1 = self.dm.add_diary("Catatan 1", "Isi catatan 1", "Tenang")
        entry2 = self.dm.add_diary("Catatan 2", "Isi catatan 2", "Semangat")
        self.assertEqual(len(self.dm.get_diaries()), 2)

        deleted = self.dm.delete_diary(entry1["id"])
        self.assertTrue(deleted)
        self.assertEqual(len(self.dm.get_diaries()), 1)
        self.assertEqual(self.dm.get_diaries()[0]["id"], entry2["id"])

    def test_diary_persistence(self):
        self.dm.add_diary("Catatan Persisten", "Tersimpan di JSON", "Reflektif")

        # Reload new DataManager instance from same file
        reloaded_dm = DataManager(self.test_json)
        diaries = reloaded_dm.get_diaries()
        self.assertEqual(len(diaries), 1)
        self.assertEqual(diaries[0]["title"], "Catatan Persisten")
        self.assertEqual(diaries[0]["content"], "Tersimpan di JSON")
        self.assertEqual(diaries[0]["mood"], "Reflektif")

    def test_diary_view_snack_compatibility(self):
        from components.diary_view import DiaryView
        from core.theme import ThemeColors
        import flet as ft

        class MockPage:
            def __init__(self):
                self.dialog_shown = None

            def show_dialog(self, dialog):
                self.dialog_shown = dialog

        mock_page = MockPage()
        colors = ThemeColors(is_dark=True)
        view = DiaryView(page=mock_page, colors=colors, data_manager=self.dm)
        
    def test_diary_custom_date_and_time(self):
        entry = self.dm.add_diary(
            title="Catatan Kemarin",
            content="Mencatat peristiwa yang terjadi kemarin sore.",
            mood="Tenang",
            custom_date="2026-10-23",
            custom_time="16:30",
        )
        self.assertEqual(entry["date"], "2026-10-23")
        self.assertEqual(entry["created_at"], "2026-10-23 16:30")

    def test_diary_detail_dialog(self):
        from components.diary_view import DiaryView
        from core.theme import ThemeColors
        import flet as ft

        class MockPage:
            def __init__(self):
                self.dialog_shown = None

            def show_dialog(self, dialog):
                self.dialog_shown = dialog

            def pop_dialog(self):
                self.dialog_shown = None

        mock_page = MockPage()
        colors = ThemeColors(is_dark=True)
        view = DiaryView(page=mock_page, colors=colors, data_manager=self.dm)

        entry = {
            "id": "d_123",
            "title": "Catatan Panjang",
            "content": "Ini adalah teks catatan yang sangat panjang untuk testing popup dialog.",
            "mood": "Bersyukur",
            "date": "2026-10-24",
            "created_at": "2026-10-24 17:05",
        }
        view._show_diary_detail_dialog(entry)
        self.assertIsNotNone(mock_page.dialog_shown)
        self.assertIsInstance(mock_page.dialog_shown, ft.AlertDialog)

    def test_custom_calendar_dialog(self):
        from components.diary_view import DiaryView
        from core.theme import ThemeColors
        import flet as ft

        class MockPage:
            def __init__(self):
                self.dialog_shown = None

            def show_dialog(self, dialog):
                self.dialog_shown = dialog

            def pop_dialog(self):
                self.dialog_shown = None

        mock_page = MockPage()
        colors = ThemeColors(is_dark=True)
        view = DiaryView(page=mock_page, colors=colors, data_manager=self.dm)

        lbl = ft.Text("Tanggal")
        view._show_custom_calendar_dialog(lbl)
        self.assertIsNotNone(mock_page.dialog_shown)
        self.assertIsInstance(mock_page.dialog_shown, ft.AlertDialog)

    def test_custom_time_dialog(self):
        from components.diary_view import DiaryView
        from core.theme import ThemeColors
        import flet as ft

        class MockPage:
            def __init__(self):
                self.dialog_shown = None

            def show_dialog(self, dialog):
                self.dialog_shown = dialog

            def pop_dialog(self):
                self.dialog_shown = None

            def update(self):
                pass

        mock_page = MockPage()
        colors = ThemeColors(is_dark=True)
        view = DiaryView(page=mock_page, colors=colors, data_manager=self.dm)

        lbl = ft.Text("17:33")
        view._show_custom_time_dialog(lbl)
        self.assertIsNotNone(mock_page.dialog_shown)
        self.assertIsInstance(mock_page.dialog_shown, ft.AlertDialog)


if __name__ == "__main__":
    unittest.main()


