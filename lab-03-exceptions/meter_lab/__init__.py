"""Надає доступ до основних операцій пакета роботи з температурами."""

from .errors import MeterError
from .service import check_readings, load_settings

__all__ = ["MeterError", "check_readings", "load_settings"]
