
import datetime
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect

from core.models import CustomUser
from subject.models import Subject
from school.models import ClassRoom
#
from .models import Teacher
from django.contrib import messages

# Create your views here.

def add_teacher(request):
    subject = Subject.objects.all()
    classroom = ClassRoom.objects.all()
    context = {
        'subject':subject,
        'classroom': classroom
    }
    print(classroom)
    print(subject)
    # context = {}

    if request.method == "POST":
        name = request.POST.get('teacher_name')
        username = request.POST.get('u_name')
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
        
        
        # save teacher information

        #get teacher class
        print(teacher_subj)
        obj_teacher_subj = Subject.objects.get(id=teacher_subj)
        obj_classteach = ClassRoom.objects.get(id=classteach)

        teacher = Teacher.objects.create(
            name = name,
            teacher_uid = teacher_uid,
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
            password="GTECH",
            photo = teacher_image,
            teacher_profile = teacher
        )
        
        # Assign student role
        user.is_teacher = True

        user.save()

        messages.success(request, 'Teacher added Successfully')
        return redirect("teacher_list")
        # return render(request, "teacher_list")
    

    return render(request, "teachers/add-teacher.html", context=context)



def teacher_list(request):
    teacher_list = Teacher.objects.all()
    context = {
        'teacher_list': teacher_list,
    }
    return render(request, "teachers/teachers.html", context)


def edit_teacher(request,slug):
    teacher = get_object_or_404(Teacher, id=slug)
    subject = Subject.objects.all()
    classroom = ClassRoom.objects.all()
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
        teacher_image = request.FILES.get('teacher_image')  if request.FILES.get('teacher_image') else teacher.teacher_image

        # 

        # teacher.first_name= first_name
        teacher.name= name
        teacher.teacher_uid= teacher_uid
        teacher.gender= gender
        teacher.date_of_birth= date_of_birth

        teacher_subj_obj = Subject.objects.get(id=teacher_subj)

        teacher.teacher_subj= teacher_subj_obj

        teacher.joining_date= joining_date
        teacher.mobile_number = mobile_number
        teacher.section = section
        teacher.teacher_image = teacher_image
        modified_by = request.user.username
        teacher.save()
        # create_notification(request.user, f"Added Teacher:  {teacher.name}")
        
        return redirect("teacher_list")
    return render(request, "teachers/edit-teacher.html",{'teacher':teacher,  'subject':subject, 'classroom': classroom} )


def view_teacher(request, slug):
    teacher = get_object_or_404(Teacher, id = slug)
    context = {
        'teacher': teacher
    }
    return render(request, "teachers/teacher-details.html", context)


def delete_teacher(request, slug):
    if request.method == "POST":
        #
        teacher = get_object_or_404(Teacher, id = slug)
        teacher.delete()

        return redirect('teacher_list')
    return HttpResponseForbidden()
