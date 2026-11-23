# ПР №6–7. Маршрутизація, CRUD та REST API у Flask

Дем’янчук Сєрафім Сергійович, група БІКСб-12540.

Блог, контролери товарів, серверна сесія і дві версії API студентів працюють в одному Flask-застосунку. Початкові публікації, товари й студенти задані в `data.py`. Зміни цих записів зберігаються в пам’яті до перезапуску.

## Запуск у Visual Studio або VS Code

Потрібен Python 3.10 або новіший. Відкрийте розпаковану папку `practice-06-07-flask-rest` і виконайте в PowerShell.

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Відкрийте [http://127.0.0.1:5000/](http://127.0.0.1:5000/). У Linux і macOS використовуйте `python3 -m venv .venv` та `.venv/bin/python`. Сервер можна зупинити через Ctrl+C.

## Контрольні запити в терміналі

У другому PowerShell відкрийте ту саму папку. Кожна команда підіймає окремий локальний сервер із початковими записами, надсилає реальні запити через `curl.exe` або `curl` та зупиняє сервер. Перший сервер може залишатися запущеним.

```powershell
.\.venv\Scripts\python.exe demo_http.py items
.\.venv\Scripts\python.exe demo_http.py session
.\.venv\Scripts\python.exe demo_http.py students
.\.venv\Scripts\python.exe demo_http.py v2
```

Для всіх чотирьох сценаріїв однією командою використайте `demo_http.py all`. Потрібен встановлений `curl.exe` або `curl`. Скрипт показує HTTP-статуси й перевірені дані з відповідей.

Окремі запити до Flask, запущеного через `app.py`.

```powershell
curl.exe -i "http://127.0.0.1:5000/api/items?max_price=5000&sort=price"
curl.exe -i "http://127.0.0.1:5000/api/students?min_gpa=90&sort_by=gpa&order=desc&per_page=1"
curl.exe -i "http://127.0.0.1:5000/api/v2/students?fields=name,gpa&sort=gpa&order=desc&per_page=1" -H "Origin: http://127.0.0.1:5500"
'{"name":"Demo Student","group":"KI-23","email":"demo@example.org","gpa":91}' | curl.exe -i -H "Content-Type: application/json" --data-binary '@-' http://127.0.0.1:5000/api/students
```

## Перевірка блогу

1. Відкрийте `/posts?page=2&per_page=2` на початкових даних. З’явиться «Сторінка 2 з 2».
2. Відкрийте `/search?q=Flask`, `/archive/2026/11` і профіль автора за посиланням у картці.
3. Створіть публікацію «Перевірка CRUD» з автором «Олена» та змістом «Публікацію додано через HTML-форму.». Сервер перенаправить на деталі й покаже підтвердження.
4. Змініть назву на «Перевірка CRUD — оновлено». Перейдіть до підтвердження видалення, а після видалення відкрийте стару адресу й перевірте 404.

## Cookies та сесія

Тема й мова зберігаються в cookies з атрибутами Max-Age, HttpOnly і SameSite. Сесія Flask-Session зберігає кошик, ім’я демонстраційного користувача й CSRF-токен у кеші `instance/sessions/`. Браузер отримує ідентифікатор `p067_sid`. Для форм зі зміною стану застосовано POST і CSRF-токен.

Для тестового POST до `/api/v2/students` скрипт `demo_http.py v2` сам створює тимчасовий ключ. Щоб задати власний ключ серверу, встановіть змінну середовища `PRACTICE_API_KEY` перед запуском. Якщо ключ ще не задано, захищений POST повертає 401. Для сталого підпису токенів можна задати `PRACTICE_SECRET_KEY`. Заголовок CORS додається для дозволеного джерела `http://127.0.0.1:5500`, яке можна змінити через `PRACTICE_CORS_ORIGIN`.

## Файли за завданнями

| Завдання | Файли |
| --- | --- |
| 1.1. GET/POST-маршрути | `blog.py`, `templates/` |
| 1.2. Контролери товарів | `items.py`, `common.py` |
| 1.3. Cookies і sessions | `account.py`, `app.py`, `templates/account.html` |
| 2.1. Створення й перегляд | `blog.py`, `templates/listing.html`, `templates/post_form.html`, `templates/post.html` |
| 2.2. Редагування й видалення | `blog.py`, `templates/delete.html`, `templates/post_form.html` |
| 3.1. REST API студентів | `students.py`, `store.py` |
| 3.2. Серіалізація та API v2 | `students.py`, `common.py`, `app.py` |

## API

| Метод | URL | Результат | Коди |
| --- | --- | --- | --- |
| GET | `/api/items` | Товари, фільтр за категорією й ціною, сортування | 200, 400 |
| POST | `/api/items` | Створення товару | 201, 400 |
| GET | `/api/items/<id>` | Деталі товару | 200, 404 |
| PUT | `/api/items/<id>` | Повна заміна полів товару | 200, 400, 404 |
| DELETE | `/api/items/<id>` | Видалення товару | 204, 404 |
| GET | `/api/students` | Список, фільтри `group` і `min_gpa`, пагінація | 200, 400 |
| POST | `/api/students` | Створення студента | 201, 400, 409, 422 |
| GET | `/api/students/<id>` | Деталі студента | 200, 404 |
| PUT | `/api/students/<id>` | Повне оновлення полів студента | 200, 400, 404, 409, 422 |
| PATCH | `/api/students/<id>` | Часткове оновлення | 200, 400, 404, 409, 422 |
| DELETE | `/api/students/<id>` | Видалення студента | 204, 404 |
| GET | `/api/students/stats` | Середній бал, розподіл за групами, топ-3 | 200 |
| GET | `/api/v2/students` | Пошук і вибір полів | 200, 400 |
| POST | `/api/v2/students` | Створення з заголовком `X-API-Key` | 201, 400, 401, 409, 422 |

## GitHub

Додайте папку `practice-06-07-flask-rest` у свій репозиторій з іншими роботами. `.gitignore` виключає локальне середовище, кеш сесій, файли з ключами та cookies.
