from unittest.mock import patch

import pytest

from django_app.workshops.models import Enrollment
from django_app.workshops.services import register


@pytest.mark.django_db
@patch("django_app.workshops.services.send_mail")
def test_confirmation_queued_after_commit(mail, workshop, django_capture_on_commit_callbacks):
    with django_capture_on_commit_callbacks(execute=True):
        assert register(workshop, name="Іван Сокіл", email="ivan@example.com")
        mail.assert_not_called()
    mail.assert_called_once_with(
        "Запис на майстер-клас",
        "Ваша заявка на «Робота з даними у Python» отримана.",
        "praktikum@example.com",
        ["ivan@example.com"],
    )
    assert Enrollment.objects.get().participant.email == "ivan@example.com"
