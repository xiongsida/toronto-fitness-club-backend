from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField


class Plan(models.Model):
    interval = models.DurationField()
    available_date = models.DateTimeField(auto_now=True)
    price = models.FloatField(validators=[MinValueValidator(0.0)])
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)


class PaymentMethod(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='payment_method',
    )
    alias = models.CharField(blank=True, null=True, max_length=15)
    card_number = CardNumberField()
    card_expire = CardExpiryField()
    security_code = SecurityCodeField()


class Subscription(models.Model):
    plan = models.ForeignKey(
        Plan,
        on_delete=models.PROTECT,
        related_name='users_subscription',
    )
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='subscription',
    )
    subscribed_time = models.DateTimeField(auto_now=True)
    expired_time = models.DateTimeField()


class UpComingPlan(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='upcoming_plan',
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.PROTECT,
        related_name='users_upcoming_plan',
    )


class Receipt(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='receipt',
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.PROTECT,
        related_name='users_receipt',
    )
    card_number = CardNumberField()
    amount = models.FloatField()
    paid_time = models.DateTimeField(auto_now=True)
    is_refund = models.BooleanField(default=False)
