from functools import partial

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction

from .models import Enrollment, Participant, Workshop


@transaction.atomic
def register(workshop: Workshop, *, name: str, email: str) -> bool:
    """Створити запис і запланувати підтвердження після коміту."""
    participant, _ = Participant.objects.get_or_create(
        email=email.strip().lower(), defaults={"name": name.strip()},
    )
    _, created = Enrollment.objects.get_or_create(participant=participant, workshop=workshop)
    if created:
        transaction.on_commit(
            partial(
                send_mail,
                "Запис на майстер-клас",
                f"Ваша заявка на «{workshop.title}» отримана.",
                settings.DEFAULT_FROM_EMAIL,
                [participant.email],
            ),
            robust=True,
        )
    return created
