"""Завдання 1.3. Уподобання в cookies, кошик та вхід у серверній сесії."""

from flask import Blueprint, abort, current_app, jsonify, redirect, render_template, request, session, url_for

account = Blueprint("account", __name__)
DAYS_30 = 30 * 24 * 60 * 60
PRODUCTS = {
    1: ("Ноутбук", 25000),
    2: ("Смартфон", 12000),
    3: ("Навушники", 2000),
}


def go_to_account():
    return redirect(url_for("account.login"))


def cookie(name, value):
    response = go_to_account()
    response.set_cookie(name, value, max_age=DAYS_30, httponly=True, samesite="Lax")
    return response


@account.post("/set-theme/<string:theme>")
def set_theme(theme):
    if theme not in ("light", "dark"):
        abort(400, "Доступні теми light і dark.")
    return cookie("theme", theme)


@account.get("/get-theme")
def get_theme():
    return jsonify(theme=request.cookies.get("theme", "light"))


@account.post("/set-language/<string:lang>")
def set_language(lang):
    if lang not in ("uk", "en"):
        abort(400, "Доступні коди мови uk і en.")
    return cookie("language", lang)


@account.get("/preferences")
def preferences():
    return jsonify(theme=request.cookies.get("theme", "light"),
                   language=request.cookies.get("language", "uk"))


@account.post("/cart/add/<int:product_id>")
def add_to_cart(product_id):
    if product_id not in PRODUCTS:
        abort(404)
    cart = session.get("cart", {})
    key = str(product_id)
    cart[key] = cart.get(key, 0) + 1
    session["cart"] = cart
    return go_to_account()


@account.get("/cart")
def view_cart():
    items = [
        {"id": int(key), "name": PRODUCTS[int(key)][0], "price": PRODUCTS[int(key)][1],
         "quantity": quantity}
        for key, quantity in session.get("cart", {}).items()
    ]
    return jsonify(items=items, total=sum(item["price"] * item["quantity"] for item in items))


@account.post("/cart/clear")
def clear_cart():
    session.pop("cart", None)
    return go_to_account()


@account.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        if not 1 <= len(username) <= 60:
            abort(400, "Ім’я має містити від 1 до 60 символів.")
        session["username"] = username
        current_app.session_interface.regenerate(session)
        return redirect(url_for("account.profile"))
    return render_template("account.html", products=PRODUCTS, cart=session.get("cart", {}))


@account.post("/logout")
def logout():
    session.pop("username", None)
    current_app.session_interface.regenerate(session)
    return go_to_account()


@account.get("/profile")
def profile():
    if "username" not in session:
        return go_to_account()
    return jsonify(username=session["username"], authenticated=True)
