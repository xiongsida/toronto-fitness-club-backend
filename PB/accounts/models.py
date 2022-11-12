from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from subscriptions.models import Plan


class TFCUser(AbstractUser):
    phone_number = PhoneNumberField(unique=True)
    avatar = models.ImageField(upload_to='user_avatars/',
                               default='avatar_default.png')

    plan = models.ForeignKey(Plan, blank=True, null=True)
    subscribed_time = models.DateTimeField(blank=True, null=True)
    next_plan = models.ForeignKey(Plan, blank=True, null=True)
    is_subscribed = models.BooleanField(default=False)
