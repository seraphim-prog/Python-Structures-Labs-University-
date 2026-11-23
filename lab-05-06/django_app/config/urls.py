"""Іменовані URL для огляду, програми й подання заявки."""

from django.urls import path

from django_app.workshops import views


urlpatterns = [
    path("", views.home, name="home"),
    path("workshops/", views.program, name="program"),
    path("apply/", views.apply, name="apply"),
]
