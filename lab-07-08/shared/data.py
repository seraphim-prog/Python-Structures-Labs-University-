from datetime import date


LEVELS = [
    ("beginner", "Початковий"),
    ("intermediate", "Середній"),
    ("advanced", "Поглиблений"),
]
ENROLLMENT_STATES = [("pending", "Очікує підтвердження"), ("confirmed", "Підтверджено")]

TOPICS = [
    ("git", "Git", "Керування версіями та командна робота"),
    ("python", "Python", "Розробка застосунків мовою Python"),
    ("web", "Веброзробка", "Інтерфейси та серверна логіка"),
]
WORKSHOPS = [
    ("python-data", "Робота з даними у Python", date(2026, 11, 27), 90, True, ["python"]),
    ("team-git", "Командна робота з Git", date(2026, 11, 30), 60, True, ["git"]),
    ("web-forms", "Форми у вебзастосунках", date(2026, 12, 3), 120, False, ["python", "web"]),
]
PARTICIPANTS = [
    ("olena@example.com", "Олена Коваль", "Київ"),
    ("taras@example.com", "Тарас Бондар", "Львів"),
]
ENROLLMENTS = [
    ("olena@example.com", "python-data"),
    ("taras@example.com", "python-data"),
    ("taras@example.com", "team-git"),
]
