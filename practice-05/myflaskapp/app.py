"""Фабрика застосунку Flask і точка входу для локального запуску."""

import os
from secrets import token_urlsafe

from flask import Flask

from .config import config_by_name
from .routes import pages


def create_app(config_name: str = "default") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    key = os.environ.get("FLASK_SECRET_KEY")
    if not key and not app.debug:
        raise RuntimeError("Для production задай FLASK_SECRET_KEY у змінних середовища.")
    app.config["SECRET_KEY"] = key or token_urlsafe(32)
    # Маршрути приєднуються до кожного створеного екземпляра.
    app.register_blueprint(pages)
    return app


if __name__ == "__main__":
    create_app("development").run(host="127.0.0.1", port=5000, use_reloader=False)
