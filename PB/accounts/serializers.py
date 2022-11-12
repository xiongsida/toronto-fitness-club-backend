from rest_framework import serializers
from .models import TFCUser
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class TFCUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TFCUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'avatar',
            'email',
            'password',
            'phone_number',
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
