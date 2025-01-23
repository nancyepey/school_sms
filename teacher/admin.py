from django.contrib import admin


#
from . models import Teacher

# Register your models here.

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    #
    list_display = ('name', 'teacher_uid', 'gender', 'teacher_subj', 'email', 'joining_date', 'mobile_number')
    search_fields = ('name', 'teacher_uid' ,'date_of_birth','teacher_subj', 'joining_date', 'email')
    list_filter = ('gender','teacher_subj', 'permanent_address')
    # readonly_fields = ('teacher_image',) # Optional: makes the image field read only

