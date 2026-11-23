"""Програма майстер-класів і спільні параметри форми."""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Workshop:
    key: str
    track: str
    title: str
    summary: str
    day: date
    start: str
    minutes: int

    @property
    def date_label(self) -> str:
        months = ("", "січня", "лютого", "березня", "квітня", "травня", "червня",
                  "липня", "серпня", "вересня", "жовтня", "листопада", "грудня")
        return f"{self.day.day} {months[self.day.month]}"


WORKSHOPS = (
    Workshop(
        "python", "Python", "Робота з даними у Python",
        "Прочитаємо таблицю з файлу CSV, згрупуємо записи й обчислимо підсумки.",
        date(2026, 11, 27), "17:00", 90,
    ),
    Workshop(
        "git", "Git", "Командна робота з Git",
        "Створимо гілку, оформимо зміни в коміт і розв’яжемо конфлікт злиття.",
        date(2026, 11, 30), "17:00", 90,
    ),
    Workshop(
        "web", "Веброзробка", "Форми у вебзастосунках",
        "Побудуємо форму та навчимося показувати серверні помилки біля відповідних полів.",
        date(2026, 12, 3), "17:00", 120,
    ),
)
WORKSHOP_BY_KEY = {workshop.key: workshop for workshop in WORKSHOPS}
WORKSHOP_CHOICES = [
    ("", "Оберіть майстер-клас"),
    *((workshop.key, workshop.title) for workshop in WORKSHOPS),
]

NAME_MIN = 3
NAME_MAX = 60
EMAIL_MAX = 254
MOTIVATION_MIN_WORDS = 5
MOTIVATION_MAX = 360

NAME_LABEL = "Ім’я та прізвище"
EMAIL_LABEL = "Електронна пошта"
WORKSHOP_LABEL = "Майстер-клас"
MOTIVATION_LABEL = "Мотивація"
NAME_REQUIRED = "Введіть ім’я та прізвище."
NAME_LENGTH = f"Ім’я та прізвище мають містити від {NAME_MIN} до {NAME_MAX} символів."
EMAIL_REQUIRED = "Введіть електронну пошту."
EMAIL_INVALID = "Введіть коректну електронну адресу."
EMAIL_LENGTH = f"Електронна адреса має містити до {EMAIL_MAX} символів."
WORKSHOP_REQUIRED = "Оберіть майстер-клас зі списку."
MOTIVATION_REQUIRED = "Коротко опишіть, чому хочете взяти участь."
MOTIVATION_LENGTH = f"Мотивація має містити до {MOTIVATION_MAX} символів."
MOTIVATION_SHORT = f"Напишіть щонайменше {MOTIVATION_MIN_WORDS} слів."
MOTIVATION_HINT = f"Від {MOTIVATION_MIN_WORDS} слів до {MOTIVATION_MAX} символів."


def has_enough_words(text: str) -> bool:
    return len(text.split()) >= MOTIVATION_MIN_WORDS


def page_context(page: str, title: str) -> dict:
    return {
        "page": page,
        "page_title": title,
        "year": date.today().year,
        "workshops": list(WORKSHOPS),
        "workshop_count": len(WORKSHOPS),
    }


def success_message(name: str, workshop_key: str) -> str:
    workshop = WORKSHOP_BY_KEY[workshop_key]
    return f"«{workshop.title}» · {name}"
