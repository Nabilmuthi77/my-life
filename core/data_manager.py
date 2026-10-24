"""Local JSON Data Manager for My Life application.
Handles atomic file operations, data integrity validation, daily decay,
click progress counting, and history snapshots.
"""

import os
import json
import datetime
from typing import Dict, Any, List, Optional
from core.constants import (
    REFERENCE_DATE,
    INITIAL_SCORES,
    INITIAL_PROGRESS,
    ASPECT_KEYS,
    ASPECT_DETAILS,
    MAX_SCORE,
    MIN_SCORE,
    CLICKS_PER_POINT,
    MAX_CLICK_HISTORY,
)


def get_default_storage_path(filename: str = "my_life_data.json") -> str:
    """Resolve a secure, writable file path for local JSON storage.
    Compatible with Android APK storage and Desktop/Dev environments.
    """
    candidates = []
    # 1. Android / Flet app storage environment
    flet_storage = os.environ.get("FLET_APP_STORAGE")
    if flet_storage and os.path.isdir(flet_storage):
        candidates.append(os.path.join(flet_storage, filename))

    # 2. Android home or app-specific files directory
    home_dir = os.path.expanduser("~")
    if home_dir and os.path.isdir(home_dir):
        # On Android, home is usually inside /data/user/0/package_name/files
        app_sub = os.path.join(home_dir, ".mylife")
        try:
            os.makedirs(app_sub, exist_ok=True)
            candidates.append(os.path.join(app_sub, filename))
        except Exception:
            candidates.append(os.path.join(home_dir, filename))

    # 3. Current working directory / local project dir
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    candidates.append(os.path.join(base_dir, filename))

    # Pick the first writable location
    for path in candidates:
        try:
            parent = os.path.dirname(path)
            if parent:
                os.makedirs(parent, exist_ok=True)
            # Test write
            test_file = path + ".writetest"
            with open(test_file, "w", encoding="utf-8") as f:
                f.write("ok")
            os.remove(test_file)
            return path
        except Exception:
            continue

    # Fallback
    return filename


class DataManager:
    """Manages application state with local JSON persistence."""

    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path or get_default_storage_path()
        self.data: Dict[str, Any] = {}
        self.load_data()

    def get_initial_dataset(self) -> Dict[str, Any]:
        """Produce the initial dataset based on reference date (2026-10-22)."""
        return {
            "schema_version": 1,
            "last_date": REFERENCE_DATE,
            "scores": dict(INITIAL_SCORES),
            "progress": dict(INITIAL_PROGRESS),
            "history": [
                {
                    "date": REFERENCE_DATE,
                    **dict(INITIAL_SCORES),
                    "total": sum(INITIAL_SCORES.values()),
                    "average": round(sum(INITIAL_SCORES.values()) / len(ASPECT_KEYS), 1),
                }
            ],
            "click_history": [],
            "theme": "auto",
        }

    def validate_and_repair_data(self, raw: Any) -> Dict[str, Any]:
        """Validate structure and clamp values into acceptable ranges."""
        default = self.get_initial_dataset()
        if not isinstance(raw, dict):
            return default

        # Validate schema_version
        schema_version = raw.get("schema_version", 1)

        # Validate last_date
        last_date = raw.get("last_date")
        if not isinstance(last_date, str) or len(last_date) != 10:
            last_date = default["last_date"]

        # Validate scores
        scores = {}
        raw_scores = raw.get("scores")
        if isinstance(raw_scores, dict):
            for k in ASPECT_KEYS:
                val = raw_scores.get(k, default["scores"][k])
                try:
                    val_int = int(val)
                except (ValueError, TypeError):
                    val_int = default["scores"][k]
                scores[k] = max(MIN_SCORE, min(MAX_SCORE, val_int))
        else:
            scores = dict(default["scores"])

        # Validate progress
        progress = {}
        raw_progress = raw.get("progress")
        if isinstance(raw_progress, dict):
            for k in ASPECT_KEYS:
                val = raw_progress.get(k, 0)
                try:
                    val_int = int(val)
                except (ValueError, TypeError):
                    val_int = 0
                progress[k] = max(0, min(CLICKS_PER_POINT - 1, val_int))
        else:
            progress = dict(default["progress"])

        # Validate theme
        theme = raw.get("theme", "auto")
        if theme not in ("auto", "light", "dark"):
            theme = "auto"

        # Validate history
        history: List[Dict[str, Any]] = []
        raw_history = raw.get("history")
        if isinstance(raw_history, list):
            seen_dates = set()
            for item in raw_history:
                if isinstance(item, dict) and "date" in item and isinstance(item["date"], str):
                    d_str = item["date"]
                    if d_str not in seen_dates:
                        seen_dates.add(d_str)
                        cleaned_item = {"date": d_str}
                        for k in ASPECT_KEYS:
                            try:
                                v = int(item.get(k, 0))
                            except (ValueError, TypeError):
                                v = 0
                            cleaned_item[k] = max(MIN_SCORE, min(MAX_SCORE, v))
                        cleaned_item["total"] = sum(cleaned_item[k] for k in ASPECT_KEYS)
                        cleaned_item["average"] = round(cleaned_item["total"] / len(ASPECT_KEYS), 1)
                        history.append(cleaned_item)
            # Sort chronologically
            history.sort(key=lambda x: x["date"])
        if not history:
            history = list(default["history"])

        # Validate click_history
        click_history: List[Dict[str, Any]] = []
        raw_clicks = raw.get("click_history")
        if isinstance(raw_clicks, list):
            for c in raw_clicks[-MAX_CLICK_HISTORY:]:
                if isinstance(c, dict):
                    click_history.append(c)

        return {
            "schema_version": schema_version,
            "last_date": last_date,
            "scores": scores,
            "progress": progress,
            "history": history,
            "click_history": click_history,
            "theme": theme,
        }

    def load_data(self) -> Dict[str, Any]:
        """Load data from JSON file with error recovery."""
        if not os.path.exists(self.file_path):
            self.data = self.get_initial_dataset()
            self.save_data()
            return self.data

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    raise ValueError("JSON file is empty")
                raw = json.loads(content)
                self.data = self.validate_and_repair_data(raw)
        except Exception:
            # Backup corrupt file safely
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            corrupt_backup = f"{self.file_path}.corrupt.{timestamp}"
            try:
                if os.path.exists(self.file_path):
                    os.rename(self.file_path, corrupt_backup)
            except Exception:
                pass
            self.data = self.get_initial_dataset()
            self.save_data()

        return self.data

    def save_data(self) -> bool:
        """Atomic write to JSON file."""
        tmp_path = self.file_path + ".tmp"
        try:
            parent = os.path.dirname(self.file_path)
            if parent:
                os.makedirs(parent, exist_ok=True)
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_path, self.file_path)
            return True
        except Exception:
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass
            return False

    def upsert_today_snapshot(self, date_str: str) -> None:
        """Create or update snapshot for a given date in history."""
        scores = self.data["scores"]
        total = sum(scores[k] for k in ASPECT_KEYS)
        average = round(total / len(ASPECT_KEYS), 1)

        snapshot = {
            "date": date_str,
            **{k: scores[k] for k in ASPECT_KEYS},
            "total": total,
            "average": average,
        }

        history = self.data["history"]
        for idx, entry in enumerate(history):
            if entry["date"] == date_str:
                history[idx] = snapshot
                return

        history.append(snapshot)
        history.sort(key=lambda x: x["date"])

    def apply_daily_decay(self, current_date_str: Optional[str] = None) -> int:
        """Apply automatic daily decay of 1 point per elapsed calendar date.
        Returns the number of days processed.
        """
        if current_date_str is None:
            current_date_str = datetime.date.today().isoformat()

        last_date_str = self.data.get("last_date", REFERENCE_DATE)

        try:
            last_dt = datetime.date.fromisoformat(last_date_str)
            current_dt = datetime.date.fromisoformat(current_date_str)
        except Exception:
            # Fallback if invalid format
            self.data["last_date"] = current_date_str
            self.save_data()
            return 0

        delta_days = (current_dt - last_dt).days
        if delta_days <= 0:
            # Same day or time traveled backwards; ensure today snapshot exists
            self.upsert_today_snapshot(last_date_str)
            self.save_data()
            return 0

        # Day-by-day decay
        # 1. Ensure snapshot for last_date is saved before decay begins
        self.upsert_today_snapshot(last_date_str)

        sim_dt = last_dt
        days_processed = 0
        while sim_dt < current_dt:
            sim_dt += datetime.timedelta(days=1)
            days_processed += 1
            sim_str = sim_dt.isoformat()

            # Reduce all 5 scores by 1 (minimum 0)
            # Note: Progress counter DOES NOT decay!
            for k in ASPECT_KEYS:
                self.data["scores"][k] = max(MIN_SCORE, self.data["scores"][k] - 1)

            # Record snapshot for this day
            self.upsert_today_snapshot(sim_str)

            # Record system activity for daily decay
            self.record_activity(
                aspect="all",
                action_type="daily_decay",
                message=f"Pergantian hari ({sim_str}) — Semua skor berkurang 1",
                resulting_score=None,
                resulting_progress=None,
                timestamp=f"{sim_str}T00:00:00",
                save_immediately=False,
            )

        self.data["last_date"] = current_date_str
        self.save_data()
        return days_processed

    def record_activity(
        self,
        aspect: str,
        action_type: str,
        message: str,
        resulting_score: Optional[int] = None,
        resulting_progress: Optional[int] = None,
        timestamp: Optional[str] = None,
        save_immediately: bool = True,
    ) -> Dict[str, Any]:
        """Record an activity item in the chronological activity feed."""
        if timestamp is None:
            timestamp = datetime.datetime.now().isoformat(timespec="seconds")

        item = {
            "aspect": aspect,
            "type": action_type,
            "message": message,
            "score": resulting_score,
            "progress": resulting_progress,
            "timestamp": timestamp,
        }

        self.data["click_history"].insert(0, item)
        if len(self.data["click_history"]) > MAX_CLICK_HISTORY:
            self.data["click_history"] = self.data["click_history"][:MAX_CLICK_HISTORY]

        if save_immediately:
            self.save_data()
        return item

    def increment_aspect_progress(self, aspect: str) -> Dict[str, Any]:
        """Plus button action:
        - Each click adds 1 to progress (0..9).
        - 10th click grants 1 point (up to 10), resets progress to 0.
        - If score is already 10: does not add progress or hoard points.
        """
        if aspect not in ASPECT_KEYS:
            raise KeyError(f"Unknown aspect: {aspect}")

        aspect_info = ASPECT_DETAILS[aspect]
        current_score = self.data["scores"][aspect]
        current_progress = self.data["progress"][aspect]
        today_str = self.data.get("last_date", datetime.date.today().isoformat())

        # If already at max score (10)
        if current_score >= MAX_SCORE:
            item = self.record_activity(
                aspect=aspect,
                action_type="max_reached",
                message=f"{aspect_info['name']} — Skor sudah maksimal (10/10)",
                resulting_score=current_score,
                resulting_progress=current_progress,
            )
            return {
                "status": "MAX_REACHED",
                "score": current_score,
                "progress": current_progress,
                "activity": item,
            }

        # Increment progress
        new_progress = current_progress + 1
        if new_progress >= CLICKS_PER_POINT:
            # 10th click: Grant point and reset progress
            new_score = min(MAX_SCORE, current_score + 1)
            self.data["scores"][aspect] = new_score
            self.data["progress"][aspect] = 0
            self.upsert_today_snapshot(today_str)
            item = self.record_activity(
                aspect=aspect,
                action_type="point_up",
                message=f"{aspect_info['name']} — Mendapat +1 poin ({new_score}/10)",
                resulting_score=new_score,
                resulting_progress=0,
            )
            return {
                "status": "POINT_EARNED",
                "score": new_score,
                "progress": 0,
                "activity": item,
            }
        else:
            # Progress click (1..9)
            self.data["progress"][aspect] = new_progress
            item = self.record_activity(
                aspect=aspect,
                action_type="progress_up",
                message=f"{aspect_info['name']} — Progres +1 ({new_progress}/10)",
                resulting_score=current_score,
                resulting_progress=new_progress,
            )
            return {
                "status": "PROGRESS_INCREMENTED",
                "score": current_score,
                "progress": new_progress,
                "activity": item,
            }

    def decrement_aspect_score(self, aspect: str) -> Dict[str, Any]:
        """Minus button action:
        - Decreases aspect score by 1 immediately.
        - Clamped to minimum 0.
        - DOES NOT alter click progress!
        """
        if aspect not in ASPECT_KEYS:
            raise KeyError(f"Unknown aspect: {aspect}")

        aspect_info = ASPECT_DETAILS[aspect]
        current_score = self.data["scores"][aspect]
        current_progress = self.data["progress"][aspect]
        today_str = self.data.get("last_date", datetime.date.today().isoformat())

        if current_score <= MIN_SCORE:
            item = self.record_activity(
                aspect=aspect,
                action_type="min_reached",
                message=f"{aspect_info['name']} — Skor sudah minimum (0)",
                resulting_score=0,
                resulting_progress=current_progress,
            )
            return {
                "status": "MIN_REACHED",
                "score": 0,
                "progress": current_progress,
                "activity": item,
            }

        new_score = max(MIN_SCORE, current_score - 1)
        self.data["scores"][aspect] = new_score
        # Progress remains unchanged
        self.upsert_today_snapshot(today_str)
        item = self.record_activity(
            aspect=aspect,
            action_type="score_down",
            message=f"{aspect_info['name']} — Poin -1 ({new_score}/10)",
            resulting_score=new_score,
            resulting_progress=current_progress,
        )
        return {
            "status": "SCORE_DECREMENTED",
            "score": new_score,
            "progress": current_progress,
            "activity": item,
        }

    def get_summary(self) -> Dict[str, Any]:
        """Calculate total and average scores across all 5 aspects."""
        scores = self.data["scores"]
        total = sum(scores.values())
        average = round(total / len(ASPECT_KEYS), 1)

        # Health/progress badge
        if average >= 8.0:
            status_text = "Luar Biasa ✨"
        elif average >= 6.0:
            status_text = "Konsisten Maju 🚀"
        elif average >= 4.0:
            status_text = "Terus Bertumbuh 🌱"
        elif average >= 2.0:
            status_text = "Ayo Bangkit 🔥"
        else:
            status_text = "Tetap Semangat 💪"

        return {
            "total": total,
            "max_total": 50,
            "average": average,
            "max_average": 10.0,
            "status_text": status_text,
        }

    def get_last_7_days_history(self) -> List[Dict[str, Any]]:
        """Return history for the last 7 calendar dates up to last_date.
        Ensures continuous chronological sequence.
        """
        history = list(self.data.get("history", []))
        if not history:
            return []

        # Map by date
        by_date = {entry["date"]: entry for entry in history}
        last_date_str = self.data.get("last_date", datetime.date.today().isoformat())

        try:
            anchor_dt = datetime.date.fromisoformat(last_date_str)
        except Exception:
            anchor_dt = datetime.date.today()

        result = []
        for i in range(6, -1, -1):
            target_dt = anchor_dt - datetime.timedelta(days=i)
            target_str = target_dt.isoformat()
            if target_str in by_date:
                result.append(by_date[target_str])
            else:
                # If date isn't recorded yet, provide graceful entry
                result.append({
                    "date": target_str,
                    "jiwa": 0,
                    "raga": 0,
                    "emosional": 0,
                    "prinsipal": 0,
                    "finansial": 0,
                    "total": 0,
                    "average": 0.0,
                })

        return result

    def set_theme_preference(self, theme: str) -> None:
        """Update and persist theme preference ('auto', 'light', 'dark')."""
        if theme in ("auto", "light", "dark"):
            self.data["theme"] = theme
            self.save_data()

    def reset_to_initial(self, current_date_str: Optional[str] = None) -> None:
        """Reset application state to initial reference values."""
        self.data = self.get_initial_dataset()
        if current_date_str:
            self.apply_daily_decay(current_date_str)
        else:
            self.save_data()

    def export_json_string(self) -> str:
        """Return formatted JSON string for backup/export."""
        return json.dumps(self.data, indent=2, ensure_ascii=False)

    def export_backup_json(self) -> str:
        """Return formatted JSON string for backup/export."""
        return self.export_json_string()

    def reset_to_defaults(self, current_date_str: Optional[str] = None) -> None:
        """Reset application state to initial reference values."""
        self.reset_to_initial(current_date_str)
