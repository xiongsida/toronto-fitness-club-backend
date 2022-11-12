from django.db import models

class Amenity(models.Model):
    type = models.CharField(max_length=256)
    
    def __str__(self):
        return self.type