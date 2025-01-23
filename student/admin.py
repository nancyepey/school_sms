from django.contrib import admin
#
from django.contrib import admin
from . models import Parent, Student

# Register your models here.

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('father_name', 'mother_name', 'father_mobile', 'mother_mobile','carer_name', 'carer_mobile')
    search_fields = ('father_name', 'mother_name', 'father_mobile', 'mother_mobile','carer_name', 'carer_mobile')
    list_filter = ('father_name', 'mother_name', 'father_mobile', 'mother_mobile','carer_name', 'carer_mobile')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    #
    list_display = ('name', 'student_uid', 'gender', 'date_of_birth','student_class', 'mobile_number', 'joining_date', 'mobile_number', 'admission_number', 'parent')
    search_fields = ('name', 'student_uid' ,'date_of_birth','student_class', 'joining_date', 'admission_number', 'parent')
    list_filter = ('gender','student_class', 'section')
    readonly_fields = ('student_image',) # Optional: makes the image field read only

