from datetime import date

from django.core.validators import MaxValueValidator, MinLengthValidator, MinValueValidator
from django.db import models

from shared.data import ENROLLMENT_STATES, LEVELS


class Participant(models.Model):
    name = models.CharField("Ім’я", max_length=60, validators=[MinLengthValidator(2)])
    email = models.EmailField("Електронна пошта", unique=True)
    active = models.BooleanField("Активний", default=True)

    class Meta:
        ordering = ["name", "id"]
        verbose_name = "учасник"
        verbose_name_plural = "учасники"

    def __str__(self) -> str:
        return self.name


class Profile(models.Model):
    participant = models.OneToOneField(
        Participant, on_delete=models.CASCADE, related_name="profile",
    )
    city = models.CharField("Місто", max_length=80)
    level = models.CharField("Рівень", max_length=16, choices=LEVELS, default="beginner")
    bio = models.TextField("Коротко про себе", blank=True, default="")

    class Meta:
        ordering = ["participant_id"]
        verbose_name = "профіль"
        verbose_name_plural = "профілі"

    def __str__(self) -> str:
        return f"{self.participant.name} — {self.city}"


class Topic(models.Model):
    name = models.CharField("Назва", max_length=60)
    slug = models.SlugField("Код", max_length=60, unique=True)
    description = models.TextField("Опис", default="", blank=True)

    class Meta:
        ordering = ["slug"]
        verbose_name = "тема"
        verbose_name_plural = "теми"

    def __str__(self) -> str:
        return self.name


class Workshop(models.Model):
    title = models.CharField("Назва", max_length=100, validators=[MinLengthValidator(3)])
    slug = models.SlugField("Код", max_length=80, unique=True)
    starts_on = models.DateField("Дата")
    duration_minutes = models.PositiveSmallIntegerField(
        "Тривалість", validators=[MinValueValidator(15), MaxValueValidator(480)],
    )
    published = models.BooleanField("Опубліковано", default=False)
    room = models.CharField("Місце проведення", max_length=40, default="Онлайн")
    topics = models.ManyToManyField(Topic, related_name="workshops", blank=True)

    class Meta:
        ordering = ["starts_on", "id"]
        verbose_name = "майстер-клас"
        verbose_name_plural = "майстер-класи"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(duration_minutes__range=(15, 480)),
                name="workshop_duration_range",
            ),
        ]

    def __str__(self) -> str:
        return self.title


class Enrollment(models.Model):
    participant = models.ForeignKey(
        Participant, on_delete=models.CASCADE, related_name="enrollments",
    )
    workshop = models.ForeignKey(
        Workshop, on_delete=models.PROTECT, related_name="enrollments",
    )
    registered_on = models.DateField("Дата запису", default=date.today)
    status = models.CharField("Стан", max_length=16, choices=ENROLLMENT_STATES, default="pending")
    note = models.TextField("Примітка", blank=True, default="")

    class Meta:
        ordering = ["registered_on", "id"]
        verbose_name = "запис на заняття"
        verbose_name_plural = "записи на заняття"
        constraints = [
            models.UniqueConstraint(
                fields=["participant", "workshop"], name="one_enrollment_per_workshop",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.participant.name} → {self.workshop.title}"
