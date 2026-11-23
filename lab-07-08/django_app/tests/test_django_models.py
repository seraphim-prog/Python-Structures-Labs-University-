from datetime import date

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models.deletion import ProtectedError

from django_app.workshops.management.commands.demo_orm import seed_catalog
from django_app.workshops.models import Enrollment, Participant, Profile, Workshop
from django_app.workshops.queries import analytics


pytestmark = pytest.mark.django_db


def test_three_relationship_types(participant, workshop, linked_records):
    profile, topic, enrollment = linked_records
    assert participant.profile == profile
    assert list(workshop.topics.all()) == [topic]
    assert list(topic.workshops.all()) == [workshop]
    assert workshop.enrollments.get() == enrollment
    assert participant.enrollments.get() == enrollment


def test_string_representations(participant, workshop, linked_records):
    profile, topic, enrollment = linked_records
    assert str(participant) == "Олена Коваль"
    assert str(profile) == "Олена Коваль — Київ"
    assert str(topic) == "Python"
    assert str(workshop) == "Робота з даними у Python"
    assert str(enrollment) == "Олена Коваль → Робота з даними у Python"


def test_model_defaults(participant, workshop, linked_records):
    profile, _, enrollment = linked_records
    assert participant.active is True
    assert workshop.room == "Онлайн"
    assert (profile.level, profile.bio) == ("beginner", "")
    assert (enrollment.status, enrollment.note) == ("pending", "")
    assert isinstance(enrollment.registered_on, date)


@pytest.mark.parametrize("name, valid", [("О", False), ("Ол", True), ("А" * 60, True), ("А" * 61, False)])
def test_name_length(name, valid):
    participant = Participant(name=name, email="new@example.com")
    if valid:
        participant.full_clean()
    else:
        with pytest.raises(ValidationError) as error:
            participant.full_clean()
        assert "name" in error.value.message_dict


def test_unique_email(participant):
    with pytest.raises(IntegrityError), transaction.atomic():
        Participant.objects.create(name="Інша людина", email=participant.email)
    assert Participant.objects.count() == 1


def test_unique_enrollment(participant, workshop, linked_records):
    with pytest.raises(IntegrityError), transaction.atomic():
        Enrollment.objects.create(participant=participant, workshop=workshop)
    assert Enrollment.objects.count() == 1


def test_delete_participant_cascades(participant, workshop, linked_records):
    participant.delete()
    assert Profile.objects.count() == 0
    assert Enrollment.objects.count() == 0
    assert Workshop.objects.filter(pk=workshop.pk).exists()


def test_enrolled_workshop_is_protected(workshop, linked_records):
    with pytest.raises(ProtectedError):
        workshop.delete()
    assert Enrollment.objects.count() == 1


def test_catalog_analytics_are_reproducible():
    seed_catalog()
    seed_catalog()
    assert analytics() == {
        "filter": ["python-data", "team-git"],
        "exclude": ["team-git"],
        "or": ["python-data", "team-git", "web-forms"],
        "counts": {"python-data": 2, "team-git": 1, "web-forms": 0},
        "total": 270,
    }
