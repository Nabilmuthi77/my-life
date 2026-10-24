"""Constants and definitions for My Life self-improvement app."""

from typing import Dict, Any

REFERENCE_DATE = "2026-10-22"

INITIAL_SCORES: Dict[str, int] = {
    "jiwa": 3,
    "raga": 4,
    "emosional": 2,
    "prinsipal": 2,
    "finansial": 0,
}

INITIAL_PROGRESS: Dict[str, int] = {
    "jiwa": 0,
    "raga": 0,
    "emosional": 0,
    "prinsipal": 0,
    "finansial": 0,
}

ASPECT_KEYS = ["jiwa", "raga", "emosional", "prinsipal", "finansial"]

ASPECT_DETAILS: Dict[str, Dict[str, Any]] = {
    "jiwa": {
        "name": "Jiwa",
        "description": "Mendekati Sang Pencipta",
        "long_description": "Menjaga kedamaian batin, spiritualitas, doa, bersyukur, serta kesadaran penuh kepada Sang Pencipta setiap saat.",
        "quote": "Dekat dengan Tuhan, menenangkan hati dan menguatkan langkah.",
        "icon_name": "SPA_ROUNDED",
        "light_color": "#0D9488",
        "dark_color": "#2DD4BF",
        "light_bg": "#E6F4F1",
        "dark_bg": "#0E2F35",
    },
    "raga": {
        "name": "Raga",
        "description": "Menjaga tubuh",
        "long_description": "Kesehatan fisik, olahraga teratur, nutrisi seimbang, istirahat cukup, dan menjaga vitalitas raga.",
        "quote": "Tubuh yang sehat adalah rumah bagi jiwa yang kuat dan pikiran yang jernih.",
        "icon_name": "FAVORITE_ROUNDED",
        "light_color": "#E11D48",
        "dark_color": "#FB7185",
        "light_bg": "#FEE2E2",
        "dark_bg": "#3B1B24",
    },
    "emosional": {
        "name": "Emosional",
        "description": "Mengendalikan diri",
        "long_description": "Kecerdasan emosional, ketenangan hati, kesabaran, empati, dan penguasaan respon terhadap tekanan hidup.",
        "quote": "Penguasaan diri adalah kemenangan sejati dalam setiap pergulatan hidup.",
        "icon_name": "PSYCHOLOGY_ROUNDED",
        "light_color": "#7C3AED",
        "dark_color": "#A78BFA",
        "light_bg": "#EDE9FE",
        "dark_bg": "#2A1E3E",
    },
    "prinsipal": {
        "name": "Prinsipal",
        "description": "Menjaga prinsip",
        "long_description": "Integritas moral, kedisiplinan, kejujuran, komitmen pada nilai-nilai hidup luhur, dan arah tujuan hidup yang teguh.",
        "quote": "Prinsip yang teguh membimbing langkah di saat badai keraguan menerpa.",
        "icon_name": "EXPLORE_ROUNDED",
        "light_color": "#0284C7",
        "dark_color": "#38BDF8",
        "light_bg": "#E0F2FE",
        "dark_bg": "#152D42",
    },
    "finansial": {
        "name": "Finansial",
        "description": "Mengelola keuangan",
        "long_description": "Manajemen keuangan bijak, menabung, berinvestasi, menghindari pemborosan, dan menjaga kemandirian finansial.",
        "quote": "Mengelola rezeki dengan bijak mendatangkan keberkahan dan ketenangan.",
        "icon_name": "ACCOUNT_BALANCE_WALLET_ROUNDED",
        "light_color": "#059669",
        "dark_color": "#34D399",
        "light_bg": "#DCFCE7",
        "dark_bg": "#133527",
    },
}

MAX_SCORE = 10
MIN_SCORE = 0
CLICKS_PER_POINT = 10
MAX_CLICK_HISTORY = 500
