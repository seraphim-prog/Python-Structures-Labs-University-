"""Практична робота №6–7. Один локальний Flask-застосунок для семи завдань."""

import logging
import os
from secrets import token_urlsafe
from pathlib import Path
from time import perf_counter

from cachelib.file import FileSystemCache
from flask import Flask, g, jsonify, render_template, request
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from werkzeug.exceptions import HTTPException

from account import account
from blog import blog
from common import APIError, now
from data import ITEMS, POSTS, STUDENTS
from items import items_api
from store import DuplicateEmail, RecordNotFound, Store
from students import students_api


def create_app(config=None):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.environ.get("PRACTICE_SECRET_KEY") or token_urlsafe(32),
        SESSION_TYPE="cachelib", SESSION_PERMANENT=False,
        SESSION_COOKIE_NAME="p067_sid", SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax",
        PRACTICE_API_KEY=os.environ.get("PRACTICE_API_KEY"),
        PRACTICE_CORS_ORIGIN=os.environ.get("PRACTICE_CORS_ORIGIN", "http://127.0.0.1:5500"),
    )
    if config:
        app.config.update(config)
    if app.config.get("SESSION_CACHELIB") is None:
        app.config["SESSION_CACHELIB"] = FileSystemCache(str(Path(app.instance_path) / "sessions"))
    Session(app)
    app.json.ensure_ascii = False
    app.logger.setLevel(logging.INFO)
    app.extensions.update(posts=Store(POSTS), items=Store(ITEMS), students=Store(STUDENTS, unique_email=True))

    @app.before_request
    def log_request():
        g.started = perf_counter()
        app.logger.info("%s %s %r", now(), request.method, request.path)

    @app.after_request
    def add_headers(response):
        response.headers["X-Request-Time"] = f"{(perf_counter() - g.started) * 1000:.2f} ms"
        if request.path.startswith("/api/"):
            response.vary.add("Origin")
            origin = request.headers.get("Origin")
            if origin and origin == app.config["PRACTICE_CORS_ORIGIN"]:
                response.headers["Access-Control-Allow-Origin"] = origin
                if request.method == "OPTIONS" and "Allow" in response.headers:
                    response.headers["Access-Control-Allow-Methods"] = response.headers["Allow"]
                    response.headers["Access-Control-Allow-Headers"] = "Content-Type, X-API-Key"
        return response

    def error_response(message, status, details=None):
        if request.path.startswith("/api/"):
            response = jsonify(error=message, status=status, details=details or {}, timestamp=now())
            if status == 401:
                response.headers["WWW-Authenticate"] = 'ApiKey realm="students-v2"'
            return response, status
        return render_template("error.html", status=status, message=message), status

    @app.errorhandler(APIError)
    def handle_api_error(error):
        return error_response(str(error), error.status_code, error.details)

    @app.errorhandler(RecordNotFound)
    def handle_missing(_error):
        return error_response("Ресурс не знайдено.", 404)

    @app.errorhandler(DuplicateEmail)
    def handle_duplicate(_error):
        return error_response("Електронна адреса вже використовується.", 409, {"field": "email"})

    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        message = {404: "Ресурс не знайдено.", 405: "Метод запиту не підтримується."}.get(
            error.code, error.description,
        )
        body, status = error_response(message, error.code)
        response = app.make_response((body, status))
        for key, value in error.get_headers():
            if key not in ("Content-Type", "Content-Length"):
                response.headers.add(key, value)
        return response

    # Форми використовують CSRF-токен. JSON-контролери працюють із тілом і заголовками.
    csrf = CSRFProtect(app)
    for blueprint in (blog, account, items_api, students_api):
        app.register_blueprint(blueprint)
    csrf.exempt(items_api)
    csrf.exempt(students_api)
    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000)
