"""Спільні функції зчитування чисел і перевірки сторін трикутника."""

import math


def parse_real(text: str) -> float:
    """Зчитує скінченне число з десятковою крапкою або комою."""
    try:
        value = float(text.strip().replace(",", "."))
    except ValueError as error:
        raise ValueError("Потрібно ввести дійсне число.") from error
    if not math.isfinite(value):
        raise ValueError("Число має бути скінченним.")
    return value


def read_real(prompt: str) -> float:
    return parse_real(input(prompt))


def forms_triangle(a: float, b: float, c: float) -> bool:
    if a <= 0 or b <= 0 or c <= 0:
        return False
    # Для додатних сторін достатньо перевірити найбільшу сторону.
    x, y, z = sorted((a, b, c))
    return math.isfinite(z) and x > z - y
