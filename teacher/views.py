
import csv
import datetime
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect

from core.models import CustomUser
from subject.models import Subject
from school.models import ClassRoom
#
from .models import Teacher
from django.contrib import messages
#
from images.models import Image
from images.services import upload_image_to_cloudflare
import uuid
from django.db.models import Q
#
# images
from images.models import Image

#login required
from django.contrib.auth.decorators import login_required



# Create your views here.


@login_required
def add_teacher(request):
    subject = Subject.objects.all()
    classroom = ClassRoom.objects.all()
    context = {
        'subject':subject,
        'classroom': classroom
    }
    # print(classroom)
    # print(subject)
    # context = {}

    if request.method == "POST":
        name = request.POST.get('teacher_name')
        # username = request.POST.get('u_name')
        teacher_uid = request.POST.get('teacher_uid')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        teacher_subj = request.POST.get('teacher_subj')
        classteach = request.POST.get('classteach')
        joining_date = request.POST.get('joining_date')
        mobile_number = request.POST.get('mobile_number')
        section = request.POST.get('section')
        teacher_image = request.FILES.get('teacher_image')
        email = request.POST.get('email')
        permanent_address = request.POST.get('permanent_address')

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

        if teacher_uid == "":
            teacher_uid = uname
        
        if joining_date == "":
            joining_date = None
        
        if date_of_birth == "":
            date_of_birth = None

        
        
        # save teacher information

        #get teacher class
        # print(teacher_subj)
        obj_teacher_subj = Subject.objects.get(id=teacher_subj)
        obj_classteach = ClassRoom.objects.get(id=classteach)

        teacher = Teacher.objects.create(
            name = name,
            teacher_uid = teacher_uid,
            usname = username,
            idontknow  = password,
            gender = gender,
            date_of_birth = date_of_birth,
            # teacher_subj = obj_teacher_subj,
            # classteach = obj_classteach,
            joining_date = joining_date,
            mobile_number = mobile_number,
            email = email,
            section = section,
            permanent_address = permanent_address,
            teacher_image = teacher_image,
            added_by = request.user.username,
        )

        teacher.classrooms.add(obj_classteach)
        teacher.t_subjects.add(obj_teacher_subj)
        teacher.save()

        # Create the user
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            name=name,
            password=password,
            photo = teacher_image,
            teacher_profile = teacher
        )
        
        # Assign student role
        user.is_teacher = True

        user.save()

        if teacher_image:
            #
            teacher.teachprofile_id = user.id
            teacher.modified_by = request.user.username
            # save image online
            img_cloudflare_id = upload_image_to_cloudflare(teacher_image)
            image = Image.objects.create(
                title = f"{teacher.teacher_uid}_{teacher_uid}",
                cloudflare_id = img_cloudflare_id,
                added_by = request.user.username,
            )

            # studimage_class
            obj_studimage_class = Image.objects.get(cloudflare_id=image.cloudflare_id)

            # open file 
            teacher.teacher_image.open()
            teacher.teach_image = obj_studimage_class
            teacher.save()

        messages.success(request, f' {name} Teacher added Successfully')
        return redirect("teacher_list")
        # return render(request, "teacher_list")
    

    return render(request, "teachers/add-teacher.html", context=context)


@login_required
def teacher_list(request):
    teacher_list = Teacher.objects.all()

    # search
    if 'q' in request.GET:
        search=request.GET['q']
        teacher_list =  Teacher.objects.filter(Q(name__contains = search) | Q(teacher_uid__contains = search) | Q(usname__contains = search)  )

    context = {
        'teacher_list': teacher_list,
    }
    return render(request, "teachers/teachers.html", context)


@login_required
def edit_teacher(request,slug):
    teacher = get_object_or_404(Teacher, id=slug)
    subject = Subject.objects.all()
    classroom = ClassRoom.objects.all()
    class_notselected_objects = []
    subj_notselected_objects = []

    print(len(class_notselected_objects))
    

    for teachclassroom in teacher.classrooms.all():
        for classrm in classroom :
            if teachclassroom.id == classrm.id:
                pass
            else:
                class_notselected_objects.append(classrm)
                # print(classrm)

    

    for teachsubj in teacher.t_subjects.all():
        for subjt in subject :
            if teachsubj.id == subjt.id:
                pass
            else:
                subj_notselected_objects.append(subjt)
    # for teachsubj in teacher.t_subjects.all():
    #     for subjt in subject :
    #         if teachsubj.id == subjt.id:
    #             pass
    #         else:
    #             # check if its not already there
    #             if len(subj_notselected_objects) > 0:
    #                 for elt in subj_notselected_objects:
    #                     if elt.id == subjt.id:
    #                         pass
    #                     else:
    #                         subj_notselected_objects.append(subjt)
    #                         # print(subjt)
    #             else:
    #                 subj_notselected_objects.append(subjt)
    
    # for teachclassroom in teacher.classrooms.all():
    #     # print(f"{classrm.class_name}_classrm")
    #     for classrm in classroom :
    #         # print(f"{classrm.class_name}_classrm.class_name")
    #         # print(f"{teachclassroom}_teachclassroom")
    #         if teachclassroom.id == classrm.id:
    #             print(f"{classrm.class_name}_classrm")
    #         else:
    #             print(f"{classrm.class_name}_classrm")
    
    # else:


    # context = {
    # }
    if request.method == "POST":
        name = request.POST.get('name')
        teacher_uid = request.POST.get('teacher_uid')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        teacher_subj = request.POST.get('teacher_subj')
        joining_date = request.POST.get('joining_date')
        mobile_number = request.POST.get('mobile_number')
        section = request.POST.get('section')
        teacher_classteach = request.POST.getlist('classteach')
        # teacher_image = request.FILES.get('teacher_image')  if request.FILES.get('teacher_image') else teacher.teacher_image

        haschange = "non"
        if request.FILES.get('teacher_image'):
            teacher_image = request.FILES.get('teacher_image')
            haschange = "oui"
        else: 
            # teacher_image = student.teacher_image
            haschange = "non"

        # generating username
        # Change all uppercase letters to lowercase
        res = name.lower()
        # print(res)
        res_arr = res.split()
        last_element = res_arr[-1] 
        uname = f"{last_element}.{res_arr[0]}"
        # print("uname")
        # print(uname)
        # username = uname
        # uniqv = uuid.uuid4()
        # val_unique = f"{uniqv}"[:4]
        # password = f"{username}_{val_unique}"

        subjs_names = teacher_subj

        # 
        if teacher_uid == "":
            teacher_uid = uname
        
        if joining_date == "":
            joining_date = None
        
        if date_of_birth == "":
            date_of_birth = None

        # 
        print("subjs_names")
        print(subjs_names)

        # subjs_names = teacher_subj
        teacher.t_subjects.set([subjs_names])
        
        # classteach_objects = []
        # for sub in classteach_names:
        #     classteach_objects.append(ClassRoom.objects.get(id=sub))
        
        # print(classteach_objects)

        if haschange == "oui":
            teacher.teacher_image = teacher_image
            teacher.teacher_image.open()

        # teacher.first_name= first_name
        teacher.name= name
        teacher.teacher_uid= teacher_uid
        teacher.gender= gender
        teacher.date_of_birth= date_of_birth

        # teacher_subj_obj = Subject.objects.get(id=teacher_subj)

        # teacher.t_subjects = teacher_subj_obj
        classteach_names = teacher_classteach
        teacher.classrooms.set(classteach_names)
        # print(teacher.classrooms.all())

        teacher.joining_date= joining_date
        teacher.mobile_number = mobile_number
        teacher.section = section
        # teacher.teacher_image = teacher_image
        teacher.modified_by = request.user.username
        teacher.save()

        

        

        if haschange == "oui":
            # teacher.teacher_image = teacher_image
            teacher.modified_by = request.user.username

            # teacher.teacher_image.open()

            # save image online
            img_cloudflare_id = upload_image_to_cloudflare(teacher_image)
            image = Image.objects.create(
                title = f"{teacher.teacher_uid}_{teacher_uid}",
                cloudflare_id = img_cloudflare_id,
                added_by = request.user.username,
            )
            # studimage_class
            
            obj_teachimage_class = Image.objects.get(cloudflare_id=image.cloudflare_id)
            # open file 
            # teacher.teacher_image.open()
            
            teacher.teach_image = obj_teachimage_class
        

            teacher.save()


        # create_notification(request.user, f"Added Teacher:  {teacher.name}")

        messages.success(request, f'{name}  Updated Successfully')
        
        return redirect("teacher_list")
    return render(request, "teachers/edit-teacher.html",{'teacher':teacher,  'subject':subject, 'classroom': classroom, 'class_notselected_objects':class_notselected_objects, 'subj_notselected_objects':subj_notselected_objects } )


@login_required
def view_teacher(request, slug):
    teacher = get_object_or_404(Teacher, id = slug)
    context = {
        'teacher': teacher
    }
    return render(request, "teachers/teacher-details.html", context)


@login_required
def delete_teacher(request, slug):
    if request.method == "POST":
        #
        teacher = get_object_or_404(Teacher, id = slug)
        name = teacher.name
        teacher.delete()

        messages.error(request, f'{name}  Deleted Successfully')

        return redirect('teacher_list')
    return HttpResponseForbidden()


@login_required
def teacher_generate_csv(request): 
    response = HttpResponse(content_type='text/csv') 
    formatted_datetime = datetime.datetime.now()
    file_name = f"teachers_{formatted_datetime}.csv"
    response['Content-Disposition'] = f'attachment; filename={file_name}'

    response.write(u'\ufeff'.encode('utf8'))
  
    writer = csv.writer(response) 
    writer.writerow(["NAME", " TEACHER UNIQUE ID",  "USERNAME", "GIVEN PASSWORD", "USER PROFILE", "TEACHER IMAGE", "TEACHER IMAGE ID", "GENDER", "SUBJECTS" , "CLASSROOMS", "DATE OF BIRTH", "NUMBER", "EMAIL", "ADDRESS"]) 
    # 

    teachers = Teacher.objects.all() 
    for teacher in teachers: 
        # print("teacher_")
        # print(teacher)
        teach_class = ""
        teach_sub = ""
        for teachclassroom in teacher.classrooms.all():
            teach_class += f"{teachclassroom.id}_"

        

        for teachsubj in teacher.t_subjects.all():
            teach_sub += f"{teachsubj.id}_"
            
        writer.writerow([ teacher.name, teacher.teacher_uid, teacher.usname, teacher.idontknow, teacher.teacher_image, teacher.teachprofile_id, teacher.teacher_image, teacher.gender, teach_sub, teach_class, teacher.date_of_birth, teacher.mobile_number, teacher.email, teacher.email]) 
        # 
  
    return response 



@login_required
def images_generate_csv(request): 
    response = HttpResponse(content_type='text/csv') 
    formatted_datetime = datetime.datetime.now()
    file_name = f"images_{formatted_datetime}.csv"
    response['Content-Disposition'] = f'attachment; filename={file_name}'

    response.write(u'\ufeff'.encode('utf8'))
  
    writer = csv.writer(response) 
    writer.writerow(["title", "cloudflare_id",  "added_by" ]) 
    # 

    images = Image.objects.all() 
    for img in images: 
        # print("img_")
        # print(img)
            
        writer.writerow([ img.title, img.cloudflare_id, img.added_by]) 
        # 
  
    return response 

@login_required
def users_generate_csv(request): 
    response = HttpResponse(content_type='text/csv') 
    formatted_datetime = datetime.datetime.now()
    file_name = f"users_{formatted_datetime}.csv"
    response['Content-Disposition'] = f'attachment; filename={file_name}'

    response.write(u'\ufeff'.encode('utf8'))
  
    writer = csv.writer(response) 
    writer.writerow(["password", "last_login",  "is_superuser", "fast_name", "last_name", "is_staff", "is_active", "username", "email", "phone", "phone_code", "is_authorized", "login_token", "name", "related_to", "date_joined", "is_actif", "has_sub", "company", "freespace", "is_student", "is_admin", "is_teacher", "is_top_management", "student_profile_id", "teacher_profile_id", "photo" ]) 
    # 

    users = CustomUser.objects.all() 
    for user in users: 
        # print("user_")
        # print(user)
            
        writer.writerow([ user.password, user.last_login, user.is_superuser, user.first_name, user.last_name, user.is_staff, user.is_actif, user.username, user.email, user.phone, user.phone_code, user.is_authorized, user.login_token, user.name, user.related_to, user.date_joined, user.is_actif, user.has_sub, user.company, user.freespace, user.is_student, user.is_admin, user.is_teacher, user.is_top_management, user.student_profile,user.teacher_profile,user.photo]) 
        # 
        # 
  
    return response 

