from django.db import models
from django.core.validators import MinValueValidator
# Create your models here.


class Plan(models.Model):
    interval = models.DurationField(
        null=False,
        blank=False,
    )
    available_date = models.DateTimeField(
        null=False,
        blank=False,
        auto_now=True,
    )
    price = models.FloatField(
        null=False,
        blank=False,
        validators=[MinValueValidator(0.0)],
    )
    is_active = models.BooleanField(
        default=True
    )
