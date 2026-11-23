"""Серверна валідація заявки засобами Django Forms."""

from django import forms

from shared import workshops as rules


class ApplicationForm(forms.Form):
    name = forms.CharField(
        label=rules.NAME_LABEL, min_length=rules.NAME_MIN, max_length=rules.NAME_MAX,
        widget=forms.TextInput(attrs={"autocomplete": "name", "placeholder": "Олена Коваль"}),
        error_messages={
            "required": rules.NAME_REQUIRED,
            "min_length": rules.NAME_LENGTH,
            "max_length": rules.NAME_LENGTH,
        },
    )
    email = forms.EmailField(
        label=rules.EMAIL_LABEL, max_length=rules.EMAIL_MAX,
        widget=forms.EmailInput(attrs={"autocomplete": "email", "placeholder": "name@example.com"}),
        error_messages={
            "required": rules.EMAIL_REQUIRED,
            "invalid": rules.EMAIL_INVALID,
            "max_length": rules.EMAIL_LENGTH,
        },
    )
    workshop = forms.ChoiceField(
        label=rules.WORKSHOP_LABEL, choices=rules.WORKSHOP_CHOICES,
        error_messages={"required": rules.WORKSHOP_REQUIRED, "invalid_choice": rules.WORKSHOP_REQUIRED},
    )
    motivation = forms.CharField(
        label=rules.MOTIVATION_LABEL, max_length=rules.MOTIVATION_MAX,
        help_text=rules.MOTIVATION_HINT,
        widget=forms.Textarea(attrs={"rows": 4, "placeholder": "Що хочете навчитися робити?"}),
        error_messages={
            "required": rules.MOTIVATION_REQUIRED,
            "max_length": rules.MOTIVATION_LENGTH,
        },
    )

    def clean_motivation(self) -> str:
        text = self.cleaned_data["motivation"]
        if not rules.has_enough_words(text):
            raise forms.ValidationError(rules.MOTIVATION_SHORT)
        return text
