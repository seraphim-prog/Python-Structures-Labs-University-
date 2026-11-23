"""Обчислює середнє показників і перевіряє задану межу."""

from statistics import fmean

from ..errors import InvalidFieldError, MeterError, ThresholdExceededError
from .validation import finite_number


def check_readings(readings: list[float], limit: float) -> float:
    """Обчислює середню температуру та перевіряє верхню межу.

    Args:
        readings (list[float]): Показники температури в °C.
        limit (float): Допустима верхня межа в °C.

    Returns:
        float: Середня температура в °C.

    Raises:
        InvalidFieldError: Некоректна межа або показники.
        ThresholdExceededError: Середнє перевищує межу.
    """
    if not readings:
        raise InvalidFieldError("readings", "має містити хоча б один показник")
    limit = finite_number(limit, "high_limit")
    values = [
        finite_number(value, f"readings[{index}]")
        for index, value in enumerate(readings)
    ]
    try:
        average = fmean(values)
    except OverflowError as error:
        raise InvalidFieldError("readings", "містить завеликі значення") from error
    if average > limit:
        raise ThresholdExceededError(average, limit)
    return average


def check_with_journal(
    readings: list[float], limit: float, journal: list[str]
) -> float:
    """Перевіряє показники й додає повідомлення про помилку до журналу.

    Args:
        readings (list[float]): Показники температури в °C.
        limit (float): Допустима верхня межа в °C.
        journal (list[str]): Список для записів про помилки.

    Returns:
        float: Середня температура в °C.

    Raises:
        InvalidFieldError: Некоректна межа або показники.
        ThresholdExceededError: Середнє перевищує межу.
    """
    try:
        return check_readings(readings, limit)
    except MeterError as error:
        journal.append(f"{type(error).__name__}: {error}")
        raise
