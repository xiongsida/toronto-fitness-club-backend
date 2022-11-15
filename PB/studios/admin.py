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
from django.db.models import Q

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
                parent=ClassParent.objects.get(id=obj.id)
                create_class_instances_when_creating_parent(parent)
            except Exception as e:
                print(e)
        return super(ClassParentAdmin, self).save_model(request, obj, form, change)
    
    def save_related(self, request, form, formsets, change):
        class_parent=ClassParent.objects.get(id=form.instance.id) 
        edition_data=formsets[1].cleaned_data
        cancellation_data=formsets[2].cleaned_data
        new_edition_length=len(edition_data)-len(class_parent.editoins.all())
        new_cancellation_length=len(cancellation_data)-len(class_parent.cancellations.all())
        try:
            edit_instances(class_parent,edition_data[0-new_edition_length:])
            cancel_instances(class_parent,cancellation_data[0-new_cancellation_length:])
        except Exception as e:
            print(e)
        return super(ClassParentAdmin, self).save_related(request, form, formsets, change)


def create_class_instances_when_creating_parent(parent,generated_dates):
    current_date=datetime.date.today()
    recur_end_date=parent.recur_end_date
    recurrence_pattern=parent.recurrence_pattern
    generated_dates=generate_weekdays(current_date,recur_end_date,recurrence_pattern)
    for class_date in generated_dates:
        ClassInstance.objects.create(class_parent=parent,
            date = class_date,
            start_time = parent.start_time, end_time = parent.end_time,
            description = parent.description, coach = parent.coach,
            capacity = parent.capacity,
            is_cancelled = False
        )


def edit_instances(this_class_parent,data_list):
    for data in data_list:
        original_date = data.get('original_date',None)
        description =data.get('description',None)
        new_date = data.get('new_date',None)
        start_time = data.get('start_time',None)
        end_time = data.get('end_time',None)
        coach = data.get('coach',None)
        capacity = data.get('capacity',None)
        recurrence_pattern = data.get('recurrence_pattern',None)
        recur_end_date = data.get('recur_end_date',None)
        edit_for_all_future = data.get('edit_for_all_future',None)
        
        # first edit for parent class if needed
        if edit_for_all_future:
            if description: this_class_parent.description=description
            if start_time: this_class_parent.start_time=start_time
            if end_time: this_class_parent.end_time=end_time
            if coach: this_class_parent.coach=coach
            if capacity!=None: this_class_parent.capacity=int(capacity)
            if recurrence_pattern: 
                this_class_parent.recurrence_pattern=recurrence_pattern
            if recur_end_date: 
                old_recur_end_date=this_class_parent.recur_end_date
                this_class_parent.recur_end_date=recur_end_date  
    
        # then edit for class instance according to pattern
        if original_date:
            classes_to_change=None
            if not edit_for_all_future: # just edit for one class at original date
                classes_to_change=ClassInstance.objects.filter(Q(date=original_date)&Q(class_parent=this_class_parent))
            elif not new_date: # edit for all future
                classes_to_change=ClassInstance.objects.filter(Q(date__gte=original_date)&Q(class_parent=this_class_parent))          
            for class_to_change in classes_to_change:
                if new_date: class_to_change.date=new_date
                if description: class_to_change.description=description
                if start_time: class_to_change.start_time=start_time
                if end_time: class_to_change.end_time=end_time
                if coach: class_to_change.coach=coach
                if capacity!=None: class_to_change.capacity=int(capacity)
                class_to_change.save() 
                     
        elif edit_for_all_future and (not new_date):
            q=Q(date__gt=datetime.date.today()) | (Q(date=datetime.date.today())&Q(start_time__gte=datetime.datetime.now().time()))
            classes_to_change=ClassInstance.objects.filter(q & Q(class_parent=this_class_parent))
            if recurrence_pattern:
                for class_to_change in classes_to_change:
                    shift=recurrence_pattern-class_to_change.date.isoweekday()
                    calculated_new_date=class_to_change.date+datetime.timedelta(days=shift)
                    if this_class_parent.recur_end_date>=calculated_new_date>datetime.date.today(): #also need before recur end date
                        class_to_change.date=calculated_new_date
                    if description: class_to_change.description=description
                    if start_time: class_to_change.start_time=start_time
                    if end_time: class_to_change.end_time=end_time
                    if coach: class_to_change.coach=coach
                    if capacity!=None: class_to_change.capacity=int(capacity)
                    class_to_change.save() 
            if recur_end_date: 
                # extend classes recur end, need enroll previous students who wish to enroll for all future
                extended_dates=generate_weekdays(old_recur_end_date+datetime.timedelta(days=1),recur_end_date,this_class_parent.recurrence_pattern)
                if ClassInstance.objects.filter(start_time__gte=old_recur_end_date):
                    extended_dates=extended_dates[1:] # there is already one previous class shift to one date due to pattern change
                for class_date in extended_dates:
                    new_extended_class=ClassInstance.objects.create(class_parent=this_class_parent,
                        date = class_date,
                        start_time = this_class_parent.start_time, end_time = this_class_parent.end_time,
                        description = this_class_parent.description, coach = this_class_parent.coach,
                        capacity = this_class_parent.capacity,
                        is_cancelled = False
                    )
                    for stu in this_class_parent.students.all():
                        if new_extended_class.capacity > len(new_extended_class.students.all()):
                            stu.class_instances.add(new_extended_class)
                          
        
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
            instances=class_parent.class_instances.all().filter(date=action_date)
            for instance in instances:
                instance.is_cancelled=is_cancelled
                instance.save()
            
        
# Register your models here.
admin.site.register(Studio, StudioAdmin)
admin.site.register(Amenity)
admin.site.register(ClassParent,ClassParentAdmin)
