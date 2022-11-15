from django.db import models
from classes.models.classParent import ClassParent
from django.db.models import CASCADE

class ClassCanellation(models.Model):
    class_parent= models.ForeignKey(to=ClassParent, on_delete=CASCADE, related_name="cancellations")
    action_date = models.DateField()
    is_cancelled = models.BooleanField()
    apply_for_all_future = models.BooleanField(default=False)
    # def delete(self):
    #     self.save()
        
class ClassEdition(models.Model):
    class_parent= models.ForeignKey(to=ClassParent, on_delete=CASCADE, related_name="editions") # editions
    original_date = models.DateField(blank=True,null=True)
    description = models.CharField(max_length=512, null=True, blank=True)
    new_date = models.DateField(null=True,blank=True)
    start_time = models.TimeField(null=True,blank=True)
    end_time = models.TimeField(null=True,blank=True)
    coach = models.CharField(max_length=128,null=True,blank=True)
    capacity = models.PositiveIntegerField(null=True, blank=True)
    recurrence_pattern = models.IntegerField(choices=ClassParent.RECURRENCE_WAY,blank=True,null=True) # weekly recurrence
    recur_end_date = models.DateField(null=True,blank=True)
    edit_for_all_future = models.BooleanField(default=False)
    # def delete(self):
        # self.save()