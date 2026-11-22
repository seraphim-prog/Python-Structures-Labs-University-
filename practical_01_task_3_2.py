"""Інтерактивний калькулятор на основі циклу while."""

import math

from practical_01_common import parse_real


def calculate(left: float, operator: str, right: float) -> float:
    if operator in ("/", "//", "%") and right == 0:
        raise ZeroDivisionError("Ділення на нуль.")

    if operator == "+":
        result = left + right
    elif operator == "-":
        result = left - right
    elif operator == "*":
        result = left * right
    elif operator == "/":
        result = left / right
    elif operator == "//":
        result = left // right
    elif operator == "%":
        result = left % right
    elif operator == "**":
        if left == 0 and right < 0:
            raise ZeroDivisionError("Нуль у від'ємному степені.")
        result = left ** right
    else:
        raise ValueError("Невідомий оператор.")

    if isinstance(result, complex):
        raise ValueError("Результат степеня виходить за межі дійсних чисел.")
    if not math.isfinite(result):
        raise OverflowError
    return result


def calculator():
    """Читає команди, зберігає успішні обчислення і показує історію."""
    print("=== Калькулятор ===")
    print("Формат: число оператор число. Команди: history, quit.")
    history = []

    while True:
        try:
            user_input = input("> ").strip()
        except EOFError:
            break
        command = user_input.lower()
        if command == "quit":
            break
        if command == "history":
            if not history:
                print("Історія порожня.")
            for index, entry in enumerate(history, start=1):
                print(f"{index}. {entry}")
            continue

        parts = user_input.split()
        if len(parts) != 3:
            print("Помилка: формат має бути «число оператор число».")
            continue

        left_text, operator, right_text = parts
        try:
            left, right = parse_real(left_text), parse_real(right_text)
            result = calculate(left, operator, right)
        except (ValueError, ZeroDivisionError) as error:
            print(f"Помилка: {error}")
            continue
        except OverflowError:
            print("Помилка: результат завеликий для формату float.")
            continue

        # Історія містить тільки результати, що успішно обчислилися.
        entry = f"{left_text} {operator} {right_text} = {result:.12g}"
        history.append(entry)
        print(entry)

    print("Калькулятор завершено.")


if __name__ == "__main__":
    calculator()
