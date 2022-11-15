from rest_framework import serializers

from classes.models.classInstance import ClassInstance
from classes.models.classParent import ClassParent

class ClassParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassParent
        fields=['name']

class ClassInstanceSerializer(serializers.ModelSerializer):
    class_parent=ClassParentSerializer(many=False)
    class Meta:
        model = ClassInstance
        fields = ['id', 'class_parent', 'date', 'start_time', 'end_time','description','coach','is_cancelled']