# ПР №5. Ініціалізація та конфігурація Django й Flask

Дем’янчук Сєрафім Сергійович, група БІКСб-12540.

Два локальні проєкти, скрипти перевірки Python, відтворення залежностей, аналізу Django settings і порівняння файлової структури. Для запуску потрібен Python 3.10 або новіший.

## Перше середовище

Відкрийте каталог `practice-05-web-config` у Visual Studio або VS Code. У терміналі PowerShell виконайте команди по черзі.

```powershell
py -3 -m venv venv
.\venv\Scripts\Activate.ps1
where.exe python
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python practical_05_task_1_1.py
python -m pip freeze
python -m pip freeze | Set-Content -Encoding ascii requirements.txt
```

`where.exe python` має першим показати шлях до `venv\Scripts\python.exe`. Якщо PowerShell не може виконати `Activate.ps1`, відкрийте вкладку Command Prompt у цій папці, запустіть `venv\Scripts\activate.bat` і використайте `python -m pip freeze > requirements.txt`.

У файлі зафіксовані Django, Flask і точні версії залежностей. `tzdata` забезпечує часовий пояс на Windows. `colorama` входить до набору для обох середовищ і підтримує роботу Click на Windows.

## Друге середовище

Виконайте в тому ж терміналі.

```powershell
deactivate
py -3 -m venv venv2
.\venv2\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python practical_05_task_1_2.py
```

Скрипт читає JSON від `pip list --format=json` в обох середовищах. Він порівнює назви й версії з `requirements.txt` та повідомляє про відсутні, зайві або невідповідні пакети. Запустіть `python practical_05_task_1_2.py --generate`, щоб записати залежності з поточного середовища. У Command Prompt для другого середовища команда активації має вигляд `venv2\Scripts\activate.bat`.

У Linux і macOS використовуйте `python3 -m venv venv`, `source venv/bin/activate`, `which python` та `python -m pip freeze > requirements.txt`. Для другого середовища замініть `venv` на `venv2`.

## Django

В окремому терміналі з кореня проєкту запустіть сервер.

```powershell
.\venv\Scripts\python.exe .\mysite\manage.py migrate
.\venv\Scripts\python.exe .\mysite\manage.py runserver 127.0.0.1:8000
```

| URL | Результат |
| --- | --- |
| `http://127.0.0.1:8000/` | Головна сторінка з трьома пунктами |
| `http://127.0.0.1:8000/about/` | Дисципліна, номер роботи, студент і група |
| `http://127.0.0.1:8000/contact/` | Форма введення імені |
| `http://127.0.0.1:8000/contact/?name=Сєрафім` | «Вітаю, Сєрафім!» |

У `settings.py` встановлено `LANGUAGE_CODE = "uk"` і `TIME_ZONE = "Europe/Kyiv"`. Додаток `pages` зареєстровано через `PagesConfig`, а маршрути підключено через `include()`. SQLite створюється під час `migrate`. Для локального сервера `DEBUG` увімкнено, а `ALLOWED_HOSTS` містить локальні адреси. Ключ читається з `DJANGO_SECRET_KEY` або генерується на поточний запуск.

## Flask

Відкрийте ще один термінал у корені проєкту.

```powershell
.\venv\Scripts\python.exe -m myflaskapp.app
```

| URL | Результат |
| --- | --- |
| `http://127.0.0.1:5000/` | Головна сторінка з маршрутами |
| `http://127.0.0.1:5000/about` | Інформація про застосунок і студента |
| `http://127.0.0.1:5000/api/info` | JSON із версією, DEBUG і маршрутами |
| `http://127.0.0.1:5000/greet/Сєрафім` | Параметр імені зі шляху |
| `http://127.0.0.1:5000/greet?name=Сєрафім` | Параметр імені з рядка запиту |

`create_app()` обирає конфігурацію і реєструє blueprint `pages`. Режим development може згенерувати ключ у пам’яті. Для створення екземпляра в режимі production значення `FLASK_SECRET_KEY` задають у змінних середовища.

Під Linux або macOS для команд запуску серверів використовуйте `venv/bin/python mysite/manage.py` та `venv/bin/python -m myflaskapp.app`. Сервери зупиняються через Ctrl+C.

## Аналіз проєктів

У терміналі з активним середовищем виконайте.

```powershell
python practical_05_task_2_2.py
python practical_05_task_3_2.py
```

- Аналіз Django показує локалізацію, SQLite, шаблони, middleware і список встановлених додатків. Перевірки охоплюють DEBUG, джерело ключа та ALLOWED_HOSTS. У локальному профілі очікується одне попередження про DEBUG. Аналізатор читає AST файлу.
- Аналіз структур друкує дерево кожного проєкту і порівнює кількість файлів Python, HTML і CSS, кількість каталогів і загальний розмір. З обліку вилучено приховані й службові файли, кеш, віртуальні середовища та локальну БД.

Для GitHub додайте каталог `practice-05-web-config` у репозиторій курсу. `.gitignore` виключає середовища, базу, файли з ключами та кеші.
