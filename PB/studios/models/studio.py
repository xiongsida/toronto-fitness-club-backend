from django.db import models
from studios.utils import gmaps
from phonenumber_field.modelfields import PhoneNumberField
from studios.models.amenity import Amenity

class Studio(models.Model):
    # name, address, geographical location, postal code, phone number, and a set of images.
    name = models.CharField(max_length=128, null=False, blank=False, unique=True)
    address = models.CharField(max_length=256, null=False, blank=False)
    latitude = models.FloatField(blank=True, default=0)
    longitude = models.FloatField(blank=True, default=0)
    postal_code = models.CharField(max_length=128)
    phone_number = PhoneNumberField()
    amenities = models.ManyToManyField(Amenity, through='StudioAmenity')
    
    def save(self, *args, **kwargs):
        try:
            temp=gmaps.geocode(self.address)[0].get("geometry").get("location")
            self.latitude, self.longitude=temp.get("lat"), temp.get("lng")
        except:
            pass
        super(Studio, self).save(*args, **kwargs)
            
    def delete(self, *args, **kwargs):
        for i in self.images.all(): # to delete the actual file, because cascade is only for database entries
            i.delete()
        super(Studio, self).delete(*args, **kwargs)
    
    @property
    def location(self):
        return {"latitude":self.latitude, "logitude":self.longitude}

    def __str__(self):
        return self.name
    
