"""Blueprint зі сторінками та маршрутом JSON."""

from importlib.metadata import version

from flask import Blueprint, current_app, jsonify, render_template, request


pages = Blueprint("pages", __name__)


@pages.get("/")
def index():
    return render_template("index.html")


@pages.get("/about")
def about():
    return render_template("about.html")


@pages.get("/api/info")
def api_info():
    return jsonify(
        framework="Flask",
        version=version("Flask"),
        debug=current_app.debug,
        routes=sorted(rule.rule for rule in current_app.url_map.iter_rules()),
    )


@pages.get("/greet")
@pages.get("/greet/<name>")
def greet(name=None):
    # Параметр у шляху має пріоритет над параметром рядка запиту.
    supplied = request.args.get("name", "") if name is None else name
    return render_template("greet.html", name=supplied.strip() or "Гість")
