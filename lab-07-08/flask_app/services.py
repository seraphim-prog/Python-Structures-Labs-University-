from datetime import date

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from .extensions import db
from .models import Enrollment, Participant, Workshop


def current_date() -> date:
    return date.today()


def commit_changes() -> None:
    """Зафіксувати зміни, відновивши сесію в разі помилки."""
    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        raise


def register(workshop: Workshop, *, name: str, email: str) -> bool:
    """Додати учасника та запис на заняття однією транзакцією."""
    address = email.strip().lower()
    workshop_id = workshop.id
    existing = (
        select(Enrollment.id)
        .join(Participant)
        .where(Participant.email == address, Enrollment.workshop_id == workshop_id)
    )
    if db.session.scalar(existing) is not None:
        return False
    participant = db.session.scalar(select(Participant).where(Participant.email == address))
    if participant is None:
        participant = Participant(name=name, email=address)
    db.session.add(Enrollment(
        participant=participant, workshop_id=workshop_id, registered_on=current_date(),
    ))
    try:
        commit_changes()
    except IntegrityError:
        if db.session.scalar(existing) is not None:
            return False
        raise
    return True
