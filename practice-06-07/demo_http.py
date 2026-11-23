"""Виконує контрольні запити curl до окремого локального Flask-сервера."""

import argparse
import json
import logging
import re
import shutil
import subprocess
from http.client import parse_headers
from io import BytesIO
from pathlib import Path
from secrets import token_urlsafe
from tempfile import TemporaryDirectory
from threading import Thread
from urllib.parse import unquote, urlencode

from cachelib.file import FileSystemCache
from werkzeug.serving import WSGIRequestHandler, make_server

from app import create_app


class QuietHandler(WSGIRequestHandler):
    def log_request(self, *_args, **_kwargs):
        pass


class Curl:
    def __init__(self, executable, base):
        self.executable = executable
        self.base = base

    def send(self, method, path, expected, *, data=None, form=None, jar=None, key=None,
             origin=None, quiet=False):
        args = [self.executable, "--silent", "--show-error", "--include", "--http1.1",
                "--noproxy", "*", "--max-time", "5", "-X", method]
        headers = {}
        body = None
        if data is not None:
            headers["Content-Type"] = "application/json"
            body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        if form is not None:
            headers["Content-Type"] = "application/x-www-form-urlencoded"
            body = urlencode(form).encode("ascii")
        if key is not None:
            headers["X-API-Key"] = key
        if origin is not None:
            headers["Origin"] = origin
        for name, value in headers.items():
            args.extend(["-H", f"{name}: {value}"])
        if body is not None:
            args.extend(["--data-binary", "@-"])
        if jar is not None:
            args.extend(["--cookie", str(jar), "--cookie-jar", str(jar)])
        result = subprocess.run([*args, self.base + path], input=body, capture_output=True, check=True)
        header_block, _, payload = result.stdout.partition(b"\r\n\r\n")
        status_line, _, raw_headers = header_block.partition(b"\r\n")
        actual = int(status_line.split()[1])
        if not quiet:
            print(f"{method} {unquote(path)}  →  HTTP {actual}")
        if actual != expected:
            raise RuntimeError(f"{method} {path}: очікувалося {expected}, отримано {actual}")
        return parse_headers(BytesIO(raw_headers)), payload


def show(data):
    print("  " + json.dumps(data, ensure_ascii=False))


def check_items(curl):
    path = "/api/items"
    print("\n1.2  Контролери товарів")
    query = urlencode({"category": "електроніка", "max_price": 5000, "sort": "price"})
    _, body = curl.send("GET", f"{path}?{query}", 200)
    filtered = json.loads(body)
    assert filtered["count"] == 1 and filtered["items"][0]["name"] == "Навушники"
    show({"count": filtered["count"], "name": filtered["items"][0]["name"]})
    data = {"name": "Мікрофон", "price": 1700, "category": "електроніка"}
    headers, body = curl.send("POST", path, 201, data=data)
    target = headers["Location"]
    show(json.loads(body))
    curl.send("GET", target, 200)
    _, body = curl.send("PUT", target, 200, data=data | {"price": 1800})
    assert json.loads(body)["price"] == 1800
    show({"price": json.loads(body)["price"]})
    _, body = curl.send("POST", path, 400, data={"name": "Неповний запис"})
    show(json.loads(body)["details"])
    _, empty = curl.send("DELETE", target, 204)
    assert not empty
    curl.send("GET", target, 404)


def check_session(curl, folder):
    print("\n1.3  Cookie та серверна сесія")
    jar = folder / "cookies.txt"
    curl.send("GET", "/profile", 302)
    _, page = curl.send("GET", "/login", 200, jar=jar, quiet=True)
    token = re.search(rb'name="csrf_token" type="hidden" value="([^"]+)"', page)[1].decode()
    form = {"csrf_token": token}
    headers, _ = curl.send("POST", "/set-theme/dark", 302, form=form, jar=jar)
    theme_cookie = next(value for value in headers.get_all("Set-Cookie") if value.startswith("theme="))
    assert all(flag in theme_cookie for flag in ("Max-Age=2592000", "HttpOnly", "SameSite=Lax"))
    print("  theme=dark | Max-Age=2592000 | HttpOnly | SameSite=Lax")
    curl.send("POST", "/set-language/en", 302, form=form, jar=jar)
    _, body = curl.send("GET", "/preferences", 200, jar=jar)
    prefs = json.loads(body)
    assert prefs == {"theme": "dark", "language": "en"}
    show(prefs)
    curl.send("POST", "/cart/add/3", 302, form=form, jar=jar)
    _, body = curl.send("GET", "/cart", 200, jar=jar)
    cart = json.loads(body)
    assert cart["items"][0]["id"] == 3 and cart["total"] == 2000
    show(cart)
    curl.send("POST", "/login", 302, form=form | {"username": "Олена"}, jar=jar)
    _, body = curl.send("GET", "/profile", 200, jar=jar)
    account = json.loads(body)
    assert account == {"username": "Олена", "authenticated": True}
    show(account)
    curl.send("POST", "/cart/clear", 302, form=form, jar=jar, quiet=True)
    _, body = curl.send("GET", "/cart", 200, jar=jar, quiet=True)
    assert json.loads(body) == {"items": [], "total": 0}
    curl.send("POST", "/logout", 302, form=form, jar=jar)
    curl.send("GET", "/profile", 302, jar=jar)


def check_students(curl):
    print("\n3.1  REST API студентів")
    path = "/api/students"
    query = urlencode({"group": "КІ-21", "min_gpa": 80, "sort_by": "gpa", "order": "desc",
                       "page": 1, "per_page": 1})
    _, body = curl.send("GET", f"{path}?{query}", 200)
    page = json.loads(body)
    assert page["count"] == 2 and page["students"][0]["gpa"] == 92.0
    show({"count": page["count"], "page": page["page"], "per_page": page["per_page"],
          "name": page["students"][0]["name"], "gpa": page["students"][0]["gpa"]})
    _, body = curl.send("GET", f"{path}/stats", 200)
    stats = json.loads(body)
    assert stats["total"] == 4 and stats["top_students"][0]["gpa"] == 95.1
    show({field: stats[field] for field in ("total", "avg_gpa", "groups")})
    data = {"name": "Олена Тестова", "group": "КІ-21", "email": "olena@example.com", "gpa": 88.0}
    headers, _ = curl.send("POST", path, 201, data=data)
    target = headers["Location"]
    curl.send("GET", target, 200)
    curl.send("PUT", target, 200, data=data | {"gpa": 91.0})
    _, body = curl.send("PATCH", target, 200, data={"gpa": 96})
    student = json.loads(body)
    assert student["gpa"] == 96 and student["email"] == data["email"] and student["honor_roll"]
    show({field: student[field] for field in ("name", "gpa", "honor_roll")})
    curl.send("POST", path, 409, data=data)
    curl.send("PATCH", target, 422, data={"gpa": 101})
    _, empty = curl.send("DELETE", target, 204)
    assert not empty
    curl.send("GET", target, 404)


def check_v2(curl, key):
    print("\n3.2  Серіалізація, заголовки та API-ключ")
    path = "/api/v2/students"
    origin = "http://127.0.0.1:5500"
    query = urlencode({"fields": "name,gpa", "search": "Іван", "sort": "gpa", "order": "desc"})
    headers, body = curl.send("GET", f"{path}?{query}", 200, origin=origin)
    matches = json.loads(body)["students"]
    assert matches == [{"name": "Іваненко О.", "gpa": 85.5}]
    assert headers["Access-Control-Allow-Origin"] == origin and headers["X-Request-Time"]
    show(matches)
    print(f"  X-Request-Time: {headers['X-Request-Time']}")
    print(f"  Access-Control-Allow-Origin: {origin}")
    data = {"name": "Олена API", "group": "КІ-22", "email": "olena.api@example.com", "gpa": 91}
    _, body = curl.send("POST", path, 401, data=data)
    show(json.loads(body)["error"])
    _, body = curl.send("POST", path, 201, data=data, key=key)
    student = json.loads(body)
    show({field: student[field] for field in ("id", "name", "gpa", "honor_roll")})
    _, body = curl.send("POST", path, 422, data=data | {"gpa": 101}, key=key)
    problem = json.loads(body)
    assert set(problem) == {"error", "status", "details", "timestamp"}
    show({field: problem[field] for field in ("status", "error", "details")})


def main():
    parser = argparse.ArgumentParser(description="Демонстрація HTTP-запитів на локальному сервері")
    parser.add_argument("section", choices=["items", "session", "students", "v2", "all"],
                        nargs="?", default="all")
    section = parser.parse_args().section
    executable = shutil.which("curl.exe") or shutil.which("curl")
    if executable is None:
        parser.exit(2, "Потрібен встановлений curl або curl.exe.\n")
    with TemporaryDirectory(prefix="practice0607-") as folder_name:
        folder = Path(folder_name)
        key = token_urlsafe(25)
        app = create_app({"PRACTICE_API_KEY": key,
                          "PRACTICE_CORS_ORIGIN": "http://127.0.0.1:5500",
                          "SESSION_CACHELIB": FileSystemCache(str(folder / "sessions"))})
        app.logger.setLevel(logging.WARNING)
        with make_server("127.0.0.1", 0, app, request_handler=QuietHandler) as server:
            worker = Thread(target=server.serve_forever, daemon=True)
            worker.start()
            curl = Curl(executable, f"http://127.0.0.1:{server.server_port}")
            scenarios = {"items": lambda: check_items(curl), "session": lambda: check_session(curl, folder),
                         "students": lambda: check_students(curl), "v2": lambda: check_v2(curl, key)}
            try:
                for run in (scenarios.values() if section == "all" else (scenarios[section],)):
                    run()
                print("\nПеревірку завершено. Усі очікувані відповіді отримано.")
            finally:
                server.shutdown()
                worker.join()


if __name__ == "__main__":
    main()
