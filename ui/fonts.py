"""
Единая загрузка шрифтов Geologica из assets/fonts.

Раньше каждое окно грузило шрифты само, а главное меню искало файлы
«Geologica Black.ttf», «Geologica.ttf», «Geologica Roman SemiBold.ttf» в папке ui/ —
после переноса шрифтов в assets/fonts этих файлов там нет, addApplicationFont
возвращал -1, и Qt молча подставлял системный шрифт.

Здесь шрифты регистрируются один раз, а окна получают реальные имена семейств,
которые вернул Qt (имя семейства в файле не всегда совпадает с именем файла:
например, Geologica-SemiBold.ttf называется «Geologica Roman SemiBold»).

Важно: в зависимости от ОС Qt может вернуть «типографское» имя семейства —
тогда Regular и SemiBold оба называются «Geologica Roman», а Bold и Black —
«Geologica», и QFont(семейство, размер) берёт обычное начертание. Поэтому
шрифт создаём через make_font(), которая дополнительно задаёт толщину.
"""
import os

from PyQt5 import QtGui

# Путь считаем от этого файла, а не от рабочей папки — так шрифты находятся
# и при запуске main.py из PyCharm, и при запуске отдельного окна (python ui/...py).
FONTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "fonts")

FALLBACK_FAMILY = "Arial"

_FONT_FILES = {
    "black": os.path.join(FONTS_DIR, "Geologica-Black.ttf"),
    "bold": os.path.join(FONTS_DIR, "Geologica-Bold.ttf"),
    "semibold": os.path.join(FONTS_DIR, "Geologica-SemiBold.ttf"),
    "regular": os.path.join(FONTS_DIR, "Geologica-Regular.ttf"),
    "auto_bold": os.path.join(FONTS_DIR, "Geologica_Auto-Bold.ttf"),
}

_WEIGHTS = {
    "black": QtGui.QFont.Black,
    "bold": QtGui.QFont.Bold,
    "semibold": QtGui.QFont.DemiBold,
    "regular": QtGui.QFont.Normal,
    "auto_bold": QtGui.QFont.Bold,
}

_families = None


def load_app_fonts():
    """Регистрирует шрифты (один раз за запуск) и возвращает {ключ: имя семейства}.
    Вызывать после создания QApplication."""
    global _families
    if _families is not None:
        return _families
    _families = {}
    for key, path in _FONT_FILES.items():
        font_id = QtGui.QFontDatabase.addApplicationFont(path) if os.path.exists(path) else -1
        families = QtGui.QFontDatabase.applicationFontFamilies(font_id) if font_id != -1 else []
        if families:
            _families[key] = families[0]
        else:
            print(f"[fonts] не удалось загрузить шрифт: {path}")
            _families[key] = FALLBACK_FAMILY
    return _families


def family(key):
    """Имя семейства для ключа: black / bold / semibold / regular / auto_bold."""
    return load_app_fonts()[key]


def make_font(key, size):
    """QFont нужного начертания: make_font("semibold", 12)."""
    font = QtGui.QFont(family(key), size)
    font.setWeight(_WEIGHTS[key])
    return font
