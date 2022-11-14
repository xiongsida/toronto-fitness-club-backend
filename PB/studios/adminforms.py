from django import forms
from studios.models.classInstanceException import ClassEdition, ClassCanellation
from studios.models.classInstance import ClassInstance
from django.db.models import Q
import datetime

class ClassCancelForm(forms.ModelForm):
    class Meta:
        model = ClassCanellation
        exclude = []
    def clean(self):
        this_class_parent=self.instance.class_parent
        action_date = self.cleaned_data.get('action_date',None)
        instances=ClassInstance.objects.filter(Q(date=action_date)&Q(class_parent=this_class_parent))
        if not instances:
            raise forms.ValidationError({'action_date': "no class in this class's instances found by this action date, try another one!"})
        

class ClassEditForm(forms.ModelForm):
    class Meta:
        model = ClassEdition
        exclude = []
    def clean(self):
        this_class_parent=self.instance.class_parent
        
        original_date = self.cleaned_data.get('original_date',None)
        new_date = self.cleaned_data.get('new_date',None)
        description = self.cleaned_data.get('description',None)
        start_time = self.cleaned_data.get('start_time',None)
        end_time = self.cleaned_data.get('end_time',None)
        coach = str(self.cleaned_data.get('coach',''))
        capacity = self.cleaned_data.get('capacity',None)
        recurrence_pattern = self.cleaned_data.get('recurrence_pattern',None)
        recur_end_date = self.cleaned_data.get('recur_end_date',None)
        edit_for_all_future = self.cleaned_data.get('edit_for_all_future',None)
        
        # when you change one instance, do not specify recurrence related fields
        # also when you want to change all instances after one specific one, do not specify recurrence related fields
        # only specify recurrence fields with general editting
        
        if original_date:
            if original_date<=datetime.date.today():
                raise forms.ValidationError({'original_date': "sorry, cannot edit past date's class"})
            instances=ClassInstance.objects.filter(Q(date=original_date)&Q(class_parent=this_class_parent))
            if not instances:
                raise forms.ValidationError({'original_date': "no class in this class's instances found by this original date, try another one!"})
            if (new_date or start_time or end_time) and (not recurrence_pattern) and (not recur_end_date) and (not edit_for_all_future):
                if new_date and ClassInstance.objects.filter(Q(date=new_date)&Q(class_parent=this_class_parent)):
                    raise forms.ValidationError({'new_date': "sorry, there is already another class in the same date, we prefer just have one same class in a day!"})
                print('change original date or time or datetime(may or may not :coach, description...), allowed')
                return # change original date or time or datetime(may or may not :coach, description...), allowed
            if (description or coach or capacity) and (not recurrence_pattern) and (not recur_end_date) and (not edit_for_all_future):
                print('change original just one class, not change time, just change coach..., also allowed')
                return # change original just one class, not change time, just change coach..., also allowed
            if edit_for_all_future and (not new_date) and (not recurrence_pattern) and (not recur_end_date):
                print('change all future after original class, but no change recurrence pattern, allowed')
                return # change all future after original class, but no change recurrence pattern, allowed
            else:
                raise forms.ValidationError({'original_date': "not sure what you want to change with all those fields"})
            
        if edit_for_all_future:
            if (description or coach or capacity) and (not recurrence_pattern) and (not recur_end_date):
                print('change all future instance from now with new information, allowed')
                return 
            if (not new_date) and (recurrence_pattern or recur_end_date or start_time or end_time):
                if recur_end_date<this_class_parent.recur_end_date:
                    raise forms.ValidationError({'recur_end_date': "you cannot edit your recur end date before your original one, if you want to cancel some future course, use cancel form"})
                print('change all future instance from now with new recur pattern, allowed')
                return
        raise forms.ValidationError({'edit_for_all_future': "not sure what you want to change with all those fields, if you want apply for all, click this"})
        
