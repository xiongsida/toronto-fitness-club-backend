from django.contrib import admin
from django import forms
from studios.models.studio import Studio
from studios.models.studioImage import StudioImage
from studios.models.amenity import Amenity
from studios.models.studioAmenity import StudioAmenity

from studios.models.classParent import ClassParent
from studios.models.classInstance import ClassInstance
from studios.models.classKeyword import ClassKeyword
from studios.models.classInstanceException import ClassEdition, ClassCanellation
import datetime
from studios.utils import generate_weekdays


class StudioImageTabularInline(admin.TabularInline):
    model = StudioImage
    list_display= ['image','thumbnail']
    readonly_fields = ['thumbnail']
    
    # def formfield_for_dbfield(self, db_field, **kwargs):
    #     if db_field.name == 'image':
    #         kwargs['widget'] = forms.FileInput(attrs={'onchange': 'alert(0)'})
    #     return super(StudioImageTabularInline, self).formfield_for_dbfield(db_field, **kwargs)
    
class StudioAmenityTabularInline(admin.TabularInline):
    model=StudioAmenity
    
    
class StudioAdmin(admin.ModelAdmin):
    inlines = [StudioImageTabularInline, StudioAmenityTabularInline]
    model = Studio
    readonly_fields = ['latitude','longitude']
    
    
class ClassKeywordTabularInline(admin.TabularInline):
    model=ClassKeyword
    extra=1
    
class ClassEditionStackedInline(admin.StackedInline):
    model=ClassEdition
    fields= [('previous_date','new_date'),'description',('start_time','end_time'),('recurrence_pattern','recur_end_date'),('coach','capacity'),'edit_for_all_future']
    extra=1

class ClassCanellationTabularInline(admin.TabularInline):
    model=ClassCanellation
    extra=1


class ClassParentAdmin(admin.ModelAdmin):
    fields=['name','studio','description','start_time','end_time',('recurrence_pattern','recur_end_date'),('coach','capacity')]
    inlines=[ClassKeywordTabularInline,ClassEditionStackedInline,ClassCanellationTabularInline]
    model=ClassParent
    
    def get_readonly_fields(self, request, obj=None):
        if obj: #This is the case when obj is already created i.e. it's an edit
            return ['name','studio','description','coach','capacity','start_time','end_time','recurrence_pattern','recur_end_date']
        else:
            return []
        
    def save_model(self,request,obj,form,change):
        if not obj.id: # creating a new class parent
            try:
                super(ClassParentAdmin, self).save_model(request, obj, form, change)
                recur_end_date=form.cleaned_data['recur_end_date']
                current_date=datetime.date.today()
                recurrence_pattern=form.cleaned_data['recurrence_pattern']
                generated_dates=generate_weekdays(current_date,recur_end_date,recurrence_pattern)
                parent=ClassParent.objects.get(id=obj.id)
                print(parent)
                sta=form.cleaned_data['start_time']
                end=form.cleaned_data['end_time']
                des=form.cleaned_data['description']
                coa=form.cleaned_data['coach']
                cap=form.cleaned_data['capacity']
                for class_date in generated_dates:
                    ClassInstance.objects.create(class_parent=parent,
                        date = class_date,
                        start_time = sta, end_time = end,
                        description = des, coach = coa,
                        capacity = cap,
                        is_cancelled = False
                    )
            except Exception as e:
                print(e)
                pass
        return super(ClassParentAdmin, self).save_model(request, obj, form, change)
        

# Register your models here.
admin.site.register(Studio, StudioAdmin)
admin.site.register(Amenity)
admin.site.register(ClassParent,ClassParentAdmin)

