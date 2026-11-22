"""Два конвеєри генераторів для обробки оцінок."""

SAMPLE_DATA = [
    "Олена,Математика,95", "Іван,Математика,78", "", "Марія,Фізика,92",
    "Петро,Математика,INVALID", "Анна,Фізика,88", "Олена,Фізика,90",
    "Іван,Програмування,85", "Марія,Програмування,91", "Петро,Фізика,76",
    "Анна,Математика,93", "Олена,Програмування,97", "", "Марія,Математика,89",
    "Іван,Фізика,72", "Петро,Програмування,80", "Анна,Програмування,86",
]


def data_source(records):
    for line in records:
        yield line


def filter_empty(records):
    for line in records:
        if line.strip():
            yield line


def parse_records(records):
    for line in records:
        try:
            parts = line.split(",")
            student, subject, grade_text = (part.strip() for part in parts)
            grade = int(grade_text)
        except ValueError:
            continue  # Некоректний формат рядка або неціла оцінка.
        if student and subject and 0 <= grade <= 100:
            yield {"student": student, "subject": subject, "grade": grade}


def filter_passed(records, min_grade: int = 60):
    for record in records:
        if record["grade"] >= min_grade:
            yield record


def format_output(records):
    for record in records:
        student = record["student"]
        subject = record["subject"]
        grade = record["grade"]
        yield f"[{subject}] {student}: {grade} балів"


def subject_averages(records):
    # Зберігаємо суму й кількість, а не список усіх оцінок предмета.
    totals = {}
    for record in records:
        subject = record["subject"]
        total, count = totals.get(subject, (0, 0))
        totals[subject] = (total + record["grade"], count + 1)
    for subject in sorted(totals):
        total, count = totals[subject]
        yield subject, total / count, count


def main():
    records = parse_records(filter_empty(data_source(SAMPLE_DATA)))
    print("Результати (від 75 балів):")
    for line in format_output(filter_passed(records, min_grade=75)):
        print(line)

    # Генератор першого конвеєра вичерпано. Для середніх потрібен новий прохід.
    records = parse_records(filter_empty(data_source(SAMPLE_DATA)))
    print("\nСередній бал за предметами (усі коректні оцінки):")
    for subject, average, count in subject_averages(records):
        print(f"  {subject}: {average:.1f} (з {count} оцінок)")


if __name__ == "__main__":
    main()
