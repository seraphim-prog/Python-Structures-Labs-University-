"""СР №1. Математичні задачі та обхід історії обчислень."""

import math


MENU = (
    "1. Факторіал        2. Геометричні фігури\n"
    "3. Історія          4. Ітератор і генератор\n"
    "0. Вихід            m. Показати меню"
)


def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("Для факторіала потрібне ціле n ≥ 0.")
    result = 1  # Порожній добуток для 0! також дорівнює 1.
    for number in range(2, n + 1):
        result *= number
    return result


def read_dimension(prompt: str) -> float:
    text = input(prompt).strip().replace(",", ".")
    try:
        value = float(text)
    except ValueError as error:
        raise ValueError("Розмір потрібно ввести числом.") from error
    if not math.isfinite(value) or value <= 0:
        raise ValueError("Розмір має бути скінченним додатним числом.")
    return value


def factorial_record() -> dict:
    try:
        n = int(input("Введіть ціле n: "))
    except ValueError as error:
        raise ValueError("Для факторіала потрібне ціле n ≥ 0.") from error
    return {
        "name": "Факторіал",
        "inputs": (n,),
        "results": {f"{n}!": factorial(n)},
        "is_geometry": False,
    }


def geometry_record() -> dict:
    print("1. Прямокутник  2. Трикутник  3. Коло")
    choice = input("Оберіть фігуру: ").strip()
    if choice == "1":
        name = "Прямокутник"
        a = read_dimension("Сторона a: ")
        b = read_dimension("Сторона b: ")
        inputs = (a, b)
        results = {"Площа": a * b, "Периметр": 2 * (a + b)}
    elif choice == "2":
        name = "Трикутник"
        base = read_dimension("Основа: ")
        height = read_dimension("Висота до основи: ")
        inputs = (base, height)
        results = {"Площа": base / 2 * height}
    elif choice == "3":
        name = "Коло"
        radius = read_dimension("Радіус: ")
        inputs = (radius,)
        results = {
            "Площа круга": math.pi * radius * radius,
            "Довжина кола": 2 * math.pi * radius,
        }
    else:
        raise ValueError("Оберіть фігуру від 1 до 3.")

    if any(not math.isfinite(value) for value in results.values()):
        raise ValueError("Результат перевищує діапазон дійсних чисел Python.")
    return {
        "name": name,
        "inputs": inputs,
        "results": results,
        "is_geometry": True,
    }


def format_record(record: dict) -> str:
    parts = []
    for label, value in record["results"].items():
        text = f"{value:.2f}" if isinstance(value, float) else str(value)
        parts.append(f"{label} = {text}")
    return f"{record['name']}: " + ", ".join(parts)


class HistoryIterator:
    """Одноразовий обхід списку записів за індексом."""

    def __init__(self, history: list[dict]):
        self._history = history
        self._index = 0
        self._limit = len(history)

    def __iter__(self):
        return self

    def __next__(self) -> dict:
        if self._index >= self._limit:
            raise StopIteration
        record = self._history[self._index]
        self._index += 1
        return record


def geometry_records(history: list[dict]):
    """Видає геометричні записи по одному під час обходу списку."""
    for record in history:
        if record["is_geometry"]:
            yield record


def show_history(history: list[dict]) -> None:
    print(f"Список list: {len(history)} записів.")
    if not history:
        print("Історія порожня. Виконайте обчислення через меню.")
        return
    for number, record in enumerate(history, start=1):
        print(f"{number}. {format_record(record)}")
    last = history[-1]
    print("Кортеж tuple (останній ввід):", last["inputs"])
    print("Словник dict (останні результати):", last["results"])
    print("Тип назви задачі:", type(last["name"]).__name__)
    print("Ознака геометричної задачі (bool):", last["is_geometry"])


def show_traversal(history: list[dict]) -> None:
    iterator = HistoryIterator(history)
    print("Ітератор — уся історія:")
    if not history:
        print("  Немає записів.")
    for record in iterator:
        print(f"  {format_record(record)}")
    print("Після обходу:", next(iterator, "ітератор вичерпано"))

    print("Генератор — лише геометричні задачі:")
    found = False
    for record in geometry_records(history):
        print(f"  {format_record(record)}")
        found = True
    if not found:
        print("  Геометричних записів немає.")


def main() -> None:
    history = []  # Історія існує в пам'яті протягом одного запуску.
    print("Математичні задачі та історія обчислень")
    print(MENU)
    while True:
        try:
            choice = input("\nОберіть команду: ").strip().lower()
            if choice == "0":
                break
            elif choice == "m":
                print(MENU)
            elif choice == "1" or choice == "2":
                record = factorial_record() if choice == "1" else geometry_record()
                # Запис зберігається після успішного обчислення та виводу.
                print(format_record(record))
                history.append(record)
            elif choice == "3":
                show_history(history)
            elif choice == "4":
                show_traversal(history)
            else:
                print("Помилка: введіть команду 0–4 або m для меню.")
        except ValueError as error:
            print(f"Помилка: {error}")
        except (EOFError, KeyboardInterrupt):
            print()
            break
    print("Роботу завершено.")


if __name__ == "__main__":
    main()
