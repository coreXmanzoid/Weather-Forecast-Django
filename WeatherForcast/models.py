from django.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings
settings.AUTH_USER_MODEL

# Create your models here.
class User(AbstractUser):
    quries_per_day = models.SmallIntegerField(default=0)
    can_send_email = models.BooleanField(default=True)


# models.py


class EmailSettings(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="email_settings"
    )

    weather_alerts = models.BooleanField(default=False)
    daily_forecast = models.BooleanField(default=False)
    weekly_summary = models.BooleanField(default=False)

    EMAIL_CHOICES = [
        ("immediate", "Immediate"),
        ("daily", "Daily"),
        ("weekly", "Weekly"),
    ]

    email_frequency = models.CharField(
        max_length=20,
        choices=EMAIL_CHOICES,
        default="daily"
    )

    def __str__(self):
        return f"{self.user.username} Email Settings"