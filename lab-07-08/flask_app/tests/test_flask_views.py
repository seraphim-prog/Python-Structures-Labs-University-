import re

from sqlalchemy import func, select

from flask_app.models import Enrollment


def post_form(client, url, **data):
    page = client.get(url).get_data(as_text=True)
    field = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', page)
    assert field is not None
    return client.post(url, data={**data, "csrf_token": field.group(1)})


def test_index_redirects(client):
    response = client.get("/")
    assert response.status_code == 302
    assert response.headers["Location"] == "/workshops/"


def test_published_list(client, workshop):
    response = client.get("/workshops/")
    assert response.status_code == 200
    assert workshop.title in response.get_data(as_text=True)
    assert workshop.room in response.get_data(as_text=True)


def test_workshop_detail(client, workshop):
    response = client.get(f"/workshops/{workshop.slug}/")
    assert response.status_code == 200
    assert "Заявка на заняття" in response.get_data(as_text=True)


def test_missing_workshop(client):
    assert client.get("/workshops/missing/").status_code == 404


def test_post_registration_redirects_and_is_repeatable(client, session, workshop):
    url = f"/workshops/{workshop.slug}/"
    response = post_form(client, url, name="Іван Сокіл", email="ivan@example.com")
    assert response.status_code == 302 and response.headers["Location"] == url
    assert "Заявку прийнято." in client.get(url).get_data(as_text=True)
    assert post_form(client, url, name="Іван Сокіл", email="ivan@example.com").status_code == 302
    assert "вже подано" in client.get(url).get_data(as_text=True)
    assert session.scalar(select(func.count(Enrollment.id))) == 1


def test_invalid_post_preserves_form(client, session, workshop):
    response = post_form(client, f"/workshops/{workshop.slug}/", name="Іван Сокіл", email="invalid")
    assert response.status_code == 400
    assert "Некоректна адреса." in response.get_data(as_text=True)
    assert "Іван Сокіл" in response.get_data(as_text=True)
    assert session.scalar(select(func.count(Enrollment.id))) == 0


def test_post_without_csrf_is_rejected(client, session, workshop):
    assert client.post(f"/workshops/{workshop.slug}/", data={"name": "Іван"}).status_code == 400
    assert session.scalar(select(func.count(Enrollment.id))) == 0
