"""
語系字典模組
"""
import json
import os
from typing import Dict, List

LANGUAGES: Dict[str, str] = {
    "English": "en",
    "中文": "zh",
    "Deutsch": "de",
    "日本語": "ja",
    "Français": "fr",
    "Tiếng Việt": "vi",
    "Bahasa Indonesia": "id"
}

ORDER_CLASSES: Dict[str, List[str]] = {
    "zh": ["標準", "急件"],
    "en": ["Standard", "Urgent"],
    "de": ["Standard", "Eilig"],
    "ja": ["標準", "緊急"],
    "fr": ["Standard", "Urgent"],
    "vi": ["Chuẩn", "Khẩn cấp"],
    "id": ["Standar", "Mendesak"]
}

MANUFACTURE_METHODS: Dict[str, List[str]] = {
    "zh": ["全自製", "全外包", "部分外包"],
    "en": ["Fully In-House", "Fully Outsourced", "Partially Outsourced"],
    "de": ["Vollständig intern", "Vollständig ausgelagert", "Teilweise ausgelagert"],
    "ja": ["全て内製", "全て外注", "一部外注"],
    "fr": ["Entièrement interne", "Entièrement sous-traité", "Partiellement sous-traité"],
    "vi": ["Toàn bộ nội bộ", "Toàn bộ thuê ngoài", "Thuê ngoài một phần"],
    "id": ["Sepenuhnya internal", "Sepenuhnya outsourcing", "Sebagian outsourcing"]
}

# Global translation registry
TRANSLATIONS: Dict[str, dict] = {}

def load_translations():
    folder = os.path.join(os.path.dirname(__file__), "translations")
    for filename in os.listdir(folder):
        if filename.endswith(".json"):
            with open(os.path.join(folder, filename), "r", encoding="utf-8") as f:
                data = json.load(f)
                TRANSLATIONS.update(data)

# Call this once at app start
load_translations()

def mapped(key: str, lang: str = "en") -> str:
    try:
        return TRANSLATIONS[key][lang]
    except KeyError as e:
        print(f"Missing translation for key: {key} in language: {lang}")
        return key
