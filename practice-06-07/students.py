"""Завдання 3.1 та 3.2. REST API студентів, серіалізація й API-ключ."""

from collections import Counter
from datetime import datetime
from functools import wraps
from hmac import compare_digest
from statistics import mean

from email_validator import EmailNotValidError, validate_email
from flask import Blueprint, current_app, jsonify, request, url_for

from common import APIError, now, number, ordering, pagination, read_json, sorted_rows, text_field

students_api = Blueprint("students", __name__, url_prefix="/api")
WRITABLE = ("name", "group", "email", "gpa")
VISIBLE = ("id", *WRITABLE, "created_at", "honor_roll")
SORTABLE = ("name", "gpa", "group")


class StudentSerializer:
    @staticmethod
    def serialize(student, fields=None):
        created = datetime.fromisoformat(student["created_at"])
        record = student | {"created_at": created.isoformat(timespec="seconds").replace("+00:00", "Z"),
                            "honor_roll": student["gpa"] >= 90}
        return {field: record[field] for field in VISIBLE if fields is None or field in fields}

    @staticmethod
    def deserialize(data, *, partial=False):
        missing = [field for field in WRITABLE if not partial and field not in data]
        unknown = sorted(set(data) - set(WRITABLE))
        if missing or unknown or not data:
            raise APIError("Некоректний набір полів студента.", 422, {"missing": missing, "unknown": unknown})
        clean = {}
        for key, limit in (("name", 90), ("group", 30), ("email", 254)):
            if key in data:
                clean[key] = text_field(data[key], key, limit, 422)
        if "email" in clean:
            try:
                address = validate_email(clean["email"], check_deliverability=False)
            except EmailNotValidError:
                raise APIError("Некоректна електронна адреса.", 422, {"field": "email"}) from None
            clean["email"] = address.normalized.casefold()
        if "gpa" in data:
            gpa = number(data["gpa"], "gpa", 422)
            if not 0 <= gpa <= 100:
                raise APIError("Середній бал має бути від 0 до 100.", 422, {"field": "gpa"})
            clean["gpa"] = gpa
        return clean

    @staticmethod
    def serialize_list(students, fields=None):
        return [StudentSerializer.serialize(student, fields) for student in students]


def require_api_key(view):
    """Порівнює заголовок із ключем, заданим у середовищі."""
    @wraps(view)
    def wrapped(*args, **kwargs):
        expected = current_app.config["PRACTICE_API_KEY"]
        supplied = request.headers.get("X-API-Key", "")
        if not expected or not compare_digest(expected.encode(), supplied.encode()):
            raise APIError("Потрібен дійсний API-ключ.", 401)
        return view(*args, **kwargs)
    return wrapped


def students():
    return current_app.extensions["students"]


def student_list(*, sort_parameter, search="", fields=None):
    group = request.args.get("group", "").strip().casefold()
    min_gpa = number(request.args.get("min_gpa", "0"), "min_gpa")
    if not 0 <= min_gpa <= 100:
        raise APIError("min_gpa має бути від 0 до 100.")
    field, desc = ordering(sort_parameter, SORTABLE, "name")
    page, per_page = pagination()
    matches = [row for row in students().all()
               if (not group or row["group"].casefold() == group)
               and row["gpa"] >= min_gpa
               and (not search or any(search in row[key].casefold() for key in ("name", "group", "email")))]
    results = sorted_rows(matches, field, desc)
    start = (page - 1) * per_page
    return jsonify(count=len(matches), page=page, per_page=per_page,
                   students=StudentSerializer.serialize_list(results[start:start + per_page], fields))


def create_student_record():
    values = StudentSerializer.deserialize(read_json())
    student = students().create(values | {"created_at": now()})
    return jsonify(StudentSerializer.serialize(student)), 201, {
        "Location": url_for("students.get_student", student_id=student["id"]),
    }


@students_api.get("/students")
def get_students():
    return student_list(sort_parameter="sort_by")


@students_api.post("/students")
def create_student():
    return create_student_record()


@students_api.get("/students/<int:student_id>")
def get_student(student_id):
    return jsonify(StudentSerializer.serialize(students().get(student_id)))


@students_api.put("/students/<int:student_id>")
def update_student(student_id):
    clean = StudentSerializer.deserialize(read_json())
    return jsonify(StudentSerializer.serialize(students().update(student_id, clean)))


@students_api.patch("/students/<int:student_id>")
def patch_student(student_id):
    clean = StudentSerializer.deserialize(read_json(), partial=True)
    return jsonify(StudentSerializer.serialize(students().update(student_id, clean)))


@students_api.delete("/students/<int:student_id>")
def delete_student(student_id):
    students().delete(student_id)
    return "", 204


@students_api.get("/students/stats")
def students_stats():
    rows = students().all()
    top = sorted_rows(rows, "gpa", True)[:3]
    return jsonify(total=len(rows), avg_gpa=round(mean(row["gpa"] for row in rows), 2) if rows else None,
                   groups=dict(Counter(row["group"] for row in rows)),
                   top_students=StudentSerializer.serialize_list(top, ("id", "name", "group", "gpa")))


@students_api.get("/v2/students")
def get_students_v2():
    fields = request.args.get("fields")
    selected = None if fields is None else [field.strip() for field in fields.split(",")]
    if selected is not None and not set(selected).issubset(VISIBLE):
        raise APIError("Запит містить невідомі поля.", details={"allowed": list(VISIBLE)})
    return student_list(sort_parameter="sort", search=request.args.get("search", "").strip().casefold(),
                        fields=selected)


@students_api.post("/v2/students")
@require_api_key
def create_student_v2():
    return create_student_record()
