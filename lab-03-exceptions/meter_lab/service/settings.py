"""Завантажує та перевіряє верхню межу температури з JSON."""

import json
from pathlib import Path

from ..errors import InvalidFieldError, SettingsFileError
from ..io_tools import read_utf8
from .validation import finite_number


def load_settings(path: Path) -> dict[str, float]:
    """Зчитує з конфігурації скінченне значення high_limit.

    Args:
        path (Path): Шлях до файлу налаштувань у форматі JSON.

    Returns:
        dict[str, float]: Словник з верхньою межею high_limit.

    Raises:
        SettingsFileError: Файл недоступний, має хибне кодування або синтаксис JSON.
        InvalidFieldError: У конфігурації немає коректної верхньої межі.
    """
    try:
        data = json.loads(read_utf8(path))
    except (OSError, ValueError) as error:
        # UnicodeDecodeError та JSONDecodeError успадковують ValueError.
        raise SettingsFileError(path) from error

    if not isinstance(data, dict):
        raise InvalidFieldError("JSON", "має бути об'єктом з ключем high_limit")
    if "high_limit" not in data:
        raise InvalidFieldError("high_limit", "відсутнє")
    return {"high_limit": finite_number(data["high_limit"], "high_limit")}
