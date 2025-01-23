import datetime
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect

from school.models import ClassRoom
#
from .models import Parent, Student
from django.contrib import messages

# Create your views here.

def add_student(request):
    classroom = ClassRoom.objects.all()
    context = {'classroom':classroom}

    if request.method == "POST":
        name = request.POST.get('student_name')
        student_uid = request.POST.get('student_uid')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        student_class = request.POST.get('student_class')
        religion = request.POST.get('religion')
        joining_date = request.POST.get('joining_date')
        mobile_number = request.POST.get('mobile_number')
        admission_number = request.POST.get('admission_number')
        section = request.POST.get('section')
        student_image = request.FILES.get('student_image')
        # added_by = request.POST.get('created_by')

        # retrieve parent data from the form
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

        #save parent info
        if father_name == "" or mother_name == "":
            parent = Parent.objects.create(
                carer_name = carer_name,
                carer_occupation = carer_occupation,
                carer_mobile = carer_mobile,
                carer_email = carer_email,
                present_address = present_address,
                permanent_address = permanent_address,
                added_by = "emnanlaptop",

            )
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
                added_by = "emnanlaptop",
            )
        
        # save student information

        #get student class
        print(student_class)
        obj_student_class = ClassRoom.objects.get(id=student_class)

        student = Student.objects.create(
            name = name,
            student_uid = student_uid,
            gender = gender,
            date_of_birth = date_of_birth,
            student_class = obj_student_class,
            religion = religion,
            joining_date = joining_date,
            mobile_number = mobile_number,
            admission_number = admission_number,
            section = section,
            student_image = student_image,
            parent = parent, 
            added_by = "emnanlaptop",
        )

        messages.success(request, 'Student added Successfully')
        return redirect("student_list")
        # return render(request, "student_list")
    

    return render(request, "students/add-student.html", context=context)



def student_list(request):
    student_list = Student.objects.select_related('parent').all()
    context = {
        'student_list': student_list,
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
#         student.modified_by = "emnanlaptop"
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
#         parent.modified_by = "emnanlaptop"

#         parent.save() #save parent
        

        
#         # return render(request, 'student_list')
#         return redirect('student_list')
    
#     return render(request, "students/edit-student.html", context)



def edit_student(request,slug):
    student = get_object_or_404(Student, id=slug)
    parent = student.parent if hasattr(student, 'parent') else None
    classroom = ClassRoom.objects.all()
    if request.method == "POST":
        # first_name = request.POST.get('first_name')
        name = request.POST.get('name')
        student_uid = request.POST.get('student_uid')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        student_class = request.POST.get('student_class')
        religion = request.POST.get('religion')
        joining_date = request.POST.get('joining_date')
        mobile_number = request.POST.get('mobile_number')
        admission_number = request.POST.get('admission_number')
        section = request.POST.get('section')
        student_image = request.FILES.get('student_image')  if request.FILES.get('student_image') else student.student_image

        # Retrieve parent data from the form
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

        student.student_class= student_class_obj


        student.religion= religion
        student.joining_date= joining_date
        student.mobile_number = mobile_number
        student.admission_number = admission_number
        student.section = section
        student.student_image = student_image
        student.modified_by = "emnanlaptop"
        student.save()
        # create_notification(request.user, f"Added Student:  {student.name}")
        
        return redirect("student_list")
    return render(request, "students/edit-student.html",{'student':student, 'parent':parent, 'classroom':classroom} )


def view_student(request, slug):
    student = get_object_or_404(Student, id = slug)
    context = {
        'student': student
    }
    return render(request, "students/student-details.html", context)


def delete_student(request, slug):
    if request.method == "POST":
        #
        student = get_object_or_404(Student, id = slug)
        student.delete()

        return redirect('student_list')
    return HttpResponseForbidden()
