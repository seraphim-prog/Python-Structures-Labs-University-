"""Збирає функції читання файлів і перетворення текстових значень."""

from .files import read_utf8
from .parsing import mean_from_text

__all__ = ["mean_from_text", "read_utf8"]
