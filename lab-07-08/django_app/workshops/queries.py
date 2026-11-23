from django.db.models import Count, Q, Sum

from .models import Workshop


def published_workshops():
    return (
        Workshop.objects.filter(published=True)
        .annotate(enrollment_count=Count("enrollments"))
        .prefetch_related("topics")
    )


def analytics() -> dict:
    """Вибірки й зведення для навчального набору даних."""
    catalog = Workshop.objects.all()
    return {
        "filter": list(catalog.filter(published=True).values_list("slug", flat=True)),
        "exclude": list(catalog.exclude(topics__slug="python").values_list("slug", flat=True)),
        "or": list(catalog.filter(
            Q(duration_minutes__gte=90) | Q(slug="team-git")
        ).values_list("slug", flat=True)),
        "counts": dict(catalog.annotate(total=Count("enrollments")).values_list("slug", "total")),
        "total": catalog.aggregate(minutes=Sum("duration_minutes", default=0))["minutes"],
    }
