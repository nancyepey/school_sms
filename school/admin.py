from django.contrib import admin
#
from . models import ClassRoom, Settings, Specialty

# Register your models here.

@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'class_code', 'class_department', 'slug')
    search_fields = ('class_name', 'class_code', 'class_department')
    list_filter = ('class_name', 'class_code', 'class_department')


admin.site.register(Settings)
admin.site.register(Specialty)