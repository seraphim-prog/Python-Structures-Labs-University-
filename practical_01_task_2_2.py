"""Тип трикутника і площа за формулою Герона."""

import math

from practical_01_common import forms_triangle, read_real


def triangle_type(a: float, b: float, c: float) -> str:
    if not forms_triangle(a, b, c):
        return "не є трикутником"

    x, y, z = sorted((a, b, c))  # z — найбільша сторона.
    if x == y and y == z:
        return "рівносторонній"
    else:
        # Додатковий відносний допуск захищає від помилки на малих сторонах.
        difference = abs(x ** 2 + y ** 2 - z ** 2)
        relative = abs((x / z) ** 2 + (y / z) ** 2 - 1)
        if difference < 1e-9 and relative < 1e-9:
            return "прямокутний"
        elif x == y or y == z:
            return "рівнобедрений"
        else:
            return "різносторонній"


def triangle_area(a: float, b: float, c: float) -> float:
    if not forms_triangle(a, b, c):
        raise ValueError("Сторони не утворюють трикутника.")
    # Формула Герона для впорядкованих сторін z ≥ y ≥ x.
    # Групування множників зменшує втрату точності поблизу виродження.
    x, y, z = sorted((a, b, c))
    factors = (z + (y + x), x - (z - y), x + (z - y), z + (y - x))
    area = (math.sqrt(factors[0]) * math.sqrt(factors[1]) / 4
            * math.sqrt(factors[2]) * math.sqrt(factors[3]))
    if not math.isfinite(area):
        raise OverflowError
    return area


def main():
    try:
        a, b, c = [read_real(f"Введіть сторону {side}: ") for side in "abc"]
        kind = triangle_type(a, b, c)
        print(f"Тип: {kind}")
        if kind != "не є трикутником":
            print(f"Площа: {triangle_area(a, b, c):.6g} кв. од.")
        else:
            print("Площу можна обчислити для трьох коректних сторін.")
    except ValueError as error:
        print(f"Помилка: {error}")
    except OverflowError:
        print("Помилка: сторони завеликі для обчислення у форматі float.")
    except EOFError:
        print("Введення завершено.")


if __name__ == "__main__":
    main()
