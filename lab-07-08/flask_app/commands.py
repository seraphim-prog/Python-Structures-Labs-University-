from contextlib import contextmanager
from datetime import date
from uuid import uuid4

import click
from sqlalchemy import event, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from shared.data import ENROLLMENTS, PARTICIPANTS, TOPICS, WORKSHOPS

from .extensions import db
from .models import Enrollment, Participant, Profile, Topic, Workshop
from .queries import analytics
from .services import commit_changes


def seed_catalog():
    topics = {}
    for slug, name, description in TOPICS:
        topic = db.session.scalar(select(Topic).where(Topic.slug == slug))
        if topic is None:
            topic = Topic(slug=slug, name=name, description=description)
            db.session.add(topic)
        topics[slug] = topic
    workshops = {}
    for slug, title, day, minutes, published, tags in WORKSHOPS:
        workshop = db.session.scalar(select(Workshop).where(Workshop.slug == slug))
        if workshop is None:
            workshop = Workshop(slug=slug, title=title, starts_on=day,
                                duration_minutes=minutes, published=published, topics=[topics[t] for t in tags])
            db.session.add(workshop)
        workshops[slug] = workshop
    participants = {}
    for email, name, city in PARTICIPANTS:
        participant = db.session.scalar(select(Participant).where(Participant.email == email))
        if participant is None:
            participant = Participant(email=email, name=name, profile=Profile(city=city))
            db.session.add(participant)
        participants[email] = participant
    db.session.flush()
    for email, slug in ENROLLMENTS:
        participant, workshop = participants[email], workshops[slug]
        exists = db.session.scalar(select(Enrollment.id).filter_by(
            participant_id=participant.id, workshop_id=workshop.id,
        ))
        if exists is None:
            db.session.add(Enrollment(
                participant=participant, workshop=workshop, registered_on=date(2026, 11, 22),
            ))
    commit_changes()


@contextmanager
def count_statements():
    engine = db.engine
    statements = []

    def capture(_connection, _cursor, statement, _parameters, _context, _many):
        statements.append(statement)

    event.listen(engine, "before_cursor_execute", capture)
    try:
        yield statements
    finally:
        event.remove(engine, "before_cursor_execute", capture)


def demo_orm():
    seed_catalog()
    probe = Participant(name="Учасник CRUD", email=f"demo-{uuid4().hex}@example.com")
    db.session.add(probe)
    commit_changes()
    identity = probe.id
    click.echo(f"CREATE: збережено = {identity is not None}")
    read = db.session.scalar(select(Participant).where(Participant.id == identity))
    click.echo(f"READ: {read.name}")
    read.active = False
    commit_changes()
    click.echo(f"UPDATE: active = {db.session.get(Participant, identity).active}")
    db.session.delete(read)
    commit_changes()
    click.echo(f"DELETE: існує = {db.session.get(Participant, identity) is not None}")

    for key, value in analytics().items():
        click.echo(f"{key}: {value}")
    participant = db.session.scalar(select(Participant).filter_by(email="taras@example.com"))
    click.echo(f"Зворотний зв’язок: {participant.name}, записів = {len(participant.enrollments)}")
    query = select(Workshop).order_by(Workshop.starts_on, Workshop.id)
    db.session.expire_all()
    with count_statements() as plain:
        expected = [(item.slug, [topic.slug for topic in item.topics])
                    for item in db.session.scalars(query)]
    db.session.expire_all()
    with count_statements() as eager:
        actual = [(item.slug, [topic.slug for topic in item.topics])
                  for item in db.session.scalars(query.options(selectinload(Workshop.topics)))]
    if expected != actual:
        raise RuntimeError("Набори тем не збігаються.")
    click.echo(f"N+1: {len(plain)} → {len(eager)} запити, однакові теми")

    original = db.session.scalar(select(Enrollment).order_by(Enrollment.id).limit(1))
    temporary_address = f"rollback-{uuid4().hex}@example.com"
    db.session.add(Participant(name="Учасник транзакції", email=temporary_address))
    db.session.flush()
    db.session.add(Enrollment(participant_id=original.participant_id, workshop_id=original.workshop_id))
    try:
        commit_changes()
    except IntegrityError:
        retained = db.session.scalar(select(Participant.id).where(Participant.email == temporary_address))
        click.echo(f"ROLLBACK: дублікат відхилено, тимчасовий учасник існує = {retained is not None}")
