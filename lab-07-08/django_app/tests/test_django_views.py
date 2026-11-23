import pytest
from django.test import Client
from django.urls import reverse

from django_app.workshops.models import Enrollment


pytestmark = pytest.mark.django_db


def test_index_redirects(client):
    response = client.get("/")
    assert response.status_code == 302
    assert response["Location"] == "/workshops/"


def test_published_list(client, workshop):
    response = client.get("/workshops/")
    assert response.status_code == 200
    assert "workshops/list.html" in [template.name for template in response.templates]
    assert workshop.title in response.content.decode()
    assert workshop.room in response.content.decode()


def test_workshop_detail(client, workshop):
    response = client.get(reverse("workshop_detail", args=[workshop.slug]))
    assert response.status_code == 200
    assert "workshops/detail.html" in [template.name for template in response.templates]
    assert "Заявка на заняття" in response.content.decode()


def test_missing_workshop(client):
    assert client.get("/workshops/missing/").status_code == 404


def test_post_registration_redirects_and_is_repeatable(client, workshop):
    url = reverse("workshop_detail", args=[workshop.slug])
    response = client.post(url, {"name": "Іван Сокіл", "email": "ivan@example.com"})
    assert response.status_code == 302 and response["Location"] == url
    assert "Заявку прийнято." in client.get(url).content.decode()
    assert client.post(url, {"name": "Іван Сокіл", "email": "ivan@example.com"}).status_code == 302
    assert "вже подано" in client.get(url).content.decode()
    assert Enrollment.objects.count() == 1


def test_invalid_post_preserves_form(client, workshop):
    response = client.post(f"/workshops/{workshop.slug}/", {"name": "Іван Сокіл", "email": "invalid"})
    assert response.status_code == 400
    assert response.context["form"].errors.get("email")
    assert "Іван Сокіл" in response.content.decode()
    assert Enrollment.objects.count() == 0


def test_post_without_csrf_is_rejected(workshop):
    client = Client(enforce_csrf_checks=True)
    assert client.post(f"/workshops/{workshop.slug}/", {"name": "Іван"}).status_code == 403
    assert Enrollment.objects.count() == 0
