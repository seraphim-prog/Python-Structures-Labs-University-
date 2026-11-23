from datetime import date

import pytest
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from flask_app.commands import seed_catalog
from flask_app.models import Enrollment, Participant, Profile, Workshop
from flask_app.queries import analytics
from flask_app.services import commit_changes


def test_three_relationship_types(participant, workshop, linked_records):
    profile, topic, enrollment = linked_records
    assert participant.profile is profile
    assert workshop.topics == [topic]
    assert topic.workshops == [workshop]
    assert workshop.enrollments == [enrollment]
    assert participant.enrollments == [enrollment]


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
    if valid:
        assert Participant(name=name, email="new@example.com").name == name
    else:
        with pytest.raises(ValueError, match="від 2 до 60"):
            Participant(name=name, email="new@example.com")


def test_unique_email(session, participant):
    session.add(Participant(name="Інша людина", email=participant.email))
    with pytest.raises(IntegrityError):
        commit_changes()
    assert session.scalar(select(func.count(Participant.id))) == 1


def test_missing_foreign_key_is_rejected(session, workshop):
    session.add(Enrollment(participant_id=10000, workshop_id=workshop.id))
    with pytest.raises(IntegrityError):
        commit_changes()
    assert session.scalar(select(func.count(Enrollment.id))) == 0


def test_delete_participant_cascades(session, participant, workshop, linked_records):
    session.delete(participant)
    commit_changes()
    assert session.scalar(select(func.count(Profile.id))) == 0
    assert session.scalar(select(func.count(Enrollment.id))) == 0
    assert session.get(Workshop, workshop.id) is not None


def test_enrolled_workshop_is_protected(session, workshop, linked_records):
    session.delete(workshop)
    with pytest.raises(IntegrityError):
        commit_changes()
    assert session.scalar(select(func.count(Enrollment.id))) == 1


def test_failed_batch_rolls_back_all_changes(session, participant, workshop, linked_records):
    session.add(Participant(name="Марко Ліс", email="rollback@example.com"))
    session.flush()
    session.add(Enrollment(participant_id=participant.id, workshop_id=workshop.id))
    with pytest.raises(IntegrityError):
        commit_changes()
    assert session.scalar(select(Participant).filter_by(email="rollback@example.com")) is None
    assert session.scalar(select(func.count(Enrollment.id))) == 1


def test_catalog_analytics_are_reproducible(session):
    seed_catalog()
    seed_catalog()
    assert analytics() == {
        "filter": ["python-data", "team-git"],
        "exclude": ["team-git"],
        "or": ["python-data", "team-git", "web-forms"],
        "counts": {"python-data": 2, "team-git": 1, "web-forms": 0},
        "total": 270,
    }
