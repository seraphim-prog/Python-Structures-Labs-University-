import os
from pathlib import Path
from secrets import token_urlsafe

from flask import Flask

from .commands import demo_orm
from .extensions import csrf, db, migrate
from .views import web


def create_app(config: dict | None = None) -> Flask:
    project = Path(__file__).resolve().parents[1]
    app = Flask(__name__, static_folder=project / "shared" / "static")
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("FLASK_SECRET_KEY") or token_urlsafe(48),
        SQLALCHEMY_DATABASE_URI=os.environ.get("FLASK_DATABASE_URI") or "sqlite:///orm-flask.sqlite3",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    if config:
        app.config.update(config)
    db.init_app(app)
    migrate.init_app(app, db, directory=str(Path(__file__).with_name("migrations")))
    csrf.init_app(app)
    app.register_blueprint(web)
    app.cli.command("demo-orm")(demo_orm)
    return app
