from rest_framework import serializers

from studios.models.studio import Studio
from studios.models.studioImage import StudioImage
from studios.models.studioAmenity import StudioAmenity
from studios.models.amenity import Amenity

from studios.models.classInstance import ClassInstance
from studios.models.classParent import ClassParent

class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = ['id', 'name', 'address', 'location', 'postal_code', 'phone_number']
        
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
    
    class Meta:
        model=Studio
        fields = ['id', 'name', 'address', 'location', 'postal_code', 'phone_number','images','amenities']
        
class ClassParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassParent
        fields=['name']

class StudioClassesSerializer(serializers.ModelSerializer):
    class_parent=ClassParentSerializer(many=False)
    class Meta:
        model = ClassInstance
        fields = ['class_parent', 'date', 'start_time', 'end_time','description','coach']