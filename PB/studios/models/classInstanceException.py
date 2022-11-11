from django.db import models
from django.db.models import CASCADE
from studios.models.classEvent import ClassEvent

class ClassInstanceException(models.Model):
    class_event=models.ForeignKey(to=ClassEvent, on_delete=CASCADE, related_name="exceptions")
    event_date=models.DateField()
    is_cancelled=models.BooleanField(default=True)
    same_for_all_future=models.BooleanField()