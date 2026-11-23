"""Серверна валідація заявки засобами Flask-WTF."""

from flask_wtf import FlaskForm
from wtforms import EmailField, SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, ValidationError

from shared import workshops as rules


def strip_text(value: str | None) -> str | None:
    return value.strip() if value is not None else None


class WorkshopSelectField(SelectField):
    def pre_validate(self, form):
        try:
            super().pre_validate(form)
        except ValidationError as error:
            raise ValidationError(rules.WORKSHOP_REQUIRED) from error


class ApplicationForm(FlaskForm):
    name = StringField(
        rules.NAME_LABEL, filters=[strip_text],
        validators=[
            DataRequired(message=rules.NAME_REQUIRED),
            Length(min=rules.NAME_MIN, max=rules.NAME_MAX, message=rules.NAME_LENGTH),
        ],
        render_kw={"autocomplete": "name", "placeholder": "Олена Коваль"},
    )
    email = EmailField(
        rules.EMAIL_LABEL, filters=[strip_text],
        validators=[
            DataRequired(message=rules.EMAIL_REQUIRED),
            Length(max=rules.EMAIL_MAX, message=rules.EMAIL_LENGTH),
            Email(message=rules.EMAIL_INVALID, check_deliverability=False),
        ],
        render_kw={"autocomplete": "email", "placeholder": "name@example.com"},
    )
    workshop = WorkshopSelectField(
        rules.WORKSHOP_LABEL, choices=rules.WORKSHOP_CHOICES,
        validators=[DataRequired(message=rules.WORKSHOP_REQUIRED)],
    )
    motivation = TextAreaField(
        rules.MOTIVATION_LABEL, description=rules.MOTIVATION_HINT, filters=[strip_text],
        validators=[
            DataRequired(message=rules.MOTIVATION_REQUIRED),
            Length(max=rules.MOTIVATION_MAX, message=rules.MOTIVATION_LENGTH),
        ],
        render_kw={"rows": 4, "placeholder": "Що хочете навчитися робити?"},
    )

    def validate_motivation(self, field) -> None:
        if not field.errors and not rules.has_enough_words(field.data):
            raise ValidationError(rules.MOTIVATION_SHORT)
