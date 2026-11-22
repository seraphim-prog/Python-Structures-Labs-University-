"""Порівняння списку й виразу-генератора."""

import sys
import timeit


def memory_comparison():
    sizes = (1_000, 10_000, 100_000, 1_000_000)
    print(f"{'N':>12} | {'list (байт)':>14} | {'gen (байт)':>12} | {'Ratio':>8}")
    print("-" * 57)
    for n in sizes:
        data_list = [x ** 2 for x in range(n)]
        data_gen = (x ** 2 for x in range(n))
        # getsizeof вимірює сам об'єкт, без об'єктів за його посиланнями.
        list_size = sys.getsizeof(data_list)
        gen_size = sys.getsizeof(data_gen)
        ratio = list_size / gen_size
        print(f"{n:>12,} | {list_size:>14,} | {gen_size:>12,} | {ratio:>7.0f}×")
        del data_list, data_gen


def performance_comparison():
    n, repeats = 500_000, 5
    # timeit повертає суму часу запусків. Ділимо її на кількість запусків.
    list_total = timeit.timeit(
        lambda: sum([x ** 2 for x in range(n)]), number=repeats
    )
    gen_total = timeit.timeit(
        lambda: sum(x ** 2 for x in range(n)), number=repeats
    )
    list_avg, gen_avg = list_total / repeats, gen_total / repeats
    print(f"sum() для {n:,} елементів, середнє з {repeats} запусків:")
    print(f"  list comprehension: {list_avg:.6f} с")
    print(f"  generator expression: {gen_avg:.6f} с")
    faster = "list" if list_avg <= gen_avg else "generator"
    print(f"  Менший виміряний час: {faster}")


def practical_usage():
    words = [
        "Python", "ітератор", "генератор", "yield", "comprehension",
        "дані", "пам'ять", "ефективність", "конвеєр", "ліниві",
        "обчислення", "протокол", "об'єкт", "клас", "функція",
    ]
    longest = max((word for word in words), key=len)
    all_nonempty = all(bool(word) for word in words)
    has_long = any(len(word) > 15 for word in words)
    csv_line = ",".join(word for word in words)
    total_length = sum(len(word) for word in words)
    word_lengths = {word: len(word) for word in words}
    even_squares = sum(x ** 2 for x in range(1, 101) if x % 2 == 0)

    print(f"Найдовше слово: {longest} ({len(longest)} символів)")
    print(f"Усі слова непорожні: {all_nonempty}")
    print(f"Є слово довше за 15 символів: {has_long}")
    print(f"CSV: {csv_line}")
    print(f"Сума довжин слів: {total_length}")
    print(f"Довжини: {word_lengths}")
    print(f"Сума квадратів парних від 1 до 100: {even_squares}")


def main():
    print("Розмір об'єктів за sys.getsizeof():")
    memory_comparison()
    print()
    performance_comparison()
    print("\nВирази-генератори на практиці:")
    practical_usage()


if __name__ == "__main__":
    main()
