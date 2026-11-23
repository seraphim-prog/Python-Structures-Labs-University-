"""Визначає спільний клас і три окремі винятки для обробки температур."""

from pathlib import Path


class MeterError(Exception):
    """Позначає помилку під час обробки налаштувань або показників.

    Args:
        *args (object): Дані для стандартного конструктора Exception.

    Returns:
        MeterError: Базовий об'єкт винятку.

    Raises:
        Немає.
    """


class InvalidFieldError(MeterError):
    """Зберігає назву поля, яке не пройшло перевірку.

    Args:
        field (str): Назва поля.
        reason (str): Пояснення помилки.

    Returns:
        InvalidFieldError: Виняток перевірки даних.

    Raises:
        Немає.
    """

    def __init__(self, field: str, reason: str) -> None:
        """Запам'ятовує поле та причину відхилення.

        Args:
            field (str): Назва поля.
            reason (str): Пояснення помилки.

        Returns:
            None: Результат ініціалізації.

        Raises:
            Немає.
        """
        super().__init__(field, reason)
        self.field = field
        self.reason = reason

    def __str__(self) -> str:
        """Повертає повідомлення з назвою некоректного поля.

        Args:
            Додаткових параметрів немає.

        Returns:
            str: Назва поля та пояснення.

        Raises:
            Немає.
        """
        return f"Поле «{self.field}» {self.reason}."


class SettingsFileError(MeterError):
    """Зберігає шлях до конфігурації, яку не вдалося завантажити.

    Args:
        path (Path): Шлях до файлу JSON.

    Returns:
        SettingsFileError: Виняток завантаження конфігурації.

    Raises:
        Немає.
    """

    def __init__(self, path: Path) -> None:
        """Запам'ятовує шлях до конфігурації.

        Args:
            path (Path): Шлях до файлу JSON.

        Returns:
            None: Результат ініціалізації.

        Raises:
            Немає.
        """
        super().__init__(path)
        self.path = path

    def __str__(self) -> str:
        """Повертає повідомлення з назвою файлу.

        Args:
            Додаткових параметрів немає.

        Returns:
            str: Короткий опис помилки завантаження.

        Raises:
            Немає.
        """
        return f"Не вдалося завантажити «{self.path.name}»."


class ThresholdExceededError(MeterError):
    """Зберігає середню температуру та перевищену межу.

    Args:
        average (float): Середня температура в градусах Цельсія.
        limit (float): Верхня межа в градусах Цельсія.

    Returns:
        ThresholdExceededError: Виняток перевищення межі.

    Raises:
        Немає.
    """

    def __init__(self, average: float, limit: float) -> None:
        """Запам'ятовує обчислене середнє та межу.

        Args:
            average (float): Середня температура.
            limit (float): Верхня межа.

        Returns:
            None: Результат ініціалізації.

        Raises:
            Немає.
        """
        super().__init__(average, limit)
        self.average = average
        self.limit = limit

    def __str__(self) -> str:
        """Повертає повідомлення про перевищення межі.

        Args:
            Додаткових параметрів немає.

        Returns:
            str: Середня температура та дозволена межа.

        Raises:
            Немає.
        """
        return f"Середня {self.average:g} °C перевищила межу {self.limit:g} °C."
