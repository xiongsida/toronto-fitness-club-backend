from django.db import models
from django.db.models import CASCADE
from studios.models.classParent import ClassParent
import datetime

class ClassInstance(models.Model):
    class_parent = models.ForeignKey(to=ClassParent, on_delete=CASCADE, related_name="class_instances")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.CharField(max_length=512, null=False, blank=False)
    coach = models.CharField(max_length=128, null=False, blank=False)
    capacity = models.PositiveIntegerField(null=False, blank=False)
    is_cancelled = models.BooleanField()
    
    @property
    def begin_datetime(self):
        return datetime.datetime.combine(self.date,self.start_time)
    
    def __str__(self):
        return self.class_parent.name+self.date.strftime('%Y-%m-%d')
    
    