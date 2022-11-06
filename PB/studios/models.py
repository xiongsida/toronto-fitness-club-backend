from django.db import models
import googlemaps
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import CASCADE
from django.utils.safestring import mark_safe
import os

# Create your models here.
gmaps = googlemaps.Client(key='AIzaSyAz2VJWVsBKb65KyxVWm1exv2-dubWdFdU')

class Amenity(models.Model):
    type = models.CharField(max_length=256)
    
    def __str__(self):
        return self.type
    
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
        for i in self.images.all(): # to delete the actual file, because cascade is for database entries
            i.delete()
        super(Studio, self).delete(*args, **kwargs)
    
    @property
    def location(self):
        return {"latitude":self.latitude, "logitude":self.longitude}

    def __str__(self):
        return self.name
    
    
class StudioImage(models.Model):
    studio = models.ForeignKey(to=Studio, on_delete=CASCADE, related_name="images")
    image = models.ImageField(upload_to = 'studio-images/')
    
    def save(self, *args, **kwargs):
        to_delete_path=None
        try:
            this = StudioImage.objects.get(id=self.id)
            if this.image != self.image:
                to_delete_path=this.image.path # update the image, need delete old one
        except: 
            pass
        super(StudioImage, self).save(*args, **kwargs)
        if to_delete_path:
            os.remove(to_delete_path)
    
    def delete(self, *args, **kwargs):
        try:
            self.image.delete(save=False)
        except:
            pass
        super(StudioImage, self).delete(*args, **kwargs)
        
    @property
    def thumbnail(self):    
        if self.image:
            # print(self.image.url)
            return mark_safe("<img src={} \
                style='width:{}px; height:{}px' />".format(self.image.url,min(100,0.5*self.image.width),min(100,0.5*self.image.height)))
        
    def __str__(self):
        return "studio_"+str(self.studio)+"_image_"+str(self.id)
    

class StudioAmenity(models.Model):
    studio = models.ForeignKey(Studio, on_delete=CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=CASCADE)
    quantity = models.PositiveIntegerField()
    
    class Meta:
        unique_together=[['studio','amenity']]


class Class(models.Model):
    pass


