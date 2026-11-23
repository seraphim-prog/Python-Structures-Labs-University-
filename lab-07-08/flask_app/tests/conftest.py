from datetime import date

import pytest

from flask_app.app import create_app
from flask_app.extensions import db
from flask_app.models import Enrollment, Participant, Profile, Topic, Workshop


@pytest.fixture
def app(tmp_path):
    database = tmp_path / "isolated.sqlite3"
    application = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database.as_posix()}",
    })
    with application.app_context():
        db.create_all()
    yield application
    with application.app_context():
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
    database.unlink(missing_ok=True)


@pytest.fixture
def session(app):
    with app.app_context():
        yield db.session


@pytest.fixture
def participant(session):
    participant = Participant(name="Олена Коваль", email="olena@example.com")
    session.add(participant)
    session.commit()
    return participant


@pytest.fixture
def workshop(session):
    workshop = Workshop(
        title="Робота з даними у Python", slug="python-data", starts_on=date(2026, 11, 27),
        duration_minutes=90, published=True,
    )
    session.add(workshop)
    session.commit()
    return workshop


@pytest.fixture
def linked_records(session, participant, workshop):
    profile = Profile(participant=participant, city="Київ")
    session.add(profile)
    topic = Topic(name="Python", slug="python")
    workshop.topics.append(topic)
    enrollment = Enrollment(participant=participant, workshop=workshop)
    session.add_all([topic, enrollment])
    session.commit()
    return profile, topic, enrollment
