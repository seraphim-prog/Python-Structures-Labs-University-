"""Факторіал, гармонічна сума і таблиця множення."""


def factorial(n: int) -> int:
    """Обчислює n! для цілого n ≥ 0."""
    result = 1  # Для n = 0 цикл не виконається, тому 0! = 1.
    for number in range(2, n + 1):
        result *= number
    return result


def harmonic_sum(n: int) -> float:
    """Сумує n перших членів ряду, включно з порожньою сумою H(0)."""
    result = 0.0
    for index in range(n):
        result += 1 / (index + 1)
    return result


def multiplication_table(n: int) -> None:
    if n == 0:
        print("Порожня таблиця.")
        return
    width = len(str(n * n)) + 1  # Ширина за найбільшим добутком і пробілом.
    for row in range(1, n + 1, 1):
        for column in range(1, n + 1):
            print(f"{row * column:>{width}d}", end="")
        print()


def main():
    try:
        n = int(input("Введіть ціле n (n ≥ 0): "))
    except ValueError:
        print("Помилка: n має бути цілим числом.")
        return
    except EOFError:
        print("Введення завершено.")
        return
    if n < 0:
        print("Помилка: n має бути невід'ємним.")
        return

    print(f"{n}! = {factorial(n)}")
    print(f"Гармонічна сума H({n}) = {harmonic_sum(n):.6f}")
    print(f"Таблиця множення {n}×{n}:")
    multiplication_table(n)


if __name__ == "__main__":
    main()
