from rest_framework import serializers
from .models import TFCUser
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class TFCUserSerializer(serializers.HyperlinkedModelSerializer):
    payment_method = serializers.HyperlinkedRelatedField(
        view_name='paymentmethod-detail',
        read_only=True,
    )
    subscription = serializers.HyperlinkedRelatedField(
        view_name='subscription-detail',
        read_only=True,
    )
    upcoming_plan = serializers.HyperlinkedRelatedField(
        view_name='upcomingplan-detail',
        read_only=True,
    )
    receipt = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='receipt-detail',
        read_only=True,
    )

    class Meta:
        model = TFCUser
        fields = [
            'url',
            'username',
            'first_name',
            'last_name',
            'avatar',
            'email',
            'password',
            'phone_number',
            'payment_method',
            'subscription',
            'upcoming_plan',
            'receipt',
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = TFCUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
