"""Ітерабельний контейнер StudentGroup з окремим ітератором."""

from collections import namedtuple
from itertools import islice
from operator import index

Student = namedtuple("Student", ["name", "grade"])


class StudentGroupIterator:
    def __init__(self, students: list[Student]):
        self._students = students
        self._index = 0
        self._limit = len(students)  # Нові записи підхопить наступний обхід.

    def __iter__(self):
        return self

    def __next__(self) -> Student:
        if self._index >= self._limit:
            raise StopIteration
        student = self._students[self._index]
        self._index += 1
        return student


class StudentGroup:
    def __init__(self, group_name: str):
        self._group_name = group_name
        self._students: list[Student] = []

    def add_student(self, name: str, grade: int) -> None:
        self._students.append(Student(name, grade))

    def __iter__(self) -> StudentGroupIterator:
        # Кожен обхід має окремий індекс ітератора.
        return StudentGroupIterator(self._students)

    def __len__(self) -> int:
        return len(self._students)

    def top_students(self, n: int = 3):
        """Повертає ітератор по найвищих оцінках."""
        n = index(n)
        if n < 0:
            raise ValueError("Кількість студентів має бути невід'ємною.")
        ranked = sorted(self._students, key=lambda student: student.grade,
                        reverse=True)
        return islice(ranked, min(n, len(ranked)))


def main():
    group = StudentGroup("КІ-21")
    for name, grade in [("Олена", 95), ("Іван", 78), ("Марія", 92),
                        ("Петро", 85), ("Анна", 88)]:
        group.add_student(name, grade)

    print("Кількість студентів:", len(group))
    for title in ("Перший обхід", "Другий обхід"):
        print(f"{title}:", ", ".join(student.name for student in group))

    first, second = iter(group), iter(group)
    print("Ітератор A:", next(first).name, next(first).name)
    print("Ітератор B (перший крок):", next(second).name)

    print("Усі пари студентів:")
    for i, left in enumerate(group):
        for j, right in enumerate(group):
            if i < j:  # Уникаємо пар із самим собою та дублікатів.
                print(f"  {left.name} та {right.name}")

    print("Топ-3:")
    for student in group.top_students():
        print(f"  {student.name}: {student.grade}")


if __name__ == "__main__":
    main()
