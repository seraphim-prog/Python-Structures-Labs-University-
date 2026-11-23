"""Перетворює текстові числа для обчислення середнього."""

from math import isfinite


def mean_from_text(raw_total: str, raw_count: str) -> float:
    """Ділить суму показників на їх кількість.

    Args:
        raw_total (str): Сума показників у текстовому вигляді.
        raw_count (str): Кількість показників у текстовому вигляді.

    Returns:
        float: Середнє значення.

    Raises:
        ValueError: Хибний формат, нескінченна сума або некоректна кількість.
        ZeroDivisionError: Кількість дорівнює нулю.
    """
    total = float(raw_total)
    count = int(raw_count)
    if not isfinite(total):
        raise ValueError("сума має бути скінченним числом")
    if count < 0:
        raise ValueError("кількість має бути невід'ємною")
    try:
        return total / count
    except OverflowError as error:
        raise ValueError("кількість завелика для обчислення") from error
