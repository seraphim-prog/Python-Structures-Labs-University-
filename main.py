"""П'ять завдань про вбудовані структури даних Python. Без зовнішніх пакетів."""

import argparse
import csv
import json
import platform
import re
import statistics
import sys
import timeit
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SIZES = (100, 1_000, 10_000)
STUDENTS = [
    ("Дем'янчук", "БІКСб-12540", (90, 85, 95)),
    ("Коваль", "БІКСб-12540", (78, 82, 86)),
    ("Мельник", "БІКСб-12540", (100, 92, 96)),
]


def heading(number, title):
    print(f"\nЗАВДАННЯ {number}. {title}\n" + "-" * 65)


def task1():
    heading(1, "Списки")
    numbers = [12, 7, 25, 7, 3, 18, 10, 2]
    original = numbers.copy()
    print("Тип елементів: int")
    print("Початковий список:", numbers)
    print("numbers[2] =", numbers[2])
    print("numbers[-1] =", numbers[-1])
    print("numbers[1:5] =", numbers[1:5])
    print("numbers[::2] =", numbers[::2])
    print("numbers[::-1] =", numbers[::-1])
    same_object = numbers
    numbers.append(30)
    print("Після append(30):", numbers, "довжина =", len(numbers))
    numbers.insert(1, 99)
    print("Після insert(1, 99):", numbers, "довжина =", len(numbers))
    removed = numbers.pop(3)
    print(f"Після pop(3), видалено {removed}:", numbers, "довжина =", len(numbers))
    numbers[2:4] = [44, 55]
    print("Після numbers[2:4] = [44, 55]:", numbers, "довжина =", len(numbers))
    squares = [value ** 2 for value in original if value % 2 == 0]
    print("Квадрати парних чисел початкового списку:", squares)
    print("Об'єкт після мутацій той самий:", numbers is same_object)
    print("Копія початкового списку:", original)


def unpack_student(record):
    surname, group, grades = record
    return surname, group, grades


def average_grade(records):
    total = 0
    count = 0
    for record in records:
        _, _, grades = unpack_student(record)
        total += sum(grades)
        count += len(grades)
    if count == 0:
        raise ValueError("Немає оцінок для обчислення середнього бала.")
    return total / count


def task2():
    heading(2, "Кортежі та розпакування")
    print(f"{'Прізвище':<16} {'Група':<14} Оцінки")
    for record in STUDENTS:
        surname, group, grades = unpack_student(record)
        print(f"{surname:<16} {group:<14} {grades}")
    print(f"Середній бал за всіма 9 оцінками: {average_grade(STUDENTS):.2f} бала зі 100")
    record = STUDENTS[0]
    try:
        record[0] = "Інше прізвище"
    except TypeError as error:
        print("Очікувана помилка TypeError:", error)
    mutable_record = ("Приклад", [80, 90])
    print("Кортеж зі списком до зміни:", mutable_record)
    mutable_record[1].append(100)
    print("Після append(100) до вкладеного списку:", mutable_record)
    print("Посилання в кортежі не замінено; змінено вміст вкладеного списку.")


def tokenize(text):
    text = unicodedata.normalize("NFC", text).casefold()
    text = text.translate(str.maketrans({"’": "'", "ʼ": "'", "‘": "'"}))
    # Літери Unicode; цифри, підкреслення й пунктуація розділяють слова.
    # Апостроф зберігається лише всередині слова.
    return re.findall(r"[^\W\d_]+(?:'[^\W\d_]+)*", text)


def count_words(text):
    frequencies = {}
    for word in tokenize(text):
        frequencies[word] = frequencies.get(word, 0) + 1
    return frequencies


def task3(text_path, output_dir, threshold):
    heading(3, "Словники та частоти слів")
    text = text_path.read_text(encoding="utf-8-sig")
    print("Файл:", text_path)
    print("Вхідний текст:\n" + text.strip())
    frequencies = count_words(text)
    print("\nЗа ключем (порядок Unicode):")
    for word, count in sorted(frequencies.items()):
        print(f"{word:<18} {count}")
    by_frequency = sorted(frequencies.items(), key=lambda item: (-item[1], item[0]))
    print("\nЗа спаданням частоти, при рівності - за ключем:")
    for word, count in by_frequency:
        print(f"{word:<18} {count}")
    missing_key = "відсутнє_слово"
    print(f"Безпечний пошук {missing_key!r}:", frequencies.get(missing_key, 0))
    frequent = {word: count for word, count in frequencies.items() if count >= threshold}
    print(f"Dict comprehension, частота >= {threshold}:", dict(sorted(frequent.items())))
    print("Усього слів:", sum(frequencies.values()), "; різних слів:", len(frequencies))
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "frequencies.tsv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t")
        writer.writerow(["word", "count"])
        writer.writerows(by_frequency)
    print("Результат:", output_dir / "frequencies.tsv")


def task4():
    heading(4, "Множини")
    first = [101, 102, 103, 103, 105, 106]
    second = [103, 104, 104, 105, 107]
    third = [103, 105, 105]
    a, b, c = set(first), set(second), set(third)
    print("Вхід A:", first, "; унікальні:", sorted(a))
    print("Вхід B:", second, "; унікальні:", sorted(b))
    print("Вхід C:", third, "; унікальні:", sorted(c))
    print("Перетин A & B:", sorted(a & b))
    print("Об'єднання A | B:", sorted(a | b))
    print("Різниця A - B:", sorted(a - b))
    print("Симетрична різниця A ^ B:", sorted(a ^ b))
    print("C є підмножиною A:", c <= a)
    print("B є підмножиною A:", b <= a)
    access_profiles = {frozenset({"read", "write"}): "редактор"}
    print("Frozenset як ключ:", access_profiles[frozenset({"write", "read"})])


def unique_with_list(values):
    result = []
    for value in values:
        if value not in result:
            result.append(value)
    return result


def unique_with_set(values):
    result = set()
    for value in values:
        result.add(value)
    return result


def task5(output_dir, repeats):
    heading(5, "Вимірювання алгоритмічної складності")
    output_dir.mkdir(parents=True, exist_ok=True)
    rows, raw_rows = [], []
    print(f"Повторів: {repeats}. У таблиці - мікросекунди на одну операцію.")
    print("Для unique_* одна операція означає повний прохід по n елементах.")
    print(f"{'n':>7} {'Операція':<14} {'Середнє, мкс':>14} {'Мін, мкс':>12} {'Макс, мкс':>12}")
    for n in SIZES:
        sequence = list(range(n))
        value_set = set(sequence)
        mapping = dict.fromkeys(sequence, True)
        target = n - 1  # Наявний елемент наприкінці списку: повний пошук.
        values = [i // 2 for i in range(n)]  # Кожне значення зустрічається двічі.
        context = {"sequence": sequence, "value_set": value_set, "mapping": mapping,
                   "target": target, "values": values,
                   "unique_with_list": unique_with_list, "unique_with_set": unique_with_set}
        operations = [
            ("list_in", "target in sequence", 10_000),
            ("set_in", "target in value_set", 10_000),
            ("dict_in", "target in mapping", 10_000),
            ("unique_list", "unique_with_list(values)", max(1, 10_000 // n)),
            ("unique_set", "unique_with_set(values)", max(1, 10_000 // n)),
        ]
        # Коректність результатів перевіряємо поза вимірюваним блоком.
        assert set(unique_with_list(values)) == unique_with_set(values)
        for name, statement, loops in operations:
            durations = timeit.repeat(statement, globals=context, number=loops, repeat=repeats)
            per_operation = [duration / loops for duration in durations]
            mean_us = statistics.mean(per_operation) * 1_000_000
            min_us, max_us = min(per_operation) * 1_000_000, max(per_operation) * 1_000_000
            rows.append([n, name, loops, repeats, mean_us, min_us, max_us])
            for index, seconds in enumerate(per_operation, start=1):
                raw_rows.append([n, name, index, loops, seconds])
            print(f"{n:>7} {name:<14} {mean_us:>14.3f} {min_us:>12.3f} {max_us:>12.3f}")
    for filename, headers, data in [
        ("benchmark.csv", ["n", "operation", "loops", "repeats", "mean_us", "min_us", "max_us"], rows),
        ("benchmark_raw.csv", ["n", "operation", "repeat", "loops", "seconds_per_operation"], raw_rows),
    ]:
        with (output_dir / filename).open("w", encoding="utf-8", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow(headers)
            writer.writerows(data)
    metadata = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "implementation": platform.python_implementation(),
        "platform": platform.platform(), "machine": platform.machine(),
        "sizes": list(SIZES), "repeats": repeats, "search_target": "n - 1 (present, last)",
        "unique_input": "[i // 2 for i in range(n)]; n/2 unique values",
        "timer": "timeit default_timer (perf_counter); default GC behaviour",
        "measurement": "setup excluded; mean/min/max per operation; no output inside timer",
    }
    (output_dir / "environment.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\nlist_in: очікуємо O(n); set_in і dict_in: O(1) у середньому.")
    print("unique_list: O(n^2); unique_set: O(n) у середньому для всього проходу.")
    print("Константні витрати, кеш і сторонні процеси впливають на короткі вимірювання.")
    print("CSV і параметри експерименту:", output_dir)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", choices=["all", "1", "2", "3", "4", "5"], default="all",
                        help="номер завдання; типово запускаються всі")
    parser.add_argument("--text", type=Path, default=BASE_DIR / "data" / "text.txt",
                        help="UTF-8 файл для завдання 3")
    parser.add_argument("--output", type=Path, default=BASE_DIR / "results",
                        help="каталог результатів")
    parser.add_argument("--threshold", type=int, default=2, help="мінімальна частота слова")
    parser.add_argument("--repeats", type=int, default=5, help="повтори вимірювань, мінімум 3")
    args = parser.parse_args()
    if args.threshold < 1:
        parser.error("--threshold має бути не менше 1")
    if args.repeats < 3:
        parser.error("--repeats має бути не менше 3")
    tasks = {"1": task1, "2": task2,
             "3": lambda: task3(args.text, args.output, args.threshold),
             "4": task4, "5": lambda: task5(args.output, args.repeats)}
    try:
        for number, action in tasks.items():
            if args.task in ("all", number):
                action()
    except (OSError, UnicodeError) as error:
        print(f"Помилка роботи з файлом: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    raise SystemExit(main())
