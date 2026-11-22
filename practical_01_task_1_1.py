"""Обчислення математичних виразів."""

import math

from practical_01_common import forms_triangle, read_real


def main():
    try:
        a = read_real("Введіть a: ")
        b = read_real("Введіть b: ")
        c = read_real("Введіть c: ")
        sum_squares = a ** 2 + b ** 2 + c ** 2
        average = (a + b + c) / 3
        discriminant = b ** 2 - 4 * a * c
        if not math.isfinite(sum_squares) or not math.isfinite(discriminant):
            raise OverflowError
    except ValueError as error:
        print(f"Помилка: {error}")
        return
    except OverflowError:
        print("Помилка: числа завеликі для обчислення у форматі float.")
        return
    except EOFError:
        print("Введення завершено.")
        return

    print(f"Сума квадратів: {sum_squares:.2f}")
    print(f"Середнє арифметичне: {average:.2f}")
    print(f"Дискримінант (b² − 4ac): {discriminant:.2f}")
    if a == 0:
        print("За a = 0 квадратний член відсутній.")

    if a > 0 and b > 0:
        hypotenuse = math.sqrt(a ** 2 + b ** 2)
        print(f"Гіпотенуза: {hypotenuse:.2f}")
    else:
        print("Гіпотенуза: потрібні додатні катети a та b.")
    print(f"Утворюють трикутник: {'так' if forms_triangle(a, b, c) else 'ні'}")

    # Додатково показуємо цілочисельне ділення та остачу з умови.
    if b == 0:
        print("Операції // і % потребують ненульового b.")
    else:
        quotient, remainder = a // b, a % b
        if math.isfinite(quotient) and math.isfinite(remainder):
            print(f"a // b = {quotient:.2f}, a % b = {remainder:.2f}")
        else:
            print("Частка виходить за діапазон float.")


if __name__ == "__main__":
    main()
