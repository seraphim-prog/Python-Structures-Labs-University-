"""Рендеринг DTL, обробка заявки та сторінка відмови CSRF."""

from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_safe, require_http_methods

from shared import workshops as data

from .forms import ApplicationForm


@require_safe
def home(request):
    return render(request, "home.html", data.page_context("home", "Майстер-класи з програмування"))


@require_safe
def program(request):
    return render(request, "program.html", data.page_context("program", "Програма майстер-класів"))


@require_http_methods(["GET", "HEAD", "POST"])
def apply(request):
    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            messages.success(request, data.success_message(
                form.cleaned_data["name"], form.cleaned_data["workshop"]
            ))
            return redirect("apply")
    else:
        selection = request.GET.get("workshop", "")
        initial = {"workshop": selection} if selection in data.WORKSHOP_BY_KEY else None
        form = ApplicationForm(initial=initial)

    context = data.page_context("apply", "Заявка на майстер-клас")
    context["form"] = form
    return render(request, "apply.html", context)


def csrf_rejected(request, reason=""):
    context = data.page_context("apply", "Запит відхилено")
    context["status_code"] = 403
    return render(request, "csrf_rejected.html", context, status=403)
