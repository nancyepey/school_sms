from django.contrib import admin

#
from . models import ClassRoom, Settings, Specialty

#
from import_export import resources
from images.models import Image
from core.models import CustomUser
from teacher.models import Teacher



# Register your models here.

@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'class_code', 'class_department', 'slug')
    search_fields = ('class_name', 'class_code', 'class_department')
    list_filter = ('class_name', 'class_code', 'class_department')


admin.site.register(Settings)
admin.site.register(Specialty)



class SpecialtyResource(resources.ModelResource):
    class Meta:
        model = Specialty
        # 
        import_id_fields = ["code"]
        skip_unchanged = True
        use_bulk = True



class ImageResource(resources.ModelResource):
    class Meta:
        model = Image
        # 
        import_id_fields = ["cloudflare_id"]
        skip_unchanged = True
        use_bulk = True



class UserprofileResource(resources.ModelResource):
    def before_import_row(self, row, **kwargs):
        for key, value in row.items():
            if key == "name":
                print(value)
            if key == "last_login":
                print("valueeeeeeeeeeee")
                if type(value) == "nan" or  isinstance(value, float) or value=="" or  value==" ":
                    print("nan---")
                    row[key] = None
                    pass
                #   
                else:
                    print("fsfdfv")
                    print(value)
                    date_a = value
                    print(date_a)
                    # 
                    row[key] = date_a
                    # date_a = f"{value}".split(" ")
                    # print(date_a)
                    # # 
                    # row[key] = date_a[0]
            if key == "date_joined":
                print("valueeeeeeeeeeee")
                if type(value) == "nan" or  isinstance(value, float) or value=="" or  value==" ":
                    print("nan---")
                    row[key] = None
                    pass
                #   
                else:
                    print("fsfdfv")
                    # date_a = value.date()
                    # date_a = f"{value}".split(" ")
                    # print(date_a)
                    # # 
                    # row[key] = date_a[0]
                    date_a = value
                    row[key] = date_a
            if key == "teacher_profile_id":
                print("valueeeeeeeeeeee")
                if type(value) == "nan" or  isinstance(value, float) or value=="" or  value==" ":
                    print("nan---")
                    row[key] = None
                    pass
                #   
                else:
                    print("fsfdfv")
                    # get the teacher
                    get_teachprof = Teacher.objects.filter(name=value)
                    if len(get_teachprof) > 1:
                        row[key] = None
                    elif len(get_teachprof) == 1:
                        row[key] = get_teachprof
                    else:
                        row[key] = None


    class Meta:
        model = CustomUser
        # 
        import_id_fields = ["username"]
        skip_unchanged = True
        use_bulk = True





class TeacherResource(resources.ModelResource):
    def before_import_row(self, row, **kwargs):
        for key, value in row.items():
            if key == "teacher_uid":
                print("teacher_uid")
                print(value)
            if key == "date_of_birth":
                print("valueeeeeeeeeeee")
                if type(value) == "nan" or  isinstance(value, float) or value=="" or  value==" ":
                    print("nan---")
                    row[key] = None
                    pass
                #   
                else:
                    print("fsfdfv")
                    print(value)
                    date_a = value
                    print(date_a)
                    # 
                    row[key] = date_a
                    # date_a = f"{value}".split(" ")
                    # print(date_a)
                    # # 
                    # row[key] = date_a[0]
            if key == "joining_date":
                print("valueeeeeeeeeeee")
                if type(value) == "nan" or  isinstance(value, float) or value=="" or  value==" ":
                    print("nan---")
                    row[key] = None
                    pass
                #   
                else:
                    print("fsfdfv")
                    # date_a = value.date()
                    # date_a = f"{value}".split(" ")
                    # print(date_a)
                    # # 
                    # row[key] = date_a[0]
                    date_a = value
                    row[key] = date_a


    class Meta:
        model = Teacher
        # 
        import_id_fields = ["teacher_uid"]
        skip_unchanged = True
        use_bulk = True
























