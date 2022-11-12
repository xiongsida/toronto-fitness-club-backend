from django.db import models
from django.db.models import CASCADE
from studios.models.amenity import Amenity
from studios.models.studio import Studio

class StudioAmenity(models.Model):
    studio = models.ForeignKey(Studio, on_delete=CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=CASCADE)
    quantity = models.PositiveIntegerField()
    
    class Meta:
        unique_together=[['studio','amenity']]