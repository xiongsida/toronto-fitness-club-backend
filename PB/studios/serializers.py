from rest_framework import serializers

from studios.models.studio import Studio
from studios.models.studioImage import StudioImage
from studios.models.studioAmenity import StudioAmenity
from studios.models.amenity import Amenity

from django.urls import reverse
        
class StudioImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudioImage
        fields=['id','image']

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields=['type']

class StudioAmenitySerializer(serializers.ModelSerializer):
    amenity=AmenitySerializer()
    class Meta:
        model = StudioAmenity
        fields=['amenity','quantity']
        
class StudioDetailSerializer(serializers.ModelSerializer):
    images=StudioImageSerializer(many=True,read_only=True)
    amenities=StudioAmenitySerializer(source='studioamenity_set',many=True,read_only=True)
    classes=serializers.SerializerMethodField(source="get_classes")
    def get_classes(self, obj):
        return self.context['request'].build_absolute_uri(reverse("classes:classes-list"))+"?studio_id={}".format(obj.id)
    class Meta:
        model=Studio
        fields = ['id', 'name', 'address', 'location', 'postal_code', 'phone_number','images','classes','amenities','direction']
        
        
class StudioSerializer(serializers.HyperlinkedModelSerializer):
    details = serializers.SerializerMethodField(source="get_details")
    def get_details(self, obj):
        return self.context['request'].build_absolute_uri(reverse("studios:details", kwargs={'studio_id': obj.id}))
    class Meta:
        model = Studio
        fields = ['id', 'name', 'address', 'location', 'postal_code', 'phone_number',"details"]