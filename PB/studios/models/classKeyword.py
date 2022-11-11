from django.db import models
from studios.models.classEvent import ClassEvent
from django.db.models import CASCADE

class ClassKeyword(models.Model):
    classparent = models.ForeignKey(to=ClassEvent, on_delete=CASCADE, related_name="keywords")
    keyword = models.CharField(max_length=128)
    def __str__(self):
        return self.keyword