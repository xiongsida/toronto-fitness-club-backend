from django.contrib import admin
from studios.models.studio import Studio
from studios.models.studioImage import StudioImage
from studios.models.amenity import Amenity
from studios.models.studioAmenity import StudioAmenity

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
        
# Register your models here.
admin.site.register(Studio, StudioAdmin)
admin.site.register(Amenity)
