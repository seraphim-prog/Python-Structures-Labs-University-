from datetime import date

from sqlalchemy.orm import backref, validates

from .extensions import db


workshop_topics = db.Table(
    "workshop_topics",
    db.Column("workshop_id", db.ForeignKey("workshops.id", ondelete="CASCADE"), primary_key=True),
    db.Column("topic_id", db.ForeignKey("topics.id", ondelete="CASCADE"), primary_key=True),
)


class Participant(db.Model):
    __tablename__ = "participants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(254), nullable=False, unique=True)
    active = db.Column(db.Boolean, nullable=False, default=True)

    @validates("name")
    def validate_name(self, _key: str, value: str) -> str:
        value = value.strip()
        if not 2 <= len(value) <= 60:
            raise ValueError("Ім’я повинно містити від 2 до 60 символів.")
        return value

    def __str__(self) -> str:
        return self.name


class Profile(db.Model):
    __tablename__ = "profiles"

    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(
        db.Integer, db.ForeignKey("participants.id", ondelete="CASCADE"),
        nullable=False, unique=True,
    )
    city = db.Column(db.String(80), nullable=False)
    level = db.Column(db.String(16), nullable=False, default="beginner")
    bio = db.Column(db.Text, nullable=False, default="")
    participant = db.relationship(
        Participant, backref=backref("profile", uselist=False, cascade="all, delete-orphan",
                                     passive_deletes=True),
    )

    def __str__(self) -> str:
        return f"{self.participant.name} — {self.city}"


class Topic(db.Model):
    __tablename__ = "topics"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    slug = db.Column(db.String(60), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False, default="")

    def __str__(self) -> str:
        return self.name


class Workshop(db.Model):
    __tablename__ = "workshops"
    __table_args__ = (
        db.CheckConstraint("duration_minutes BETWEEN 15 AND 480", name="workshop_duration_range"),
    )

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(80), nullable=False, unique=True)
    starts_on = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.SmallInteger, nullable=False)
    published = db.Column(db.Boolean, nullable=False, default=False)
    room = db.Column(db.String(40), nullable=False, default="Онлайн", server_default="Онлайн")
    topics = db.relationship(
        Topic, secondary=workshop_topics, backref="workshops", order_by=Topic.slug,
    )

    def __str__(self) -> str:
        return self.title


class Enrollment(db.Model):
    __tablename__ = "enrollments"
    __table_args__ = (
        db.UniqueConstraint("participant_id", "workshop_id", name="one_enrollment_per_workshop"),
    )

    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(
        db.Integer, db.ForeignKey("participants.id", ondelete="CASCADE"), nullable=False,
    )
    workshop_id = db.Column(
        db.Integer, db.ForeignKey("workshops.id", ondelete="RESTRICT"), nullable=False,
    )
    registered_on = db.Column(db.Date, nullable=False, default=date.today)
    status = db.Column(db.String(16), nullable=False, default="pending")
    note = db.Column(db.Text, nullable=False, default="")
    participant = db.relationship(
        Participant, backref=backref("enrollments", cascade="all, delete-orphan", passive_deletes=True),
    )
    workshop = db.relationship(Workshop, backref=backref("enrollments", passive_deletes="all"))

    def __str__(self) -> str:
        return f"{self.participant.name} → {self.workshop.title}"
