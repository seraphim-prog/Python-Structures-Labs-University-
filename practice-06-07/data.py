"""Початкові записи для локального запуску практичної роботи."""

POSTS = [
    {"title": "Вступ до Python", "author": "Іван",
     "content": "Перші програми з умовами, циклами та функціями.",
     "created_at": "2026-11-01T09:00:00+00:00"},
    {"title": "Flask для початківців", "author": "Марія",
     "content": "Маршрути зіставляють адреси з функціями, які формують відповідь.",
     "created_at": "2026-11-05T09:00:00+00:00"},
    {"title": "REST API", "author": "Петро",
     "content": "HTTP-методи визначають операцію, а JSON передає дані ресурсу.",
     "created_at": "2026-11-10T09:00:00+00:00"},
    {"title": "Робота з HTML-формами", "author": "Марія",
     "content": "Сервер перевіряє дані форми перед створенням запису.",
     "created_at": "2026-10-28T09:00:00+00:00"},
]

ITEMS = [
    {"name": "Ноутбук", "price": 25000.0, "category": "електроніка"},
    {"name": "Книга Python", "price": 500.0, "category": "книги"},
    {"name": "Навушники", "price": 2000.0, "category": "електроніка"},
]

STUDENTS = [
    {"name": "Іваненко О.", "group": "КІ-21", "email": "ivan@example.com", "gpa": 85.5},
    {"name": "Петренко М.", "group": "КІ-21", "email": "petro@example.com", "gpa": 92.0},
    {"name": "Сидоренко А.", "group": "КІ-22", "email": "syd@example.com", "gpa": 78.3},
    {"name": "Коваль Л.", "group": "КІ-22", "email": "koval@example.com", "gpa": 95.1},
]
for student in STUDENTS:
    student["created_at"] = "2026-11-01T09:00:00+00:00"
