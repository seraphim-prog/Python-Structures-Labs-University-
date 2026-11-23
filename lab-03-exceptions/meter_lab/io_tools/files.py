"""Читає текстові зразки й налаштування у кодуванні UTF-8."""

from pathlib import Path


def read_utf8(path: Path) -> str:
    """Зчитує весь текст файлу та закриває його після читання.

    Args:
        path (Path): Шлях до текстового файлу.

    Returns:
        str: Вміст файлу.

    Raises:
        OSError: Файл відсутній або його неможливо прочитати.
        UnicodeDecodeError: Дані неможливо декодувати як UTF-8.
    """
    with path.open(encoding="utf-8") as source:
        return source.read()
