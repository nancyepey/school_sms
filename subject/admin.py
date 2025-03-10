from django.contrib import admin

#
from django.contrib import admin
from . models import Subject
#
from import_export import resources
from datetime import datetime
import numpy as np


# Register your models here.

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    # list_display = [field.name for field in Subject._meta.get_fields() if not field.many_to_many] #('slug', 'classroom', 'description', 'added_by','modified_by', 'is_actif')
    search_fields = ('title', 'subject_code', 'classroom')
    list_filter = ('title', 'subject_code', 'classroom', 'is_actif')



class SubjectResource(resources.ModelResource):
    class Meta:
        model = Subject
        # 
        import_id_fields = ["subject_code"]
        skip_unchanged = True
        use_bulk = True

