from django.contrib import admin
from django import forms
from studios.models.studio import Studio
from studios.models.studioImage import StudioImage
from studios.models.amenity import Amenity
from studios.models.studioAmenity import StudioAmenity

from studios.models.classEvent import ClassEvent
from studios.models.classKeyword import ClassKeyword
from studios.models.classInstanceException import ClassInstanceException

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
    
class ClassInstanceExceptionTabularInline(admin.TabularInline):
    model=ClassInstanceException
    
class ClassEventAdmin(admin.ModelAdmin):
    inlines=[ClassKeywordTabularInline,ClassInstanceExceptionTabularInline]
    model=ClassEvent
    readonly_fields = ['previous_version']
    

# Register your models here.
admin.site.register(Studio, StudioAdmin)
admin.site.register(Amenity)
admin.site.register(ClassEvent,ClassEventAdmin)

