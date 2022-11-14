from rest_framework import serializers
from .models import *


class PlanSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Plan
        fields = [
            'url',
            'description',
            'interval',
            'available_date',
            'price',
        ]


class PaymentMethodSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PaymentMethod
        read_only_fields = ['user']
        fields = [
            'url',
            'user',
            'alias',
            'card_number',
            'card_expire',
            'security_code',
        ]


class SubscriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subscription
        read_only_fields = ['user', 'expired_time']
        fields = [
            'url',
            'user',
            'plan',
            'subscribed_time',
            'expired_time',
        ]


class UpComingPlanSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UpComingPlan
        read_only_fields = ['user']
        fields = [
            'url',
            'user',
            'plan',
        ]


class ReceiptSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Receipt
        read_only_fields = [
            'url',
            'user',
            'plan',
            'card_number',
            'amount',
            'paid_time',
            'is_refund',
        ]
        fields = read_only_fields
