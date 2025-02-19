import datetime
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect

from core.models import CustomUser
from school.models import ClassRoom, Specialty
#
from .models import Parent, Student
from django.contrib import messages

# Create your views here.

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
        date_of_birth = request.POST.get('date_of_birth')
        student_class = request.POST.get('student_class')
        specialty_class = request.POST.get('specialty_class')
        religion = request.POST.get('religion')
        joining_date = request.POST.get('joining_date')
        mobile_number = request.POST.get('mobile_number')
        admission_number = request.POST.get('admission_number')
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
            if father_name == "" or mother_name == "":
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

        
        if student_email == "":
            if father_email == "":
                stu_email = mother_email
            if carer_email == "":
                stu_email = carer_email
        else:
            stu_email = student_email
        
        # save student information

        #get student class
        print(student_class)
        obj_student_class = ClassRoom.objects.get(id=student_class)
        # specialty_class
        obj_specialty_class = Specialty.objects.get(id=specialty_class)

        student = Student.objects.create(
            name = name,
            student_uid = student_uid,
            gender = gender,
            date_of_birth = date_of_birth,
            student_class = obj_student_class,
            specialty = obj_specialty_class,
            religion = religion,
            joining_date = joining_date,
            mobile_number = mobile_number,
            admission_number = admission_number,
            section = section,
            student_image = student_image,
            parent = parent, 
            added_by = request.user.username,
        )

        #
        

        # Create the user
        user = CustomUser.objects.create_user(
            username=username,
            email=stu_email,
            name=name,
            password="GTECH",
            photo = student_image,
            student_profile = student
        )
        
        # Assign student role
        user.is_student = True

        user.save()

        messages.success(request, 'Student added Successfully')
        return redirect("student_list")
        # return render(request, "student_list")
    

    return render(request, "students/add-student.html", context=context)



def student_list(request):
    student_list = Student.objects.select_related('parent').all()
    classroom = ClassRoom.objects.all()
    context = {
        'student_list': student_list,
        'classroom':classroom,
    }
    # print(context)
    if request.method == 'POST':
        # print(request)
        class_selected = request.POST.get('student_class')
        get_class = ClassRoom.objects.get(id = class_selected)
        student_list = Student.objects.filter(student_class=get_class)
        context = {
            'student_list': student_list,
            'classroom':classroom,
            'class_selected': get_class.class_name,
            'codeclass_selected': get_class.class_code,
        }

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
        date_of_birth = request.POST.get('date_of_birth')
        student_class = request.POST.get('student_class')
        specialty_class = request.POST.get('specialty_class')
        religion = request.POST.get('religion')
        joining_date = request.POST.get('joining_date')
        mobile_number = request.POST.get('mobile_number')
        admission_number = request.POST.get('admission_number')
        section = request.POST.get('section')
        student_image = request.FILES.get('student_image')  if request.FILES.get('student_image') else student.student_image

        # Retrieve parent data from the form
        parent_info = request.POST.get('parents')

        print(parent_info)

        if parent_info:
            #get parent
            parent = Parent.objects.get(id=parent_info)
        else:
            #edit parent
            if parent_info == "":
                parent.father_name = request.POST.get('father_name')
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
        student.name= name
        student.student_uid= student_uid
        student.gender= gender
        student.date_of_birth= date_of_birth

        student_class_obj = ClassRoom.objects.get(id=student_class)
        # specialty_class
        specialty_class_obj = Specialty.objects.get(id=specialty_class)

        student.parent = parent

        student.student_class= student_class_obj
        student.specialty= specialty_class_obj


        student.religion= religion
        student.joining_date= joining_date
        student.mobile_number = mobile_number
        student.admission_number = admission_number
        student.section = section
        student.student_image = student_image
        student.modified_by = request.user.username
        student.save()
        # create_notification(request.user, f"Added Student:  {student.name}")

        messages.success(request, f'{name}  Updated Successfully')
        
        return redirect("student_list")
    return render(request, "students/edit-student.html",{'student':student, 'parent':parent, 'parents':parents, 'classroom':classroom, "specialties":specialties} )


def view_student(request, slug):
    student = get_object_or_404(Student, id = slug)
    context = {
        'student': student,
    }
    return render(request, "students/student-details.html", context)


def delete_student(request, slug):
    if request.method == "POST":
        #
        student = get_object_or_404(Student, id = slug)
        name = student.name
        student.delete()

        messages.error(request, f'{name} Deleted Successfully')

        return redirect('student_list')
    return HttpResponseForbidden()
