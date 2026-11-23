"""Точка входу Flask і маршрути майстер-класів."""

import os
from pathlib import Path
from secrets import token_urlsafe

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_wtf.csrf import CSRFError, CSRFProtect

from shared import workshops as data

from .forms import ApplicationForm


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def create_app() -> Flask:
    app = Flask(
        __name__, template_folder="templates",
        static_folder=PROJECT_ROOT / "shared" / "static", static_url_path="/static",
    )
    app.config.update(
        SECRET_KEY=os.environ.get("FLASK_SECRET_KEY") or token_urlsafe(48),
        SESSION_COOKIE_SAMESITE="Lax",
    )
    CSRFProtect(app)

    @app.get("/")
    def home():
        return render_template("home.html", **data.page_context("home", "Майстер-класи з програмування"))

    @app.get("/workshops/")
    def program():
        return render_template("program.html", **data.page_context("program", "Програма майстер-класів"))

    @app.route("/apply/", methods=["GET", "POST"])
    def apply():
        if request.method == "POST":
            form = ApplicationForm()
            if form.validate_on_submit():
                flash(data.success_message(form.name.data, form.workshop.data), "success")
                return redirect(url_for("apply"))
        else:
            selection = request.args.get("workshop", "")
            form = ApplicationForm(workshop=selection if selection in data.WORKSHOP_BY_KEY else "")

        return render_template("apply.html", form=form, **data.page_context("apply", "Заявка на майстер-клас"))

    @app.errorhandler(CSRFError)
    def csrf_rejected(error):
        return render_template(
            "csrf_rejected.html", status_code=400, **data.page_context("apply", "Запит відхилено")
        ), 400

    return app
