from django.db import models
from classes.models.classParent import ClassParent
from django.db.models import CASCADE

class ClassKeyword(models.Model):
    classparent = models.ForeignKey(to=ClassParent, on_delete=CASCADE, related_name="keywords")
    keyword = models.CharField(max_length=128)
    def __str__(self):
        return self.keyword