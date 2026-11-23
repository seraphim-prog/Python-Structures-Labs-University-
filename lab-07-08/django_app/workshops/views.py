from django import forms
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_safe

from .queries import published_workshops
from .services import register


class EnrollmentForm(forms.Form):
    name = forms.CharField(label="Ім’я", min_length=2, max_length=60)
    email = forms.EmailField(label="Електронна пошта", max_length=254)


@require_safe
def index(request):
    return redirect("workshop_list")


@require_safe
def workshop_list(request):
    return render(request, "workshops/list.html", {"workshops": published_workshops()})


@require_http_methods(["GET", "HEAD", "POST"])
def workshop_detail(request, slug):
    workshop = get_object_or_404(published_workshops(), slug=slug)
    form = EnrollmentForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        created = register(workshop, **form.cleaned_data)
        message = "Заявку прийнято." if created else "Заявку на це заняття вже подано."
        messages.success(request, message)
        return redirect("workshop_detail", slug=slug)
    return render(
        request, "workshops/detail.html", {"workshop": workshop, "form": form},
        status=400 if form.is_bound else 200,
    )
