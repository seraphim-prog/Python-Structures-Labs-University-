"""Представлення головної, інформаційної та контактної сторінок."""

from django.shortcuts import render


def index(request):
    return render(request, "pages/index.html")


def about(request):
    return render(request, "pages/about.html")


def contact(request):
    # Рядок імені передається в контекст з автоматичним HTML-екрануванням.
    name = request.GET.get("name", "").strip()
    return render(request, "pages/contact.html", {"name": name})
