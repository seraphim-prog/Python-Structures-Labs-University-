from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import EmailField, StringField
from wtforms.validators import DataRequired, Email, Length

from .extensions import db
from .models import Workshop
from .queries import published_workshops
from .services import register


web = Blueprint("web", __name__)


def trim(value):
    return value.strip() if value is not None else None


class EnrollmentForm(FlaskForm):
    name = StringField(
        "Ім’я", filters=[trim],
        validators=[DataRequired("Введіть ім’я."), Length(2, 60, "Довжина імені від 2 до 60 символів.")],
    )
    email = EmailField(
        "Електронна пошта", filters=[trim],
        validators=[DataRequired("Введіть адресу."), Length(max=254), Email("Некоректна адреса.")],
    )


@web.get("/")
def index():
    return redirect(url_for("web.workshop_list"))


@web.get("/workshops/")
def workshop_list():
    return render_template("list.html", workshops=db.session.execute(published_workshops()).all())


@web.route("/workshops/<slug>/", methods=["GET", "POST"])
def workshop_detail(slug):
    row = db.session.execute(published_workshops().where(Workshop.slug == slug)).one_or_none()
    if row is None:
        abort(404)
    workshop, count = row
    form = EnrollmentForm()
    if form.validate_on_submit():
        created = register(workshop, name=form.name.data, email=form.email.data)
        flash("Заявку прийнято." if created else "Заявку на це заняття вже подано.")
        return redirect(url_for("web.workshop_detail", slug=slug))
    return render_template("detail.html", workshop=workshop, count=count, form=form), (
        400 if form.is_submitted() else 200
    )
