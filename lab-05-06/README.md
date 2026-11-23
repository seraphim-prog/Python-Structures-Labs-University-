# ЛБ №5–6. Шаблони, форми та валідація в Django і Flask

**Практикум** показує програму майстер-класів і дає змогу перевірити заявку на заняття. Версії Django та Flask-WTF реалізують однакові сторінки й правила форми. Дані програми і CSS спільні. Для запуску бази даних не потрібно.

## Запуск у Windows

Потрібен Python 3.10 або новіший. Відкрийте папку `lab-05-06-web-forms` у VS Code. Виконуйте команди з цієї папки у двох терміналах PowerShell.

**Django** — [127.0.0.1:8000](http://127.0.0.1:8000/)

```powershell
py -3 -m venv .venv-django
.\.venv-django\Scripts\python.exe -m pip install -r django_app/requirements.txt
.\.venv-django\Scripts\python.exe -m django_app.manage runserver 127.0.0.1:8000
```

**Flask** — [127.0.0.1:5000](http://127.0.0.1:5000/)

```powershell
py -3 -m venv .venv-flask
.\.venv-flask\Scripts\python.exe -m pip install -r flask_app/requirements.txt
.\.venv-flask\Scripts\python.exe -m flask --app flask_app.app run --host 127.0.0.1 --port 5000
```

## Запуск у Linux або macOS

```bash
python3 -m venv .venv-django
.venv-django/bin/python -m pip install -r django_app/requirements.txt
.venv-django/bin/python -m django_app.manage runserver 127.0.0.1:8000
```

```bash
python3 -m venv .venv-flask
.venv-flask/bin/python -m pip install -r flask_app/requirements.txt
.venv-flask/bin/python -m flask --app flask_app.app run --host 127.0.0.1 --port 5000
```

Для локального запуску кожна програма генерує випадковий секретний ключ і тримає його в пам’яті. Для стабільного ключа між перезапусками задайте `DJANGO_SECRET_KEY` або `FLASK_SECRET_KEY` у середовищі. Сервери розробки запускаються на `127.0.0.1`.

## Сторінки та контрольні приклади

| URL | Призначення |
| --- | --- |
| `/` | Огляд і розклад занять |
| `/workshops/` | Програма з датою, часом і тривалістю кожного майстер-класу |
| `/apply/` | Форма заявки. Посилання з програми попередньо вибирає заняття |

- Введіть `Олена Коваль`, адресу `olena.example.com`, оберіть «Форми у вебзастосунках» і додайте мотивацію `Хочу навчитись.`. Помилки адреси й мотивації з’являться поруч із полями. Решта введення збережеться у формі.
- Виправте адресу на `olena@example.com`, а мотивацію на `Хочу навчитися перевіряти дані вебформ на сервері.`. Після перенаправлення з’явиться одноразове підтвердження. Це демонстраційна заявка з перевіркою й підтвердженням у поточному сеансі.
- Для перевірки CSRF на локальних серверах виконайте наведені команди. Django повертає 403, Flask повертає 400. У Linux або macOS використовуйте `curl` замість `curl.exe`.

```powershell
curl.exe -s -o NUL -w "Django HTTP %{http_code}\n" -X POST http://127.0.0.1:8000/apply/
curl.exe -s -o NUL -w "Flask HTTP %{http_code}\n" -X POST http://127.0.0.1:5000/apply/
```

Для цих команд у Linux або macOS замініть також `NUL` на `/dev/null`.

## Структура

| Каталог | Вміст |
| --- | --- |
| `django_app/config/` | Налаштування, middleware та маршрути Django |
| `django_app/workshops/` | Зареєстрований застосунок, представлення, форма та шаблони DTL |
| `flask_app/` | Фабрика застосунку, маршрути, форма Flask-WTF і шаблони Jinja |
| `shared/` | Програма занять, параметри валідації й CSS |

Кожна версія має свій `requirements.txt`. В обох версіях потрібен вихідний каталог `shared/`.
