from django.db import models
import datetime
from django.db.models import CASCADE
from studios.models.studio import Studio
from accounts.models import TFCUser
from studios.utils import generate_weekdays


class ClassParent(models.Model):
    RECURRENCE_WAY = [
        (1, 'recur every Monday'),
        (2, 'recur every Tuesday'),
        (3, 'recur every Wednesday'),
        (4, 'recur every Thursday'),
        (5, 'recur every Friday'),
        (6,'recur every Saturday'),
        (7,'recur every Sunday')
    ]
    name = models.CharField(max_length=128, null=False, blank=False)
    studio = models.ForeignKey(to=Studio, on_delete=CASCADE, related_name="classes")
    description = models.CharField(max_length=512, null=False, blank=False)
    coach = models.CharField(max_length=128, null=False, blank=False)
    capacity = models.PositiveIntegerField(null=False, blank=False)
    created_datetime = models.DateTimeField(auto_now_add=True) # when class was created
    start_time = models.TimeField(null=False,blank=False)  # the specific start time in a day
    end_time = models.TimeField(null=False,blank=False)
    recurrence_pattern = models.IntegerField(default=1,choices=RECURRENCE_WAY) # weekly recurrence
    recur_end_date = models.DateField(null=False,blank=False) # when recurring class ends, if infinity, end_date could be 9999-12-31
    
    students = models.ManyToManyField(TFCUser,related_name='class_parents') # this is only used when previous user wish to enroll to all future, and then admin extend the future classes
    
    def __str__(self):
        return 'studio_'+str(self.studio)+':class_'+self.name
    
