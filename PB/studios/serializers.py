from rest_framework import serializers

from studios.models import Studio

class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = ['id', 'name', 'address', 'location', 'postal_code', 'phone_number']