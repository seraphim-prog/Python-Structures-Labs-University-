# ЛБ №7–8. Моделі даних і тестування Django та Flask

«Практикум» веде каталог майстер-класів і приймає заявки учасників. Це два самостійні застосунки з однаковою моделлю предметної області. Відносно ЛБ №5–6 додано п’ять моделей, бази SQLite, міграції та автоматизовані тести.

## Запуск у Windows

Потрібен Python 3.10 або новіший. Відкрийте розпаковану папку `lab-07-08-orm-pytest` і виконуйте команди з неї. Для кожної версії використовуйте окремий термінал PowerShell.

### Django

```powershell
py -3 -m venv .venv-django
.\.venv-django\Scripts\python.exe -m pip install -r django_app/requirements.txt
.\.venv-django\Scripts\python.exe -m django_app.manage migrate
.\.venv-django\Scripts\python.exe -m django_app.manage demo_orm
.\.venv-django\Scripts\python.exe -m django_app.manage runserver 127.0.0.1:8000
```

Сторінка програми відкривається за адресою http://127.0.0.1:8000/workshops/.

### Flask

```powershell
py -3 -m venv .venv-flask
.\.venv-flask\Scripts\python.exe -m pip install -r flask_app/requirements.txt
.\.venv-flask\Scripts\python.exe -m flask --app flask_app.app db upgrade
.\.venv-flask\Scripts\python.exe -m flask --app flask_app.app demo-orm
.\.venv-flask\Scripts\python.exe -m flask --app flask_app.app run --port 5000
```

Сторінка програми відкривається за адресою http://127.0.0.1:5000/workshops/.

У Linux і macOS створіть середовища через `python3 -m venv` і замініть шлях до Python на `.venv-django/bin/python` або `.venv-flask/bin/python`.

## Схема та демонстраційні дані

| Проєкт | Файл бази за замовчуванням | Міграції |
| --- | --- | --- |
| Django | `django_app/orm-django.sqlite3` | `django_app/workshops/migrations/` |
| Flask | `instance/orm-flask.sqlite3` | `flask_app/migrations/` |

Flask використовує URI `sqlite:///orm-flask.sqlite3`. Шляхи можна задати через `DJANGO_DB_PATH` і `FLASK_DATABASE_URI`. Для локального запуску ключі створюються в пам’яті. Стабільні ключі можна задати через `DJANGO_SECRET_KEY` або `FLASK_SECRET_KEY`.

Міграції `0001` створюють таблиці учасників, профілів, тем, майстер-класів і заявок та проміжну таблицю тем. Міграції `0002` додають місце проведення `room` із початковим значенням «Онлайн». Переглянути історію можна через `python -m django_app.manage showmigrations workshops` або `python -m flask --app flask_app.app db history`. SQL другої міграції Django показує команда `python -m django_app.manage sqlmigrate workshops 0002`.

Команди демонстрації додають контрольні дані без дублювання, показують CRUD, фільтрацію, зведення і вимірюють кількість SQL-запитів для тем. Flask також демонструє rollback. Числа у звіті отримано на чистих базах. Якщо додати власні заявки, підрахунки зміняться.

Django використовує локальний поштовий бекенд у пам’яті, щоб показати виклик підтвердження після коміту. У Flask дата реєстрації записується під час створення заявки.

## Тести та покриття

У командах нижче `python` означає інтерпретатор відповідного віртуального середовища. Щоб виконати обидва набори з одного середовища, встановіть залежності командою `python -m pip install -r requirements.txt`. Фікстури використовують окремі тестові бази, а модулі міграцій і файли тестів виключені з підрахунку покриття.

```powershell
python -m pytest django_app/tests -c django_app/pytest.ini -v --cov=django_app.workshops --cov-config=.coveragerc --cov-report=term-missing
python -m pytest flask_app/tests -c flask_app/pytest.ini -v --cov=flask_app --cov-config=.coveragerc --cov-report=term-missing
```

Для звичайного тестового запуску відкрийте каталог `django_app/` або `flask_app/` і виконайте `python -m pytest -v` відповідним інтерпретатором. У підкаталогах `tests/` є окремі перевірки моделей, HTTP-маршрутів і моків. Демонстраційний сценарій можна повторити через форму на сторінці заняття. Після коректної заявки кількість записів збільшується, повторне надсилання з тією ж адресою показує повідомлення про наявну заявку.
