from django.contrib import admin

from studios.models import Studio, StudioImage, Amenity, StudioAmenity

class StudioImageTabularInline(admin.TabularInline):
    model = StudioImage
    list_display= ['image','thumbnail']
    readonly_fields = ['thumbnail']
    
class StudioAmenityTabularInline(admin.TabularInline):
    model=StudioAmenity
    
    
class StudioAdmin(admin.ModelAdmin):
    inlines = [StudioImageTabularInline, StudioAmenityTabularInline]
    model = Studio
    readonly_fields = ['latitude','longitude']

# Register your models here.
admin.site.register(Studio, StudioAdmin)
admin.site.register(Amenity)
