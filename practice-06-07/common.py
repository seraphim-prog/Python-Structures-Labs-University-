"""Перевірка даних запиту і спільні правила відповідей."""

from datetime import datetime, timezone
from functools import wraps
from math import isfinite

from flask import request


class APIError(Exception):
    def __init__(self, message, status_code=400, details=None):
        super().__init__(message)
        self.status_code = status_code
        self.details = details or {}


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_json():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise APIError("Очікується JSON-об’єкт.")
    return data


def validate_json(required_fields):
    """Передає перевірений JSON і називає відсутні поля."""
    def decorate(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            data = read_json()
            missing = [field for field in required_fields if field not in data]
            if missing:
                raise APIError("Відсутні обов’язкові поля.", details={"missing": missing})
            return view(*args, data=data, **kwargs)
        return wrapped
    return decorate


def text_field(value, field, limit, status=400):
    if isinstance(value, str):
        cleaned = value.strip()
        if 0 < len(cleaned) <= limit:
            return cleaned
    raise APIError("Некоректне текстове поле.", status, {field: f"Від 1 до {limit} символів."})


def number(value, field, status=400):
    try:
        parsed = float(value)
    except (TypeError, ValueError, OverflowError):
        parsed = float("nan")
    if isinstance(value, bool) or not isfinite(parsed):
        raise APIError("Очікується скінченне число.", status, {"field": field})
    return parsed


def pagination(default=10):
    try:
        page = int(request.args.get("page", "1"))
        per_page = int(request.args.get("per_page", str(default)))
    except ValueError:
        raise APIError("page і per_page мають бути цілими числами.") from None
    if page < 1 or not 1 <= per_page <= 100:
        raise APIError("page має бути ≥ 1, per_page має бути від 1 до 100.")
    return page, per_page


def ordering(parameter, allowed, default):
    field = request.args.get(parameter, default)
    direction = request.args.get("order", "asc")
    if field not in allowed or direction not in {"asc", "desc"}:
        raise APIError("Некоректне сортування.", details={parameter: list(allowed), "order": ["asc", "desc"]})
    return field, direction == "desc"


def sorted_rows(rows, field, descending):
    return sorted(rows, key=lambda row: row[field].casefold() if isinstance(row[field], str) else row[field],
                  reverse=descending)
