import csv
import datetime
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
import pandas as pd

from core.models import CustomUser
from testeval.models import ReportCard
from teacher.models import Teacher
from subject.models import Subject
from student.models import Student
# from .models import Notification
from .models import ClassRoom, Settings, Specialty

from .models import Settings
from django.http import HttpResponseForbidden
from django.contrib import messages
#search
from django.db.models import Q
# csv
import csv 
from django.utils.text import slugify
import os
from tablib import Dataset
from school.admin import ImageResource, SpecialtyResource, TeacherResource, UserprofileResource
from school.forms import CSVImgImportForm, CSVSpecialtyImportForm, CSVStudsImportForm, CSVTeachImportForm, CSVUserImportForm

#login required
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def index(request):
    return render(request, "authentication/login.html")
    # return render(request, "home/index.html")


@login_required
def dashboard(request):
    company = Settings.objects.get(clientName='GILEAD TECHNICAL HIGH SCHOOL')
    user_info = Student.objects.get(id=request.user.student_profile.id)
    class_info = ClassRoom.objects.get(id=user_info.student_class.id)
    class_subjects = Subject.objects.filter(classroom=class_info.id)
    num_subjects = Subject.objects.filter(classroom=class_info.id).count()
    # print(num_subjects)
    #get number of subjects
    user_class = user_info.student_class.class_name
    # print(user_info.student_image.url)
    context = {
        'user_info': user_info,
        "user_class" : user_class,
        'company': company,
        "class_info" : class_info,
        "class_subjects" : class_subjects,
        "num_subjects" : num_subjects,
    }
    # unread_notification = Notification.objects.filter(user=request.user, is_read=False)
    # unread_notification_count = unread_notification.count()
    return render(request, "dashboard/student-dashboard.html", context)


@login_required
def admin_dashboard(request):
    company = Settings.objects.get(clientName='GILEAD TECHNICAL HIGH SCHOOL')
    classroom = ClassRoom.objects.all()
    count_class = ClassRoom.objects.all().count()
    count_subjects = Subject.objects.all().count()
    count_students = Student.objects.all().count()
    report_card_count = ReportCard.objects.select_related('student').filter(is_actif=True).count()
    print(f"{report_card_count}----report_card_count")
    context = {
        'company': company,
        "classroom" : classroom,
        "count_class" : count_class,
        "count_subjects" : count_subjects,
        "count_students" : count_students,
        "repcard_counts":report_card_count,
    }
    # unread_notification = Notification.objects.filter(user=request.user, is_read=False)
    # unread_notification_count = unread_notification.count()
    return render(request, "dashboard/admin-dashboard.html", context)


@login_required
def teacher_dashboard(request):
    company = Settings.objects.get(clientName='GILEAD TECHNICAL HIGH SCHOOL')
    if request.user.teacher_profile.id:
        user_info = Teacher.objects.get(id=request.user.teacher_profile.id)
    class_info = ClassRoom.objects.all()
    # class_subjects = Subject.objects.filter(classroom=class_info.id)
    # num_subjects = Subject.objects.filter(classroom=class_info.id).count()
    # print(num_subjects)
    #get number of subjects
    # user_class = user_info.student_class.class_name
    # print(user_info.student_image.url)
    context = {
        'user_info': user_info,
        # "user_class" : user_class,
        'company': company,
        "class_info" : class_info,
        # "class_subjects" : class_subjects,
        # "num_subjects" : num_subjects,
    }
    # unread_notification = Notification.objects.filter(user=request.user, is_read=False)
    # unread_notification_count = unread_notification.count()
    return render(request, "dashboard/teacher-dashboard.html", context)



@login_required
def import_export(request):
    class_list = ClassRoom.objects.all()
    specialty_list = Specialty.objects.all()
    
    form = CSVSpecialtyImportForm()
    form_img = CSVImgImportForm()
    form_usr = CSVUserImportForm()
    form_teach = CSVTeachImportForm()
    form_studs = CSVStudsImportForm()
    context = {
        'class_list': class_list,
        'specialty_list': specialty_list,
        'csv_specialty_import_form': form,
        'csv_img_import_form': form_img,
        'csv_usr_import_form': form_usr,
        'csvteach_import_form': form_teach,
        'csvstuds_import_form': form_studs,
    }
    
    if request.method == 'POST':
        # print(request)
        # form_img = CSVImgImportForm(request.POST, request.FILES)
        # if form_img.is_valid():
        #     # print("importttttttttt")
        #     csv_file = request.FILES['csv_file']
        #     csv_reader = pd.read_excel(csv_file, engine="openpyxl")
        #     # 

        #     file = request.FILES['csv_file']
        #     df = pd.read_excel(file)

        #     """Rename the headeers in the excel file
        #    to match Django models fields"""

        #     #Call the Specialty Resource Model and make its instance
        #     imgs_resource = ImageResource()

        #     # Load the pandas dataframe into a tablib dataset
        #     dataset = Dataset().load(csv_reader)
        #     # dataset = Dataset().load(df)

        #     # Call the import_data hook and pass the tablib dataset
        #     result = imgs_resource.import_data(dataset,\
        #      dry_run=True, raise_errors = True)
            
        #     if not result.has_errors():
        #         result = imgs_resource.import_data(dataset, dry_run=False)
        #         messages.success(request, "Images Data imported successfully")
        #         # return redirect('index')
        #         #
            
        #     else:
        #         messages.error(request, "Not Imported Images Data")
            #
        
        # user form import
        form_usr = CSVUserImportForm(request.POST, request.FILES)
        if form_usr.is_valid():
            # print("importttttttttt")
            csv_file = request.FILES['csv_file']
            csv_reader = pd.read_excel(csv_file, engine="openpyxl")
            # 

            file = request.FILES['csv_file']
            df = pd.read_excel(file)

            """Rename the headeers in the excel file
           to match Django models fields"""

            #Call the Specialty Resource Model and make its instance
            usrs_resource = UserprofileResource()

            # Load the pandas dataframe into a tablib dataset
            dataset = Dataset().load(csv_reader)
            # dataset = Dataset().load(df)

            # Call the import_data hook and pass the tablib dataset
            result = usrs_resource.import_data(dataset,\
             dry_run=True, raise_errors = True)
            
            if not result.has_errors():
                result = usrs_resource.import_data(dataset, dry_run=False)
                messages.success(request, "Users Data imported successfully")
                # return redirect('index')
                #
            
            else:
                messages.error(request, "Not Imported Users Data")
            #

        # teacher
        # form_teach = CSVTeachImportForm(request.POST, request.FILES)
        # # teach form import
        # if form_teach.is_valid():
        #     # print("importttttttttt")
        #     csv_file = request.FILES['csv_file']
        #     csv_reader = pd.read_excel(csv_file, engine="openpyxl")
        #     # 

        #     file = request.FILES['csv_file']
        #     df = pd.read_excel(file)

        #     """Rename the headeers in the excel file
        #    to match Django models fields"""

        #     #Call the Teacher Resource Model and make its instance
        #     teach_resource = TeacherResource()

        #     # Load the pandas dataframe into a tablib dataset
        #     dataset = Dataset().load(csv_reader)
        #     # dataset = Dataset().load(df)

        #     # Call the import_data hook and pass the tablib dataset
        #     result = teach_resource.import_data(dataset,\
        #      dry_run=True, raise_errors = True)
            
        #     if not result.has_errors():
        #         result = teach_resource.import_data(dataset, dry_run=False)
        #         messages.success(request, "Teacher Data imported successfully")
        #         # return redirect('index')
        #         #
            
        #     else:
        #         messages.error(request, "Not Imported Teacher Data")
        #     #
    #

    return render(request, "import_export/import_export.html", context)



@login_required
def class_list(request):
    class_list = ClassRoom.objects.all()
    context = {
        'class_list': class_list,
    }
    return render(request, "class/classes.html", context)


@login_required
def add_class(request):

    if request.method == "POST":
        name      = request.POST.get('name')
        code      = request.POST.get('code')
        dept       = request.POST.get('dept')
        added_by     = request.user.username
        # added_by = "emnanlaptop"
        # obj_student_class = ClassRoom.objects.filter(classroom)

        classroom = ClassRoom.objects.create(
            class_name = name,
            class_code = code,
            class_department = dept,
            added_by = request.user.username,
        )
        classroom.save()

        messages.success(request, f'{name} Class added Successfully')
        return redirect("class_list")
    return render(request, "class/add-class.html")



@login_required
def edit_class(request, slug):
    # classroom = ClassRoom.objects.get(id=slug)
    # context = {
    #     'classroom': classroom,
    # }
    class_room = get_object_or_404(ClassRoom, id=slug)
    context = {
        'classroom':class_room,
    }

    if request.method == "POST":
        name      = request.POST.get('name')
        code      = request.POST.get('code')
        dept       = request.POST.get('dept')
        modified_by     = request.user.username

        # 
        # obj_student_class = ClassRoom.objects.filter(classroom)

        
        class_room.class_name = name
        class_room.class_code = code
        class_room.class_department = dept
        # description = description,
        class_room.modified_by = modified_by

        # class_room.update()

        
        class_room.save()

        messages.success(request, 'Class updated Successfully')
        return redirect("class_list")
    return render(request, "class/edit-class.html", context) 

@login_required
def del_class(request, slug):
    if request.method == "POST":
        #
        classroom = get_object_or_404(ClassRoom, id = slug)
        classroom.delete()

        return redirect('class_list')
    return HttpResponseForbidden()




@login_required
def specialty_list(request):
    specialty_list = Specialty.objects.all()
    
    form = CSVSpecialtyImportForm()

    # search
    if 'q' in request.GET:
        search=request.GET['q']
        specialty_list =  Specialty.objects.filter(Q(name__contains = search) | Q(code__contains = search) |  Q(department__contains = search)  )

    context = {
        'specialty_list': specialty_list,
        'csv_specialty_import_form': form,
    }
    
    if request.method == 'POST':
        # print(request)
        form = CSVSpecialtyImportForm(request.POST, request.FILES)
        if form.is_valid():
            print("importttttttttt")
            csv_file = request.FILES['csv_file']
            csv_reader = pd.read_excel(csv_file, engine="openpyxl")
            # 

            file = request.FILES['csv_file']
            df = pd.read_excel(file)

            """Rename the headeers in the excel file
           to match Django models fields"""

            #Call the Specialty Resource Model and make its instance
            specialties_resource = SpecialtyResource()

            # Load the pandas dataframe into a tablib dataset
            dataset = Dataset().load(csv_reader)
            # dataset = Dataset().load(df)

            # Call the import_data hook and pass the tablib dataset
            result = specialties_resource.import_data(dataset,\
             dry_run=True, raise_errors = True)
            
            if not result.has_errors():
                result = specialties_resource.import_data(dataset, dry_run=False)
                messages.success(request, "Specialty Data imported successfully")
                # return Response({"status": "Specialty Data Imported Successfully"})
                # return redirect('index')
                #
            
            else:
                messages.error(request, "Not Imported Specialty Data")
            #
    # 

    return render(request, "specialty/specialty.html", context)



@login_required
def add_specialty(request):

    if request.method == "POST":
        name      = request.POST.get('name')
        code      = request.POST.get('code')
        # classroom      = request.POST.get('classroom')
        dept       = request.POST.get('dept')
        # other       = request.POST.get('other')
        added_by     = request.user.username,
        # added_by = "emnanlaptop"
        # obj_student_class = ClassRoom.objects.filter(classroom)

        specialty = Specialty.objects.create(
            name = name,
            code = code,
            department = dept,
            added_by = added_by, 
        )

        # obj_class = Specialty.objects.get(id=classroom)

        # specialty.classroom.add(obj_class)
        specialty.save()

        messages.success(request, 'specialty added Successfully')
        return redirect("specialty_list")
    return render(request, "specialty/add-specialty.html")



@login_required
def edit_specialty(request, slug):
    # classroom = ClassRoom.objects.get(id=slug)
    # context = {
    #     'classroom': classroom,
    # }
    specialty = get_object_or_404(Specialty, id=slug)
    context = {
        'specialty':specialty,
    }

    if request.method == "POST":
        name      = request.POST.get('name')
        code      = request.POST.get('code')
        # classroom      = request.POST.get('classroom')
        dept       = request.POST.get('dept')
        modified_by     = request.user.username,

        # 
        # obj_student_class = ClassRoom.objects.filter(classroom)

        
        specialty.name = name 
        specialty.code = code
        specialty.department = dept
        # description = description,
        specialty.modified_by = modified_by

        # specialty.update()

        # obj_class = Specialty.objects.get(id=classroom)

        # specialty.classroom.add(obj_class)

        
        specialty.save()

        messages.success(request, 'Specialty updated Successfully')
        return redirect("specialty_list")
    return render(request, "specialty/edit-specialty.html", context) 



@login_required
def del_specialty(request, slug):
    if request.method == "POST":
        #
        specialty = get_object_or_404(Specialty, id = slug)
        specialty.delete()

        return redirect('specialty_list')
    return HttpResponseForbidden()



@login_required
def companySettings(request):
    company = Settings.objects.get(clientName='GILEAD TECHNICAL HIGH SCHOOL')
    context = {'company': company}
    return render(request, 'company/company-settings.html', context)




@login_required
def class_generate_csv(request): 
    response = HttpResponse(content_type='text/csv') 
    formatted_datetime = datetime.datetime.now()
    file_name = f"classrooms_{formatted_datetime}.csv"
    response['Content-Disposition'] = f'attachment; filename={file_name}'

    response.write(u'\ufeff'.encode('utf8'))
  
    writer = csv.writer(response) 
    writer.writerow(["CLASSROOM / CLASS NAME", "CLASS CODE",  "CLASS DEPARTMENT"]) 
    # 

    classrooms = ClassRoom.objects.all() 
    for classroom in classrooms: 
        print("classroom_")
        # print(classroom)
            
        writer.writerow([ classroom.class_name, classroom.class_code, classroom.class_department]) 
        # 
  
    return response 


@login_required
def specialty_generate_csv(request): 
    response = HttpResponse(content_type='text/csv') 
    formatted_datetime = datetime.datetime.now()
    file_name = f"specialties_{formatted_datetime}.csv"
    response['Content-Disposition'] = f'attachment; filename={file_name}'

    response.write(u'\ufeff'.encode('utf8'))
  
    writer = csv.writer(response) 
    writer.writerow(["NAME", " CODE",  " DEPARTMENT"]) 
    # writer.writerow(["NAME", " CODE",  " DEPARTMENT"]) 
    # 

    specialty = Specialty.objects.all() 
    for specialty in specialty: 
        print("specialty_")
        # print(specialty)
            
        writer.writerow([ specialty.name, specialty.code, specialty.department]) 
        # 
  
    return response 

@login_required
def import_images(request):
    class_list = ClassRoom.objects.all()
    specialty_list = Specialty.objects.all()
    
    form = CSVSpecialtyImportForm()
    context = {
        'class_list': class_list,
        'specialty_list': specialty_list,
        'csv_specialty_import_form': form,
    }
    return render(request, "import_export/import_export.html", context)

@login_required
def import_users(request):
    class_list = ClassRoom.objects.all()
    specialty_list = Specialty.objects.all()
    
    form = CSVSpecialtyImportForm()
    context = {
        'class_list': class_list,
        'specialty_list': specialty_list,
        'csv_specialty_import_form': form,
    }
    return render(request, "import_export/import_export.html", context)