from datetime import date
from unittest.mock import patch

from sqlalchemy import select

from flask_app.models import Enrollment
from flask_app.services import register


@patch("flask_app.services.current_date", return_value=date(2026, 11, 23))
def test_registration_uses_fixed_date(clock, session, workshop):
    assert register(workshop, name="Іван Сокіл", email="ivan@example.com")
    clock.assert_called_once_with()
    enrollment = session.scalars(select(Enrollment)).one()
    assert enrollment.registered_on == date(2026, 11, 23)
    assert enrollment.participant.email == "ivan@example.com"
