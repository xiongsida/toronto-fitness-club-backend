from django.db import models
import datetime
from django.db.models import DO_NOTHING

class ClassEvent(models.Model):
    RECCURENCE_WAY = [
        ('MONDAY', 'recur every Monday'),
        ('TUESDAY', 'recur every Tuesday'),
        ('WEDNESDAY', 'recur every Wednesday'),
        ('THURSDAY', 'recur every Thursday'),
        ('FRIDAY', 'recur every Friday'),
        ('SATURDAY','recur every Saturday'),
        ('SUNDAY','recur every Sunday')
    ]
    name = models.CharField(max_length=128, null=False, blank=False)
    description = models.CharField(max_length=512, null=False, blank=False)
    coach = models.CharField(max_length=128, null=False, blank=False)
    capacity = models.PositiveIntegerField(null=False, blank=False)
    created_datetime = models.DateTimeField(auto_now_add=True) # when class was created
    start_time = models.TimeField()  # the specific start time in a day
    end_time = models.TimeField()
    reccurence_pattern = models.CharField(default='MONDAY',choices=RECCURENCE_WAY,max_length=9) # weekly recurrence
    recur_end_date = models.DateField(default=datetime.datetime(9999,12,31)) # when recurring class ends, if infinity, end_date could be 9999-12-31
    previous_version = models.ForeignKey('self',null=True,on_delete=DO_NOTHING,related_name='later_version')
    