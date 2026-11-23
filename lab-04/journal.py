"""Дані навчальної сесії, перевірка введення та експорт журналу."""

import json
from dataclasses import asdict, dataclass

from PyQt6.QtCore import QIODevice, QSaveFile


SUBJECTS = ("Програмування", "Математика", "Кібербезпека", "Інше")
MIN_DURATION = 5
MAX_DURATION = 240
MIN_GOAL = 15
MAX_GOAL = 720


@dataclass(frozen=True, slots=True)
class StudySession:
    topic: str
    subject: str
    minutes: int
    difficulty: int
    completed: bool


@dataclass(frozen=True, slots=True)
class JournalSettings:
    title: str = "Журнал навчальних сесій"
    goal: int = 120


def validate_session(
    topic: str, subject: str, minutes: int, difficulty: int, completed: bool
) -> StudySession:
    """Перевіряє форму і повертає запис, готовий до додавання."""
    topic = topic.strip()
    if not topic:
        raise ValueError("Введіть тему сесії.")
    if not MIN_DURATION <= minutes <= MAX_DURATION:
        raise ValueError(f"Тривалість має бути від {MIN_DURATION} до {MAX_DURATION} хв.")
    return StudySession(topic, subject, minutes, difficulty, completed)


def export_journal(
    path: str, settings: JournalSettings, sessions: tuple[StudySession, ...]
) -> None:
    """Записує параметри та сесії у файл JSON з кодуванням UTF-8."""
    data = {
        "title": settings.title,
        "goal_minutes": settings.goal,
        "sessions": [asdict(session) for session in sessions],
    }
    payload = (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    target = QSaveFile(path)
    if not target.open(QIODevice.OpenModeFlag.WriteOnly):
        raise OSError(target.errorString())
    if target.write(payload) != len(payload):
        error = target.errorString()
        target.cancelWriting()
        raise OSError(error)
    if not target.commit():
        raise OSError(target.errorString())
