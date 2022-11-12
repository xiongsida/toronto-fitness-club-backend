from django.db import models
from studios.utils import delete_file_thumbnail
from sorl.thumbnail import get_thumbnail
from django.db.models import CASCADE
from django.utils.safestring import mark_safe
from studios.models.studio import Studio
from django.conf import settings

class StudioImage(models.Model):
    studio = models.ForeignKey(to=Studio, on_delete=CASCADE, related_name="images")
    image = models.ImageField(upload_to = settings.STUDIO_IMAGE_RELATIVE_PATH)
    
    def save(self, *args, **kwargs):
        try:
            previous = StudioImage.objects.get(id=self.id)
            if previous.image != self.image:
                delete_file_thumbnail(previous.image)
        except: 
            pass
        super(StudioImage, self).save(*args, **kwargs)

    
    def delete(self, *args, **kwargs):
        try:
            previous = StudioImage.objects.get(id=self.id)
            if previous.image != self.image:
                delete_file_thumbnail(previous.image) # in case of update+delete at the same time
            delete_file_thumbnail(self.image)
        except:
            pass
        super(StudioImage, self).delete(*args, **kwargs)
        
    @property
    def thumbnail(self):    
        if self.image:
            # print(self.image.url)
            thumb=get_thumbnail(self.image, '100x100', quality=90)
            return mark_safe("<img src={} />".format(thumb.url))
        
    def __str__(self):
        return "studio_"+str(self.studio)+"_image_"+str(self.id)