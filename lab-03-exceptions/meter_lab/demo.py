"""Відтворює сценарії лабораторної роботи в консолі."""

import argparse
from pathlib import Path

import meter_lab

from .errors import InvalidFieldError, MeterError
from .io_tools import mean_from_text, read_utf8
from .service import check_readings, check_with_journal

SAMPLES = Path(__file__).resolve().parent.parent / "samples"


def _task_1() -> None:
    print("ЗАВДАННЯ 1. Обробка вбудованих винятків")
    print("\n1.1. Перетворення тексту в ціле число (try/except)")
    for raw_count in ("3", "три"):
        try:
            count = int(raw_count)
        except ValueError:
            print(f"  {raw_count!r} → ValueError: очікувалося ціле число.")
            continue
        print(f"  {raw_count!r} → успіх: кількість = {count}")

    print("\n1.2. Читання файлу (try/except/else/finally)")
    for filename in ("temperatures.txt", "missing_temperatures.txt"):
        print(f"  Файл {filename}")
        try:
            contents = read_utf8(SAMPLES / filename)
        except (OSError, UnicodeDecodeError) as error:
            print(f"  except → {type(error).__name__}")
        else:
            readings = ", ".join(contents.splitlines())
            print(f"  else → зчитано показники: {readings}")
        finally:
            print("  finally → спробу читання завершено.")

    print("\n1.3. Середнє з текстових даних (один except для двох типів)")
    for total, count_text in (("24", "2"), ("abc", "2"), ("8", "0")):
        label = f"  сума={total!r}, кількість={count_text!r}"
        try:
            average = mean_from_text(total, count_text)
        except (ValueError, ZeroDivisionError) as error:
            print(f"{label} → {type(error).__name__}")
        else:
            print(f"{label} → успіх: {average:.2f}")


def _task_2() -> None:
    print("ЗАВДАННЯ 2. Власні винятки та ланцюжки")
    settings = meter_lab.load_settings(SAMPLES / "settings.json")
    limit = settings["high_limit"]
    readings = [
        float(line)
        for line in read_utf8(SAMPLES / "temperatures.txt").splitlines()
    ]
    average = check_readings(readings, limit)
    print(f"Файл settings.json: межа {limit:.2f} °C, середня {average:.2f} °C.")

    print("\n2.1. Порожній список показників")
    try:
        check_readings([], limit)
    except InvalidFieldError as error:
        print(f"  Перехоплено InvalidFieldError: {error}")

    print("\n2.2. Завантаження конфігурації з помилкою")
    for filename in ("missing_settings.json", "broken_settings.json"):
        try:
            meter_lab.load_settings(SAMPLES / filename)
        except MeterError as error:
            print(f"  Перехоплено як MeterError → {type(error).__name__}")
            print(f"  {error}")
            print(f"  __cause__: {type(error.__cause__).__name__}")

    print("\n2.3. Показники 27 і 28 °C при межі 25 °C")
    journal: list[str] = []
    try:
        check_with_journal([27.0, 28.0], limit, journal)
    except MeterError as error:
        print("  Запис журналу:")
        print(f"  {journal[-1]}")
        print(f"  Після повторного raise отримано: {type(error).__name__}")


def _task_3() -> None:
    print("ЗАВДАННЯ 3. Пакети, імпорти та публічні імена")
    print(f"import meter_lab → {meter_lab.__name__}")
    print(f"from pathlib import Path → {Path.__name__}")
    print(f"from .io_tools import read_utf8 → {read_utf8.__module__}")
    print(f"__all__ → {meter_lab.__all__}")

    # Імпорт із зірочкою виконується лише у словнику для демонстрації.
    namespace: dict[str, object] = {}
    exec("from meter_lab import *", namespace)
    imported = sorted(name for name in namespace if name != "__builtins__")
    matches_exports = imported == sorted(meter_lab.__all__)
    print(f"from meter_lab import * → {imported}")
    print(f"Імпортовані всі й лише імена з __all__: {matches_exports}")
    print(f"SettingsFileError у просторі імен: {'SettingsFileError' in namespace}")


def _task_4() -> None:
    print("ЗАВДАННЯ 4. Документація та інтроспекція")
    print(f"__name__: {check_readings.__name__}")
    print("__doc__ (перший рядок):")
    print(f"  {check_readings.__doc__.splitlines()[0]}")
    print("__annotations__:")
    for name, annotation in check_readings.__annotations__.items():
        print(f"  {name}: {annotation}")
    print("\nhelp(check_readings)")
    help(check_readings)


def main() -> None:
    """Запускає всі демонстрації або одну за аргументом --task.

    Args:
        Параметри читаються з командного рядка.

    Returns:
        None: Результати виводяться в консоль.

    Raises:
        SystemExit: Запитано довідку або отримано некоректний аргумент.
        OSError: Відсутній або недоступний файл успішного сценарію.
        UnicodeDecodeError: Файл показників має хибне кодування.
        ValueError: У файлі показників є рядок, який не є числом.
        MeterError: Вхідні зразки успішного сценарію не пройшли перевірку.
    """
    tasks = {"1": _task_1, "2": _task_2, "3": _task_3, "4": _task_4}
    parser = argparse.ArgumentParser(description="Демонстрація ЛБ №3")
    parser.add_argument(
        "--task", choices=tasks, help="номер завдання для окремого запуску"
    )
    args = parser.parse_args()
    if args.task is not None:
        tasks[args.task]()
        return

    for number, task in tasks.items():
        if number != "1":
            print()
        task()
