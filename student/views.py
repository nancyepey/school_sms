import datetime

from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect

from core.models import CustomUser
from student.admin import StudentResource
from student.forms import CSVImportForm
from images.models import Image
from images.services import upload_image_to_cloudflare
from school.models import ClassRoom, Specialty
#
from .models import Parent, Student
from django.contrib import messages

import uuid
import pandas as pd
from tablib import Dataset
from django.db.models import Q
# csv
import csv 
from django.utils.text import slugify
import os
from django.conf import settings
from student.utils_csv import get_lookup_fields, qs_to_dataset
# from django.http import HttpResponse #already imported above
#image cloudflare

from images import services as image_services

#login required
from django.contrib.auth.decorators import login_required



# Create your views here.

@login_required
def add_student(request):
    classroom = ClassRoom.objects.all()
    parents = Parent.objects.all()
    specialties = Specialty.objects.all()
    context = {
        'classroom':classroom,
        'parents':parents,
        "specialties":specialties,
    }

    if request.method == "POST":
        name = request.POST.get('student_name')
        username = request.POST.get('u_name')
        student_email = request.POST.get('student_email')
        student_uid = request.POST.get('student_uid')
        gender = request.POST.get('gender')
        status = request.POST.get('status')
        date_of_birth = request.POST.get('date_of_birth')
        place_of_birth = request.POST.get('place_of_birth')
        student_class = request.POST.get('student_class')
        specialty_class = request.POST.get('specialty_class')
        religion = request.POST.get('religion')
        joining_date = request.POST.get('joining_date')
        mobile_number = request.POST.get('mobile_number')
        admission_number = request.POST.get('admission_number')
        minesec_number = request.POST.get('minesec_number')
        section = request.POST.get('section')
        student_image = request.FILES.get('student_image')
        # added_by = request.POST.get('created_by')

        # retrieve parent data from the form
        parent_info = request.POST.get('parents')
        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation')
        father_mobile = request.POST.get('father_mobile')
        father_email = request.POST.get('father_email')
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation')
        mother_mobile = request.POST.get('mother_mobile')
        mother_email = request.POST.get('mother_email')
        carer_name = request.POST.get('carer_name')
        carer_occupation = request.POST.get('carer_occupation')
        carer_mobile = request.POST.get('carer_mobile')
        carer_email = request.POST.get('carer_email')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')
        # added_by = request.POST.get('created_by')

        if parent_info:
            #get parent
            parent = Parent.objects.get(id=parent_info)
        else:
            #creating a new parent
            #save parent info
            if father_name == "" and mother_name == "":
                parent = Parent.objects.create(
                    carer_name = carer_name,
                    carer_occupation = carer_occupation,
                    carer_mobile = carer_mobile,
                    carer_email = carer_email,
                    present_address = present_address,
                    permanent_address = permanent_address,
                    added_by = request.user.username,

                )
                # stu_email = carer_email
            else:
                parent = Parent.objects.create(
                    father_name = father_name,
                    father_occupation = father_occupation,
                    father_mobile = father_mobile,
                    father_email = father_email,
                    mother_name = mother_name,
                    mother_occupation = mother_occupation,
                    mother_mobile = mother_mobile,
                    mother_email = mother_email,
                    present_address = present_address,
                    permanent_address = permanent_address,
                    added_by = request.user.username,
                )

        # generating username
        # Change all uppercase letters to lowercase
        res = name.lower()
        # print(res)
        res_arr = res.split()
        last_element = res_arr[-1] 
        uname = f"{last_element}.{res_arr[0]}"
        # print("uname")
        # print(uname)
        username = uname
        uniqv = uuid.uuid4()
        val_unique = f"{uniqv}"[:4]
        password = f"{username}_{val_unique}"

        stu_u_email = ""

        
        if student_email == "":
            stu_u_email = f"{username}@gmail.com"
            if father_email == "":
                stu_email = mother_email
            if carer_email == "":
                stu_email = carer_email
        else:
            stu_email = student_email
            stu_u_email = student_email
        

        
        # try:
        #     img_cloudflare_id = upload_image_to_cloudflare(student_image)
        #     image = Image.objects.create(
        #         title = f"{username}_{student_uid}",
        #         cloudflare_id = img_cloudflare_id,
        #         added_by = request.user.username,
        #     )
        #     print(img_cloudflare_id)
        #     print(image)
        # except:
        #     print("image not uploaded")
            # messages.error(request, 'Something went wrong')
        
        if joining_date == "":
            joining_date = None
        
        if date_of_birth == "":
            date_of_birth = None


        # save student information

        #get student class
        # print(student_class)
        obj_student_class = ClassRoom.objects.get(id=student_class)
        # specialty_class
        obj_specialty_class = Specialty.objects.get(id=specialty_class)

        

        student = Student.objects.create(
            name = name,
            student_uid = student_uid,
            gender = gender,
            date_of_birth = date_of_birth,
            place_of_birth = place_of_birth,
            student_class = obj_student_class,
            specialty = obj_specialty_class,
            sch_status = status,
            religion = religion,
            joining_date = joining_date,
            mobile_number = mobile_number,
            admission_number = admission_number,
            minesec_ident_num = minesec_number,
            section = section,
            student_image = student_image,
            # stud_image = obj_studimage_class,
            parent = parent, 
            added_by = request.user.username,
        )


        # save image online
        img_cloudflare_id = upload_image_to_cloudflare(student_image)
        image = Image.objects.create(
            title = f"{student.student_uid}_{student_uid}",
            cloudflare_id = img_cloudflare_id,
            added_by = request.user.username,
        )
        
        # print("image")
        # print(img_cloudflare_id)
        # print(image)

        # studimage_class
        obj_studimage_class = Image.objects.get(cloudflare_id=image.cloudflare_id)

        # open file 
        student.student_image.open()
        student.stud_image = obj_studimage_class
        student.save()


        #
        

        # Create the user
        user = CustomUser.objects.create_user(
            username=username,
            email=stu_u_email,
            name=name,
            password="GTECH",
            # photo = student_image,
            student_profile = student
        )
        
        # Assign student role
        user.is_student = True

        # open file 
        user.photo.open()

        user.save()

        messages.success(request, f' {name} Student added Successfully')
        return redirect("student_list")
        # return render(request, "student_list")
    

    return render(request, "students/add-student.html", context=context)


def display_image( cloudflare_id):
    if cloudflare_id:
        img_url = image_services.get_image_url_from_cloudflare(
            cloudflare_id, variant="thumbnailSmall"
            # obj.stud_image.cloudflare_id
        )
        print("obj")
        return img_url
    return "https://imagedelivery.net/FGazjujafzdf38AXQFJ0qw/834941c7-4e47-4404-a47c-c27bd18a4e00/thumbnailSmall"
    # myimage = display_image(obj_student_class)


@login_required
def student_list(request):
    student_list = Student.objects.select_related('parent').all()
    # print(student_list)
    # print(student_list[0].student_image)
    classroom = ClassRoom.objects.all()
    specialtys = Specialty.objects.all()
    form = CSVImportForm()
    displayimages = []

    # search
    if 'q' in request.GET:
        search=request.GET['q']
        # student_list =  Student.objects.filter(name__startswith = search )
        student_list =  Student.objects.filter(Q(name__contains = search) | Q(student_uid__contains = search) | Q(admission_number__contains = search)  | Q(minesec_ident_num__contains = search) )
    
        # for students in student_list:
        #     if students.stud_image:
        #         myimage = display_image(students.stud_image.cloudflare_id)
        #         displayimages.append(myimage)

    # for students in student_list:
    #     if students.stud_image:
    #         myimage = display_image(students.stud_image.cloudflare_id)
    #         displayimages.append(myimage)
    #         print("ok")
    
    # print(displayimages)

        
    context = {
        'student_list': student_list,
        # 'imgs_student_list': displayimages,
        'classroom':classroom,
        'specialtys':specialtys,
        'csv_import_form': form,
        "curent_rslt": "all_all",
    }


    # if request.method == 'GET':
    #     print("get")
    #     search = request.GET.get('search')
    #     payload_get = []
    #     if search:
    #         objs_get = Student.objects.filter(Q(name__startswith = search) | Q(student_uid__startswith = search) )
    #         return JsonResponse({
    #             'status': True,
    #             'payload': payload_get
    #         })

    # print(context)
    if request.method == 'POST':
        # print(request)
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            print("importttttttttt")
            # csv_file = request.FILES['csv_file'].read().decode('utf-8').splitlines()
            csv_file = request.FILES['csv_file']
            # csv_reader = csv.DictReader(csv_file)
            # csv_reader = pd.read_excel(csv_file)
            csv_reader = pd.read_excel(csv_file, engine="openpyxl")
            # headers = csv_reader.fieldnames
            # indices = [headers.index(col) for col in csv_reader.restval]
            # data = []

            file = request.FILES['csv_file']
            df = pd.read_excel(file)

            """Rename the headeers in the excel file
           to match Django models fields"""
            # rename_columns = {"Student Email": "email", "Student Name": "name",\
            #               "Roll Number": "roll_no", "Year": "year"}
        
            # csv_reader.rename(columns = rename_columns, inplace=True)

            #Call the Student Resource Model and make its instance
            students_resource = StudentResource()

            # Load the pandas dataframe into a tablib dataset
            dataset = Dataset().load(csv_reader)
            # dataset = Dataset().load(df)

            # Call the import_data hook and pass the tablib dataset
            result = students_resource.import_data(dataset,\
             dry_run=True, raise_errors = True)
            
            if not result.has_errors():
                result = students_resource.import_data(dataset, dry_run=False)
                messages.success(request, "Student Data imported successfully")
                # return Response({"status": "Student Data Imported Successfully"})
                # return redirect('index')
            
            else:
                messages.error(request, "Not Imported Student Data")
            # return Response({"status": "Not Imported Student Data"},\
            #      status=status.HTTP_400_BAD_REQUEST)
            # return render(request, 'students/students.html.html', context)
        else: 
            class_selected = request.POST.get('student_class')
            specialty_selected = request.POST.get('stud_specialty')
            displayimages = []
            if class_selected == "all":
                get_class = ClassRoom.objects.all()
                if specialty_selected == "all":
                    student_list = Student.objects.all()
                    # for students in student_list:
                    #     if students.stud_image:
                    #         myimage = display_image(students.stud_image)
                    #         displayimages.append(myimage)
                    get_specialty = Specialty.objects.all()
                    context = {
                        'student_list': student_list,
                        # 'imgs_student_list': displayimages,
                        'classroom':classroom,
                        'class_selected': class_selected,
                        'get_specialty': get_specialty,
                        'specialtys':specialtys,
                        "curent_rslt": f"{specialty_selected}_{class_selected}"
                    }
                else:
                    get_specialty = Specialty.objects.get(id = specialty_selected)
                    student_list = Student.objects.filter(specialty= get_specialty)
                    # for students in student_list:
                    #     if students.stud_image:
                    #         myimage = display_image(students.stud_image.cloudflare_id)
                    #         displayimages.append(myimage)
                    context = {
                        'student_list': student_list,
                        # 'imgs_student_list': displayimages,
                        'classroom':classroom,
                        'class_selected': class_selected,
                        'get_specialty': get_specialty,
                        'specialtys':specialtys,
                        'specialty_selected': get_specialty.name ,
                        "curent_rslt": f"{specialty_selected}_{class_selected}"
                    }
            else:
                get_class = ClassRoom.objects.get(id = class_selected)
                
                if specialty_selected == "all":
                    get_specialty = Specialty.objects.all()
                    student_list = Student.objects.filter(student_class=get_class)
                    # for students in student_list:
                    #     if students.stud_image:
                    #         myimage = display_image(students.stud_image.cloudflare_id)
                    #         displayimages.append(myimage)
                    specialty_selected = "all"
                    context = {
                        'student_list': student_list,
                        # 'imgs_student_list': displayimages,
                        'classroom':classroom,
                        'class_selected': get_class.class_name,
                        'get_specialty': get_specialty,
                        'specialtys':specialtys,
                        # 'specialty_selected': get_specialty.name ,
                        'codeclass_selected': get_class.class_code ,
                        "curent_rslt": f"{specialty_selected}_{class_selected}"
                    }
                else:
                    get_specialty = Specialty.objects.get(id = specialty_selected)
                    student_list = Student.objects.filter(student_class=get_class, specialty= get_specialty)
                    # for students in student_list:
                    #     if students.stud_image:
                    #         myimage = display_image(students.stud_image.cloudflare_id)
                    #         displayimages.append(myimage)
                    context = {
                        'student_list': student_list,
                        # 'imgs_student_list': displayimages,
                        'classroom':classroom,
                        'class_selected': get_class.class_name,
                        'get_specialty': get_specialty,
                        'specialtys':specialtys,
                        'specialty_selected': get_specialty.name ,
                        'codeclass_selected': get_class.class_code ,
                        "curent_rslt": f"{specialty_selected}_{class_selected}"
                    }
            # context = {
            #     'student_list': student_list,
            #     'classroom':classroom,
            #     'class_selected': class_selected,
            #     'get_specialty': get_specialty,
            #     'specialtys':specialtys,
            #     'specialty_selected': get_specialty.name ,
            #     'codeclass_selected': get_class.class_code ,
            # }
            
            # if specialty_selected == "all":
            #     if class_selected == "all":
            #         student_list = Student.objects.all()
                    
            #     else:
            #         student_list = Student.objects.filter(student_class=get_class)
            #         class_selected = get_class.class_name
            #     get_specialty = Specialty.objects.all()
            #     context = {
            #         'student_list': student_list,
            #         'classroom':classroom,
            #         'class_selected': class_selected,
            #         'get_specialty': get_specialty,
            #         'specialtys':specialtys,
            #     }
            # else:
            #     get_specialty = Specialty.objects.get(id = specialty_selected)
            #     student_list = Student.objects.filter(student_class=get_class, specialty= get_specialty)
            #     context = {
            #         'student_list': student_list,
            #         'classroom':classroom,
            #         'specialtys':specialtys,
            #         'class_selected': get_class.class_name,
            #         'specialty_selected': get_specialty.name,
            #         'codeclass_selected': get_class.class_code,
            #     }



            if student_list:
                student_list = student_list
            else:
                student_list = {}

    # downloadcsv
    if 'csv' in request.GET:
        downloadcsv=request.GET['csv']
        print(downloadcsv)
        generate_csv(request, student_list)
        

    return render(request, "students/students.html", context)



# def edit_student(request, slug):
#     student = get_object_or_404(Student, id = slug)
#     #get parent info
#     parent = student.parent if hasattr(student, 'parent') else None
#     #classromm
#     classroom = ClassRoom.objects.all()
#     context = {
#         'student': student, 
#         'parent': parent,
#         'classroom':classroom,
#     }

#     if request.method == "POST":
#         name = request.POST.get('student_name')
#         student_uid = request.POST.get('student_uid')
#         gender = request.POST.get('gender')
#         date_of_birth = request.POST.get('date_of_birth')
#         student_class = request.POST.get('student_class')
#         religion = request.POST.get('religion')
#         joining_date = request.POST.get('joining_date')
#         mobile_number = request.POST.get('mobile_number')
#         admission_number = request.POST.get('admission_number')
#         section = request.POST.get('section')
#         student_image = request.FILES.get('student_image')
#         # added_by = request.POST.get('created_by')

#         #save parent info
        
        
#         # save student information

#         #get student class
#         print(student_class)
#         student_class_obj = ClassRoom.objects.get(id=student_class)
#         print(student_class_obj)
#         # Student.objects.filter(id=slug).update(student_class=student_class)

#         # 

#         student.name = name
#         student.gender = gender
#         # student.date_of_birth = date_of_birth
#         student.student_class_id = student_class_obj
#         student.religion = religion
#         student.joining_date = joining_date
#         student.mobile_number = mobile_number
#         student.admission_number = admission_number
#         student.section = section
#         # student.student_image = student_image
#         student.student_uid = student_uid
#         student.modified_by = request.user.username
#         student.save()

#         # retrieve parent data from the form
#         parent.father_name = request.POST.get('father_name')
#         parent.father_occupation = request.POST.get('father_occupation')
#         parent.father_mobile = request.POST.get('father_mobile')
#         parent.father_email = request.POST.get('father_email')
#         parent.mother_name = request.POST.get('mother_name')
#         parent.mother_occupation = request.POST.get('mother_occupation')
#         parent.mother_mobile = request.POST.get('mother_mobile')
#         parent.mother_email = request.POST.get('mother_email')
#         parent.carer_name = request.POST.get('carer_name')
#         parent.carer_occupation = request.POST.get('carer_occupation')
#         parent.carer_mobile = request.POST.get('carer_mobile')
#         parent.carer_email = request.POST.get('carer_email')
#         parent.present_address = request.POST.get('present_address')
#         parent.permanent_address = request.POST.get('permanent_address')
#         parent.modified_by = request.user.username

#         parent.save() #save parent
        

        
#         # return render(request, 'student_list')
#         return redirect('student_list')
    
#     return render(request, "students/edit-student.html", context)


@login_required
def edit_student(request,slug):
    student = get_object_or_404(Student, id=slug)
    parent = student.parent if hasattr(student, 'parent') else None
    classroom = ClassRoom.objects.all()
    parents = Parent.objects.all()
    specialties = Specialty.objects.all()
    if request.method == "POST":
        # first_name = request.POST.get('first_name')
        name = request.POST.get('name')
        student_uid = request.POST.get('student_uid')
        gender = request.POST.get('gender')
        status = request.POST.get('status')
        date_of_birth = request.POST.get('date_of_birth')
        place_of_birth = request.POST.get('place_of_birth')
        student_class = request.POST.get('student_class')
        specialty_class = request.POST.get('specialty_class')
        religion = request.POST.get('religion')
        joining_date = request.POST.get('joining_date')
        mobile_number = request.POST.get('mobile_number')
        admission_number = request.POST.get('admission_number')
        minesec_number = request.POST.get('minesec_number')
        section = request.POST.get('section')
        # student_image = request.FILES.get('student_image')  if request.FILES.get('student_image') else student.student_image

        
        
        if joining_date == "":
            joining_date = None
        
        if date_of_birth == "":
            date_of_birth = None
            
        haschange = "non"
        if request.FILES.get('student_image'):
            student_image = request.FILES.get('student_image')
            haschange = "oui"
        else: 
            # student_image = student.student_image
            haschange = "non"
            
        # student_image = request.FILES.get('student_image')  if request.FILES.get('student_image') else student.student_image

        # Retrieve parent data from the form
        parent_info = request.POST.get('parents')

        
        isparentnew = request.POST.get('new_parent')

        # print(parent_info)
        father_name       = request.POST.get('father_name')
        mother_name       = request.POST.get('mother_name')
        father_occupation = request.POST.get('father_occupation')
        father_mobile     = request.POST.get('father_mobile')
        father_email      = request.POST.get('father_email')
        mother_occupation = request.POST.get('mother_occupation')
        mother_mobile     = request.POST.get('mother_mobile')
        mother_email      = request.POST.get('mother_email')
        present_address   = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')
        carer_name        =  request.POST.get('carer_name')
        carer_occupation  =  request.POST.get('carer_occupation')
        carer_mobile      =  request.POST.get('carer_mobile')
        carer_email       =  request.POST.get('carer_email')

        if isparentnew == "oui":
            print(isparentnew)
            #creating a new parent
            #save parent info
            if father_name == "" and mother_name == "":
                parent = Parent.objects.create(
                    carer_name = carer_name,
                    carer_occupation = carer_occupation,
                    carer_mobile = carer_mobile,
                    carer_email = carer_email,
                    present_address = present_address,
                    permanent_address = permanent_address,
                    added_by = request.user.username,

                )
                # stu_email = carer_email
            else:
                parent = Parent.objects.create(
                    father_name = father_name,
                    father_occupation = father_occupation,
                    father_mobile = father_mobile,
                    father_email = father_email,
                    mother_name = mother_name,
                    mother_occupation = mother_occupation,
                    mother_mobile = mother_mobile,
                    mother_email = mother_email,
                    present_address = present_address,
                    permanent_address = permanent_address,
                    added_by = request.user.username,
                )
        else:

            if parent_info:
                #get parent
                parent = Parent.objects.get(id=parent_info)
            else:
                #edit parent
                if parent_info == "":
                    parent.father_name = request.POST.get('father_name')
                    print(parent.father_name)
                    parent.father_occupation = request.POST.get('father_occupation')
                    parent.father_mobile = request.POST.get('father_mobile')
                    parent.father_email = request.POST.get('father_email')
                    parent.mother_name = request.POST.get('mother_name')
                    parent.mother_occupation = request.POST.get('mother_occupation')
                    parent.mother_mobile = request.POST.get('mother_mobile')
                    parent.mother_email = request.POST.get('mother_email')
                    parent.present_address = request.POST.get('present_address')
                    parent.permanent_address = request.POST.get('permanent_address')

                    parent.save()

#  update student information

        # student.first_name= first_name

        if haschange == "oui":
            student.student_image = student_image
            student.student_image.open()
        
        # student.student_image = student_image
        student.name= name
        student.student_uid= student_uid
        student.gender= gender
        student.date_of_birth= date_of_birth
        student.place_of_birth= place_of_birth

        student_class_obj = ClassRoom.objects.get(id=student_class)
        # specialty_class
        specialty_class_obj = Specialty.objects.get(id=specialty_class)

        student.parent = parent

        student.student_class= student_class_obj
        student.specialty= specialty_class_obj
        

        student.sch_status = status


        student.religion= religion
        student.joining_date= joining_date
        student.mobile_number = mobile_number
        student.admission_number = admission_number
        student.minesec_ident_num = minesec_number
        student.section = section
        # student.student_image = student_image
        student.modified_by = request.user.username

        
        student.save()

        

        if haschange == "oui":
            # student.student_image = student_image
            student.modified_by = request.user.username

            # save image online
            img_cloudflare_id = upload_image_to_cloudflare(student_image)
            image = Image.objects.create(
                title = f"{student.student_uid}_{student_uid}",
                cloudflare_id = img_cloudflare_id,
                added_by = request.user.username,
            )
            # studimage_class
            obj_studimage_class = Image.objects.get(cloudflare_id=image.cloudflare_id)
            # open file 
            # student.student_image.open()
            student.stud_image = obj_studimage_class
            # student.student_image.open()

            student.save()

        # create_notification(request.user, f"Added Student:  {student.name}")

        messages.success(request, f'{name}  Updated Successfully')
        
        return redirect("student_list")
    return render(request, "students/edit-student.html",{'student':student, 'parent':parent, 'parents':parents, 'classroom':classroom, "specialties":specialties} )


@login_required
def view_student(request, slug):
    student = get_object_or_404(Student, id = slug)
    context = {
        'student': student,
    }
    return render(request, "students/student-details.html", context)


@login_required
def delete_student(request, slug):
    if request.method == "POST":
        #
        student = get_object_or_404(Student, id = slug)
        name = student.name
        student.delete()

        messages.error(request, f'{name} Deleted Successfully')

        return redirect('student_list')
    return HttpResponseForbidden()


@login_required
def generate_csv(request, student_list): 
    response = HttpResponse(content_type='text/csv') 
    formatted_datetime = datetime.datetime.now()
    file_name = f"students_{formatted_datetime}.csv"
    response['Content-Disposition'] = f'attachment; filename={file_name}'

    response.write(u'\ufeff'.encode('utf8'))
  
    writer = csv.writer(response) 
    writer.writerow(["NAME", "STATUS", "CLASS", "SPECIALTY", "SEX", "DATE OF BIRTH", "PLACE OF BIRTH", "ADMISSION NUMBER", "MINESEC IDENTIFICATION NUMBER", "PARENT NAME", "PARENT CONTACT"]) 

    # 

    students = Student.objects.all() 
    if student_list:
        print("student_list")
        print(student_list)
        get_selections_arr = student_list.split('_')
        specialty_selected = get_selections_arr[0]
        class_selected     = get_selections_arr[1]
        if class_selected != "all":
            class_required = ClassRoom.objects.get(id=class_selected)
        if specialty_selected != "all":
            specialty_required = Specialty.objects.get(id=specialty_selected)
        if class_selected == "all" and specialty_selected == "all":
            students = Student.objects.all() 
        elif class_selected == "all" and specialty_selected != "all":
            students = Student.objects.filter(specialty = specialty_required)
        elif class_selected != "all" and specialty_selected == "all":
            students = Student.objects.filter(student_class = class_required)
        elif class_selected != "all" and specialty_selected != "all":
            students = Student.objects.filter(student_class = class_required, specialty = specialty_required)
    for student in students: 
        print("student_")
        print(student)
        if student == "<":
            pass
        else:
            sexe_stud = "G"
            parent_i = ""
            parent_num = ""
            if student.gender == "Female":
                sexe_stud = "G"
            else:
                sexe_stud = "B"
            if student.parent.father_name == "" or student.parent.mother_name == "":
                # print("eee")
                parent_i = student.parent.carer_name
                parent_num = student.parent.carer_mobile
            else:
                if student.parent.father_name != "":
                    parent_i = student.parent.father_name
                    parent_num = student.parent.father_mobile
                else:
                    parent_i = student.parent.mother_name
                    parent_num = student.parent.mother_mobile
            
            writer.writerow([student.name, student.sch_status, student.student_class.class_name, student.specialty.name, sexe_stud, student.date_of_birth, student.place_of_birth, student.admission_number, student.minesec_ident_num, parent_i, parent_num]) 
        # 
  
    return response 


# BASE_DIR = settings.BASE_DIR

# def qs_to_local_csv(qs, fields=None, path=None, filename=None):
#     if path is None:
#         path = os.path.join(os.path.dirname(BASE_DIR), 'csvstorage')
#         if not os.path.exists(path):
#             '''
#             CSV storage folder doesn't exist, make it!
#             '''
#             os.mkdir(path)
#     if filename is None:
#         model_name = slugify(qs.model.__name__)
#         filename = "{}.csv".format(model_name)
#     filepath = os.path.join(path, filename)
#     lookups = get_lookup_fields(qs.model, fields=fields)
#     dataset = qs_to_dataset(qs, fields)
#     rows_done = 0
#     with open(filepath, 'w') as my_file:
#         writer = csv.DictWriter(my_file, fieldnames=lookups)
#         writer.writeheader()
#         for data_item in dataset:
#             writer.writerow(data_item)
#             rows_done += 1
#     print("{} rows completed".format(rows_done))