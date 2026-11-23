"""Завдання 1.2. View-функції для ресурсу товарів."""

from flask import Blueprint, current_app, jsonify, request, url_for

from common import APIError, number, ordering, sorted_rows, text_field, validate_json

items_api = Blueprint("items", __name__, url_prefix="/api/items")
FIELDS = ("name", "price", "category")


def items():
    return current_app.extensions["items"]


def item_values(data):
    price = number(data["price"], "price")
    if price <= 0:
        raise APIError("Ціна має бути додатною.", details={"field": "price"})
    return {"name": text_field(data["name"], "name", 100), "price": price,
            "category": text_field(data["category"], "category", 60)}


@items_api.get("")
def get_items():
    category = request.args.get("category", "").strip().casefold()
    low = number(request.args.get("min_price", "0"), "min_price")
    high = number(request.args["max_price"], "max_price") if "max_price" in request.args else None
    if low < 0 or (high is not None and high < low):
        raise APIError("Некоректний діапазон цін.")
    field, descending = ordering("sort", ("name", "price"), "name")
    matches = [item for item in items().all()
               if (not category or item["category"].casefold() == category)
               and item["price"] >= low and (high is None or item["price"] <= high)]
    return jsonify(count=len(matches), items=sorted_rows(matches, field, descending))


@items_api.post("")
@validate_json(FIELDS)
def create_item(data):
    item = items().create(item_values(data))
    return jsonify(item), 201, {"Location": url_for("items.get_item", item_id=item["id"])}


@items_api.get("/<int:item_id>")
def get_item(item_id):
    return jsonify(items().get(item_id))


@items_api.put("/<int:item_id>")
@validate_json(FIELDS)
def update_item(item_id, data):
    return jsonify(items().update(item_id, item_values(data)))


@items_api.delete("/<int:item_id>")
def delete_item(item_id):
    items().delete(item_id)
    return "", 204
