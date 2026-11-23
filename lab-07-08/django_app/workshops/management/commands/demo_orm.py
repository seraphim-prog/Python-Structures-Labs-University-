from datetime import date
from uuid import uuid4

from django.core.management.base import BaseCommand
from django.db import connection, transaction
from django.test.utils import CaptureQueriesContext

from shared.data import ENROLLMENTS, PARTICIPANTS, TOPICS, WORKSHOPS
from django_app.workshops.models import Enrollment, Participant, Profile, Topic, Workshop
from django_app.workshops.queries import analytics


@transaction.atomic
def seed_catalog():
    topics = {}
    for slug, name, description in TOPICS:
        topics[slug], _ = Topic.objects.get_or_create(
            slug=slug, defaults={"name": name, "description": description},
        )
    workshops = {}
    for slug, title, day, minutes, published, tags in WORKSHOPS:
        workshop, _ = Workshop.objects.get_or_create(slug=slug, defaults={
            "title": title, "starts_on": day, "duration_minutes": minutes, "published": published,
        })
        workshop.topics.add(*(topics[tag] for tag in tags))
        workshops[slug] = workshop
    participants = {}
    for email, name, city in PARTICIPANTS:
        participant, _ = Participant.objects.get_or_create(email=email, defaults={"name": name})
        Profile.objects.get_or_create(participant=participant, defaults={"city": city})
        participants[email] = participant
    for email, slug in ENROLLMENTS:
        Enrollment.objects.get_or_create(
            participant=participants[email], workshop=workshops[slug],
            defaults={"registered_on": date(2026, 11, 22)},
        )


class Command(BaseCommand):
    help = "Додати зразки та показати CRUD, аналітику й кількість запитів."

    def handle(self, *args, **options):
        seed_catalog()
        write = self.stdout.write
        with transaction.atomic():
            probe = Participant.objects.create(name="Учасник CRUD", email=f"demo-{uuid4().hex}@example.com")
            write(f"CREATE: збережено = {probe.pk is not None}")
            read = Participant.objects.get(pk=probe.pk)
            write(f"READ: {read.name}")
            read.active = False
            read.save(update_fields=["active"])
            read.refresh_from_db()
            write(f"UPDATE: active = {read.active}")
            identity = read.pk
            read.delete()
            write(f"DELETE: існує = {Participant.objects.filter(pk=identity).exists()}")

        for key, value in analytics().items():
            write(f"{key}: {value}")
        participant = Participant.objects.get(email="taras@example.com")
        write(f"Зворотний зв’язок: {participant.name}, записів = {participant.enrollments.count()}")
        with CaptureQueriesContext(connection) as plain:
            expected = [(item.slug, [topic.slug for topic in item.topics.all()])
                        for item in Workshop.objects.all()]
        with CaptureQueriesContext(connection) as eager:
            actual = [(item.slug, [topic.slug for topic in item.topics.all()])
                      for item in Workshop.objects.prefetch_related("topics")]
        if expected != actual:
            raise RuntimeError("Набори тем не збігаються.")
        write(f"N+1: {len(plain)} → {len(eager)} запити, однакові теми")
