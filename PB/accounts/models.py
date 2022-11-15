from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class TFCUser(AbstractUser):
    phone_number = PhoneNumberField(null=True, blank=True)
    avatar = models.ImageField(upload_to='user_avatars/',
                               default='avatar_default.png')
