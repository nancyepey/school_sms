from django.contrib import admin
#
from django.contrib import admin
from numpy import isnat
from pandas import NaT

from images.models import Image
from school.models import ClassRoom, Specialty
from . models import Parent, Student
from images import services as image_services
from django.utils.html import format_html
#
from import_export import resources
from datetime import datetime
import numpy as np
import pandas as pd

# Register your models here.

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('father_name', 'mother_name', 'father_mobile', 'mother_mobile','carer_name', 'carer_mobile')
    search_fields = ('father_name', 'mother_name', 'father_mobile', 'mother_mobile','carer_name', 'carer_mobile')
    list_filter = ('father_name', 'mother_name', 'father_mobile', 'mother_mobile','carer_name', 'carer_mobile')

admin.site.register(Student)
# @admin.register(Student)
# class StudentAdmin(admin.ModelAdmin):
#     #
#     list_display = ('name', 'student_uid', 'gender', 'date_of_birth','student_class','mobile_number', 'joining_date', 'mobile_number', 'admission_number', 'parent', 'stud_image')
#     search_fields = ('name', 'student_uid' ,'date_of_birth','student_class', 'joining_date', 'admission_number', 'parent')
#     list_filter = ('gender','student_class', 'section')
#     readonly_fields = ( 'display_image') # Optional: makes the image field read only

#     def display_image(self, obj):
#         if obj.stud_image:
#             img_url = image_services.get_image_url_from_cloudflare(
#                 obj.stud_image.cloudflare_id, variant="thumbnailSmall"
#                 # obj.stud_image.cloudflare_id
#             )
#             img_html = f'<img src="{img_url}"  />'
#             return format_html(img_html)
#         return "No image"
#     display_image.short_description = "Current Image"



class StudentResource(resources.ModelResource):
    def before_import_row(self, row, **kwargs):
        for key, value in row.items():
            if key == "date_of_birth":
                print("valueeeeeeeeeeee")
                print(value)
                print(type(value))
                if type(value) == "nan" or  isinstance(value, float):
                    print("nan---")
                    row[key] = None
                    pass
                if value == None or value == "nan" or np.isnat(np.datetime64(f'{value}')) or np.isnan(np.datetime64(f'{value}')):
                    print("innnnnn")
                    row[key] = None
                # if isinstance(value, str):
                #     date_arra = value.split('/')
                #     # datetime.datetime(2006, 10, 25).date()
                #     row[key] = datetime.datetime(int(date_arra[2]), int(date_arra[1]), int(date_arra[0])).date()
                else:
                    # formatted_date = datetime.strptime(value, "%m/%d/%Y").strftime("%Y-%m-%d")
                    # formatted_date = datetime.today().strftime('%Y-%m-%d')
                    # row[key] = formatted_date
                    # print("value")
                    # print(value)
                    # date_arra = value.split('/')
                    # datetime.datetime(2006, 10, 25).date()
                    # row[key] = datetime.datetime(int(date_arra[2]), int(date_arra[1]), int(date_arra[0])).date()
                    print("fsfdfv")
                    date_a = value.date()
                    print(date_a)
                    # date_arra = f"{date_a}".split('-')
                    # print(date_arra)
                    # print("date_arra")
                    # print(date_arra)
                    # row[key] = datetime.datetime(int(date_arra[0]), int(date_arra[1]), int(date_arra[2])).date()
                    row[key] = date_a
            if key == "joining_date":
                print("joining_date")
                if value == None or value == "nan":
                    value = None
                if isinstance(value, str) and value.startswith("#"):
                    row[key] = datetime.strptime("01, 01, 1901", "%m, %d, %Y").strftime("%Y-%m-%d")
                else:
                    # formatted_date = datetime.strptime(value, "%m/%d/%Y").strftime("%Y-%m-%d")
                    formatted_date = datetime.today().strftime('%Y-%m-%d')
                    
                    row[key] = formatted_date
            if key == "student_class":
                print("student_class")
                # print(value)
                # print(row[key])
                if value == "" or value == 0:
                    pass
                else:
                    print(value)
                    # print(row[key])
                    # 
                    student_class_obj = ClassRoom.objects.get(id=value)
                    row[key] = student_class_obj.id
                    # row[key] = student_class_obj
                    row[key] = value
                    print(row[key])
            if key == "specialty":
                print("specialty")
                # print(value)
                # print(row[key])
                if value == "" or value == 0:
                    pass
                else:
                    print(value)
                    # print(row[key])
                    # 
                    specialty_class_obj = Specialty.objects.get(id=value)
                    row[key] = specialty_class_obj.id
                    # row[key] = specialty_class_obj
                    # row[key] = value
                    print(row[key])
            if key == "stud_image":
                print("stud_image")
                if value == "" or value == 0:
                    pass
                else:
                    print(value)
                    # print(row[key])
                    # 
                    stud_img_obj = Image.objects.get(id=value)
                    row[key] = stud_img_obj.id
                    # row[key] = stud_img_obj
                    # row[key] = value
                    print(row[key])
            if key == "parent":
                print("parent")
                print(value)
                print(type(value))
                test_arr = []
                test_arr.append(value)
                if value == "" or value == 4 or value == " " or value == 0 or pd.isnull(test_arr) :
                    value = None
                    print('position none ')
                    row[key] = value
                    # pass
                # if value == 4 :
                #     print('position 4 ')
                #     print(value)
                else:
                    print(value)
                    # info_arr = f"{value}".split('_')
                    print('position ')
                    info_arr = value.split('_')
                    print('position 0')
                    print(info_arr[0])
                    print('position 1')
                    print(info_arr[1])
                    # create parent
                    parent = Parent.objects.create(
                        carer_name = info_arr[0],
                        carer_mobile = info_arr[1],
                        present_address = "BUEA",
                        permanent_address = "BUEA",
                        added_by = "emnanlaptop",

                    )
                    row[key] = parent.id
                    print(row[key])
            if key == "student_uid":
                print("student_uid")
                print(value)
                    

            # elif key == "id":
            #     if isinstance(value, str):
            #         cleaned_value = int("".join(filter(str.isdigit, value)))
            #         row[key] = cleaned_value                    
            #     else:
            #         row[key] = value

        return row

    class Meta:
        model = Student
        # import_id_fields = ["student_uid", "roll_no"]
        import_id_fields = ["student_uid"]
        skip_unchanged = True
        use_bulk = True