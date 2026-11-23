"""Перевіряє числові значення у конфігурації та показниках."""

from math import isfinite

from ..errors import InvalidFieldError


def finite_number(value: object, field: str) -> float:
    """Перетворює ціле або дійсне значення на скінченне число.

    Args:
        value (object): Значення, отримане з налаштувань або списку.
        field (str): Назва поля для повідомлення про помилку.

    Returns:
        float: Перевірене значення.

    Raises:
        InvalidFieldError: Тип або значення поля некоректне.
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise InvalidFieldError(field, "має бути числом")
    try:
        number = float(value)
    except OverflowError as error:
        raise InvalidFieldError(field, "містить завелике число") from error
    if not isfinite(number):
        raise InvalidFieldError(field, "має бути скінченним")
    return number
