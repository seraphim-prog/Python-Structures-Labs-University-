"""Завдання 1.1, 2.1 та 2.2. Маршрути й CRUD публікацій."""

from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, url_for

from common import now, pagination

blog = Blueprint("blog", __name__)
POST_FIELDS = {"title": ("Заголовок", 100), "author": ("Автор", 60), "content": ("Зміст", 3000)}


def posts():
    return current_app.extensions["posts"]


@blog.get("/")
def index():
    return render_template("home.html")


@blog.get("/posts")
def post_list():
    page, per_page = pagination()
    rows = sorted(posts().all(), key=lambda post: (post["created_at"], post["id"]), reverse=True)
    start = (page - 1) * per_page
    pages = max(1, (len(rows) + per_page - 1) // per_page)
    if page > pages:
        abort(404)
    return render_template("listing.html", title="Публікації", posts=rows[start:start + per_page],
                           page=page, pages=pages, per_page=per_page)


@blog.get("/posts/<int:post_id>")
def post_detail(post_id):
    return render_template("post.html", post=posts().get(post_id))


@blog.get("/search")
def search():
    query = request.args.get("q", "").strip()
    needle = query.casefold()
    matches = [row for row in posts().all()
               if needle in row["title"].casefold() or needle in row["content"].casefold()]
    return render_template("listing.html", title="Пошук публікацій", query=query, posts=matches)


@blog.get("/archive/<int:year>/<int:month>")
def archive(year, month):
    if not 1 <= year <= 9999 or not 1 <= month <= 12:
        abort(404)
    prefix = f"{year:04d}-{month:02d}"
    matches = [row for row in posts().all() if row["created_at"].startswith(prefix)]
    return render_template("listing.html", title=f"Архів {month:02d}.{year:04d}", posts=matches)


@blog.get("/user/<string:username>")
def user_profile(username):
    matches = [row for row in posts().all() if row["author"].casefold() == username.casefold()]
    if not matches:
        abort(404)
    return render_template("listing.html", title=f"Публікації автора · {matches[0]['author']}", posts=matches)


def post_form(existing=None):
    editing = existing is not None
    values = existing if editing else {}
    errors = {}
    if request.method == "POST":
        values = {key: request.form.get(key, "").strip() for key in POST_FIELDS}
        for key, (label, limit) in POST_FIELDS.items():
            if not 0 < len(values[key]) <= limit:
                errors[key] = f"{label} має містити від 1 до {limit} символів."
        if "/" in values["author"] or values["author"] in (".", ".."):
            errors["author"] = "Автор має бути іменем без символу /."
        if not errors:
            if editing:
                post = posts().update(existing["id"], values)
            else:
                post = posts().create(values | {"created_at": now()})
            flash("Публікацію оновлено." if editing else "Публікацію створено.")
            # Після POST браузер отримує нову сторінку через GET.
            return redirect(url_for("blog.post_detail", post_id=post["id"]))
    cancel_url = (url_for("blog.post_detail", post_id=existing["id"])
                  if editing else url_for("blog.post_list"))
    return render_template("post_form.html", editing=editing, values=values, errors=errors,
                           fields=POST_FIELDS, cancel_url=cancel_url), 400 if errors else 200


@blog.route("/posts/create", methods=["GET", "POST"])
def post_create():
    return post_form()


@blog.route("/posts/<int:post_id>/edit", methods=["GET", "POST"])
def post_edit(post_id):
    return post_form(posts().get(post_id))


@blog.route("/posts/<int:post_id>/delete", methods=["GET", "POST"])
def post_delete(post_id):
    if request.method == "POST":
        posts().delete(post_id)
        flash("Публікацію видалено.")
        return redirect(url_for("blog.post_list"))
    return render_template("delete.html", post=posts().get(post_id))
