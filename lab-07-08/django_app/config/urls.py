from django.urls import path

from django_app.workshops import views


urlpatterns = [
    path("", views.index, name="index"),
    path("workshops/", views.workshop_list, name="workshop_list"),
    path("workshops/<slug:slug>/", views.workshop_detail, name="workshop_detail"),
]
