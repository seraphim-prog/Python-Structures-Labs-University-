from datetime import date

import pytest

from django_app.workshops.models import Enrollment, Participant, Profile, Topic, Workshop


@pytest.fixture
def participant(db):
    return Participant.objects.create(name="Олена Коваль", email="olena@example.com")


@pytest.fixture
def workshop(db):
    return Workshop.objects.create(
        title="Робота з даними у Python", slug="python-data", starts_on=date(2026, 11, 27),
        duration_minutes=90, published=True,
    )


@pytest.fixture
def linked_records(participant, workshop):
    profile = Profile.objects.create(participant=participant, city="Київ")
    topic = Topic.objects.create(name="Python", slug="python")
    workshop.topics.add(topic)
    enrollment = Enrollment.objects.create(participant=participant, workshop=workshop)
    return profile, topic, enrollment
