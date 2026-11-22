"""Класифікація оцінок за шкалою ЄКТС із завдання."""


def classify_grade(score: int) -> str:
    if score < 0 or score > 100:
        raise ValueError("Оцінка має бути від 0 до 100.")
    # Межі перевіряємо зверху вниз, щоб включити нижню межу кожного рівня.
    if score >= 90:
        return "A"
    elif score >= 82:
        return "B"
    elif score >= 74:
        return "C"
    elif score >= 64:
        return "D"
    elif score >= 60:
        return "E"
    elif score >= 35:
        return "FX"
    else:
        return "F"


def main():
    try:
        score = int(input("Введіть оцінку (0–100): "))
    except ValueError:
        print("Помилка: оцінка має бути цілим числом.")
        return
    except EOFError:
        print("Введення завершено.")
        return

    try:
        grade = classify_grade(score)
    except ValueError as error:
        print(f"Помилка: {error}")
        return

    print(f"Оцінка {score} → ЄКТС: {grade}")
    passed = grade not in ("FX", "F")
    print(f"Результат: {'Зараховано' if passed else 'Не зараховано'}")


if __name__ == "__main__":
    main()
