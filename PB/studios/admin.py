from django.contrib import admin
from studios.adminforms import ClassEditForm, ClassCancelForm
from studios.models.studio import Studio
from studios.models.studioImage import StudioImage
from studios.models.amenity import Amenity
from studios.models.studioAmenity import StudioAmenity
from studios.models.classParent import ClassParent
from studios.models.classInstance import ClassInstance
from studios.models.classKeyword import ClassKeyword
from studios.models.classInstanceException import ClassEdition, ClassCanellation
import datetime
from studios.utils import generate_weekdays, flatten_list


class StudioImageTabularInline(admin.TabularInline):
    model = StudioImage
    list_display= ['image','thumbnail']
    readonly_fields = ['thumbnail']
    extra=2
    # def formfield_for_dbfield(self, db_field, **kwargs):
    #     if db_field.name == 'image':
    #         kwargs['widget'] = forms.FileInput(attrs={'onchange': 'alert(0)'})
    #     return super(StudioImageTabularInline, self).formfield_for_dbfield(db_field, **kwargs)
    
class StudioAmenityTabularInline(admin.TabularInline):
    model=StudioAmenity
    extra=2
    
class StudioAdmin(admin.ModelAdmin):
    inlines = [StudioImageTabularInline, StudioAmenityTabularInline]
    model = Studio
    readonly_fields = ['latitude','longitude','place_id']
    
    
class ClassKeywordTabularInline(admin.TabularInline):
    model=ClassKeyword
    extra=1
    
class ClassEditionStackedInline(admin.StackedInline):
    form=ClassEditForm
    model=ClassEdition
    fields= [('original_date','new_date'),'description',('start_time','end_time'),('recurrence_pattern','recur_end_date'),('coach','capacity'),'edit_for_all_future']
    extra=1
    def has_change_permission(self, request, obj=None):
        return False # this is the case when changing the classEdition, readonly
    def has_delete_permission(self, request, obj=None):
        return False
    def get_readonly_fields(self, request, obj=None):
        if not obj: #This is the case when creating the parent class, readonly
            return flatten_list(self.fields)
        return []

class ClassCanellationTabularInline(admin.TabularInline):
    form=ClassCancelForm
    model=ClassCanellation
    fields=['action_date','is_cancelled','apply_for_all_future']
    extra=1
    # readonly_fields=flatten_list(fields)
    def has_change_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return False
    def get_readonly_fields(self, request, obj=None):
        if not obj: #This is the case when creating the parent class
            return flatten_list(self.fields)
        return []


class ClassParentAdmin(admin.ModelAdmin):
    fields=['name','studio','description',('start_time','end_time'),('recurrence_pattern','recur_end_date'),('coach','capacity')]
    inlines=[ClassKeywordTabularInline,ClassEditionStackedInline,ClassCanellationTabularInline]
    model=ClassParent
    
    def get_readonly_fields(self, request, obj=None):
        if obj: #This is the case when obj is already created i.e. it's an edit
            # instead of editing original classparent to edit, we add a edition model, so all readonly
            return flatten_list(self.fields)
        return []
        
    def save_model(self,request,obj,form,change):
        if not change: # creating a new class parent
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
        return super(ClassParentAdmin, self).save_model(request, obj, form, change)
    
    def save_related(self, request, form, formsets, change):
        class_parent=ClassParent.objects.get(id=form.instance.id) 
        edition_data=formsets[1].cleaned_data
        cancellation_data=formsets[2].cleaned_data
        new_cancellation_length=len(cancellation_data)-len(class_parent.cancellations.all())
        try:
            cancel_instances(class_parent,cancellation_data[0-new_cancellation_length:])
        except Exception as e:
            print(e)
        return super(ClassParentAdmin, self).save_related(request, form, formsets, change)

# def edit_instances(class_parent,data_list):
#     for data in data_list:
#         original_date = data.get('original_date',None)
#         description =data.get('description',None)
#         new_date = data.get('new_date',None)
#         start_time = data.get('start_time',None)
#         end_time = data.get('end_time',None)
#         coach = data.get('coach',None)
#         capacity = data.get('capacity',None)
#         recurrence_pattern = data.get('recurrence_pattern',None)
#         recur_end_date = data.get('recur_end_date',None)
#         edit_for_all_future = data.get('edit_for_all_future',None)
#         if not original_date:
#             continue
#         if new_date: # just modify one
#             if original_date<=datetime.date.today():
#                 print("cannot edit past or today's class")
#                 continue
#             print("-----just move old to new, will not modify all futures to one day even though edit_for_all_future is given-----")
#             instances=class_parent.class_instances.all().filter(date=original_date)
#             for instance in instances:
#                 instance.date=new_date
#                 if description: instance.description=description
#                 if start_time: instance.start_time=start_time
#                 if end_time: instance.end_time=end_time
#                 if coach: instance.coach=coach
#                 if capacity: instance.capacity=capacity
#                 instance.save()
#         elif edit_for_all_future:
#             all_futures=class_parent.class_instances.all().filter(date__gte=original_date)
        
def cancel_instances(class_parent,data_list):
    for data in data_list:
        action_date=data.get('action_date',None)
        is_cancelled=data.get('is_cancelled',None)
        apply_for_all_future=data.get('apply_for_all_future',None)
        if not action_date:
            continue
        if apply_for_all_future:
            all_futures=class_parent.class_instances.all().filter(date__gte=action_date)
            for instance in all_futures:
                instance.is_cancelled=is_cancelled
                instance.save()
        else:
            try:
                instances=class_parent.class_instances.all().filter(date=action_date)
                for instance in instances:
                    instance.is_cancelled=is_cancelled
                    instance.save()
            except:
                print("the action date is not existing in future classes, but should never reach here if not existing because I check in forms")
                pass
            



# Register your models here.
admin.site.register(Studio, StudioAdmin)
admin.site.register(Amenity)
admin.site.register(ClassParent,ClassParentAdmin)
