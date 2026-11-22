"""Функції-генератори для числових послідовностей і вкладених списків."""

from itertools import islice
from math import isfinite
from operator import index


def arithmetic_progression(start: float, step: float):
    value = start
    while True:
        yield value
        value += step


def geometric_progression(start: float, ratio: float,
                          limit: float = float("inf")):
    # Межа включна. Для спадних або сталих прогресій підійде islice().
    value = start
    while value <= limit:
        if isinstance(value, float) and not isfinite(value):
            return  # Зупиняємося при переповненні float.
        yield value
        value *= ratio


def fibonacci(n: int | None = None):
    if n is not None:
        n = index(n)
        if n < 0:
            raise ValueError("Кількість чисел має бути невід'ємною.")
    a, b = 0, 1
    produced = 0
    while n is None or produced < n:
        yield a
        a, b = b, a + b
        produced += 1


def collatz_sequence(n: int):
    n = index(n)
    if n < 1:
        raise ValueError("Початкове число має бути додатним цілим.")
    while True:
        yield n
        if n == 1:
            return
        n = n // 2 if n % 2 == 0 else 3 * n + 1


def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)  # Делегуємо обхід вкладеного списку.
        else:
            yield item


def main():
    ap = arithmetic_progression(2, 3)
    gp = geometric_progression(1, 2, limit=1000)
    print("Арифметична прогресія:", list(islice(ap, 10)))
    print("Геометрична прогресія:", list(gp))
    print("Фібоначчі (15):", list(fibonacci(15)))

    # Довжина і максимум обчислюються за один прохід без списку значень.
    length, maximum = 0, 0
    for value in collatz_sequence(27):
        length += 1
        maximum = max(maximum, value)
    print(f"Коллатц (27): довжина={length}, макс={maximum}")

    nested = [1, [2, 3], [4, [5, 6]], 7, [8, [9, [10]]]]
    print("Розгортання:", list(flatten(nested)))
    for value in fibonacci():
        if value > 10_000:
            print(f"Перше число Фібоначчі > 10000: {value}")
            break


if __name__ == "__main__":
    main()
