"""Конвертор типів та форматоване виведення."""

import math


def main():
    try:
        text = input("Введіть число: ").strip()
        real_value = float(text.replace(",", "."))
        if not math.isfinite(real_value):
            raise ValueError
    except ValueError:
        print("Помилка: введіть скінченне число.")
        return
    except EOFError:
        print("Введення завершено.")
        return

    # Для цілого літерала int(text) зберігає точність вихідного значення.
    try:
        int_value = int(text)
    except ValueError:
        int_value = int(real_value)  # Відкидати дробову частину в бік нуля.
    bool_value = bool(real_value)
    str_value = str(real_value)

    print(f"{'Тип':<8} {'Значення':>16}")
    print(f"{type(int_value).__name__:<8} {int_value:>16d}")
    print(f"{type(real_value).__name__:<8} {real_value:>16.2f}")
    print(f"{type(bool_value).__name__:<8} {str(bool_value):>16}")
    print(f"{type(str_value).__name__:<8} {str_value:>16}")
    print("isinstance(ціле, int):", isinstance(int_value, int))

    try:
        name = input("Введіть ім'я: ").strip()
        age = int(input("Введіть вік: "))
        if not name or age < 0:
            raise ValueError
    except ValueError:
        print("Помилка: потрібні ім'я та невід'ємний цілий вік.")
        return
    except EOFError:
        print("Введення завершено.")
        return

    print(f"Ім'я: {name:<10} | Вік: {age:03d}")
    numbers = list(range(1, 6))
    print(f"list(range(1, 6)) = {numbers}")
    print(f"len(список) = {len(numbers)}, id(список) = {id(numbers)}")


if __name__ == "__main__":
    main()
