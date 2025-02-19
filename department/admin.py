from django.contrib import admin
#
from . models import Department

# Register your models here.

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Department._meta.get_fields() if not field.many_to_many] #
    search_fields = ('name', 'department_code', 'specialties')
    list_filter = ('name', 'department_code', 'specialties', 'is_actif')
