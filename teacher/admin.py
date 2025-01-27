from django.contrib import admin


#
from . models import Teacher

# Register your models here.

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    #
    list_display = ('name', 'teacher_uid', 'gender', 'teacher_subj', 'email', 'joining_date', 'mobile_number', 'teacher_subj')
    search_fields = ('name', 'teacher_uid' ,'date_of_birth', 'joining_date', 'email')
    list_filter = ('gender', 'permanent_address')
    # readonly_fields = ('teacher_image',) # Optional: makes the image field read only

    def teacher_subj(self, obj):
        return ", ".join([subject.title for subject in obj.t_subjects.all()])
    teacher_subj.subjects_desc = 'Subjects' 
    

