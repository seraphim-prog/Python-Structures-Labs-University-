from sqlalchemy import func, or_, select
from sqlalchemy.orm import selectinload

from .extensions import db
from .models import Enrollment, Topic, Workshop


def published_workshops():
    return (
        select(Workshop, func.count(Enrollment.id).label("enrollment_count"))
        .outerjoin(Enrollment, Enrollment.workshop_id == Workshop.id)
        .where(Workshop.published.is_(True))
        .group_by(Workshop.id)
        .order_by(Workshop.starts_on, Workshop.id)
        .options(selectinload(Workshop.topics))
    )


def analytics() -> dict:
    order = (Workshop.starts_on, Workshop.id)
    slugs = select(Workshop.slug).order_by(*order)
    counts = (
        select(Workshop.slug, func.count(Enrollment.id))
        .outerjoin(Enrollment, Enrollment.workshop_id == Workshop.id)
        .group_by(Workshop.id).order_by(*order)
    )
    return {
        "filter": list(db.session.scalars(slugs.where(Workshop.published.is_(True)))),
        "exclude": list(db.session.scalars(slugs.where(~Workshop.topics.any(Topic.slug == "python")))),
        "or": list(db.session.scalars(slugs.where(
            or_(Workshop.duration_minutes >= 90, Workshop.slug == "team-git")
        ))),
        "counts": {slug: value for slug, value in db.session.execute(counts)},
        "total": db.session.scalar(select(func.coalesce(func.sum(Workshop.duration_minutes), 0))),
    }
