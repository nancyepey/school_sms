from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from school.models import ClassRoom, Specialty
from subject.models import Subject

# Create your views here.

def subject_list(request):
    subject_list = Subject.objects.prefetch_related('classroom').all()
    context = {
        'subject_list': subject_list,
    }
    return render(request, "subjects/subjects.html", context)



def add_subject(request):
    classroom = ClassRoom.objects.all()
    specialty = Specialty.objects.all()
    
    context = {
        'classroom':classroom,
        'specialty':specialty
    }

    if request.method == "POST":
        title = request.POST.get('subject_title')
        fr_title = request.POST.get('subject_title_fren')
        coef = request.POST.get('coeff')
        subject_code = request.POST.get('subject_code')
        classroom = request.POST.get('subject_class[]')
        specialty = request.POST.get('specialty[]')
        description = request.POST.get('description')
        category = request.POST.get('category')
        # added_by = "emnanlaptop"

        # 

        #get student class
        # print(classroom)
        # obj_student_class = ClassRoom.objects.filter(classroom)

        subject = Subject.objects.create(
            title = title,
            fr_title = fr_title,
            coef = coef,
            subject_code = subject_code,
            description = description,
            category = category,
            added_by = request.user.username,
        )

        # count = 0
        # for e in classroom:
        #     obj_class = ClassRoom.objects.get(id=e)
        #     # subject.classroom.add(obj_class)
        #     subject.classroom.m2m.add(obj_class)
        #     count += 1

        obj_class = ClassRoom.objects.get(id=classroom)

        subject.classroom.add(obj_class)
        subject.save()

        messages.success(request, 'Subject added Successfully')
        return redirect("subject_list")
    
    return render(request, "subjects/add-subject.html", context)

def edit_subject(request, slug):
    subject = get_object_or_404(Subject, id=slug)
    classroom = ClassRoom.objects.all()
    specialty = Specialty.objects.all()
    mysubject_class = subject.classroom.all()
    subj_specialty_class = subject.specialty.all()
    # print(mysubject_class)
    # print(mysubject_class.classroom_id)
    # for team in mysubject_class:
    #     print(team)
    #     print(team.id)
    # print(subj_specialty_class)
    context = {
        'classroom':classroom,
        'subject':subject,
        'mysubject_class':mysubject_class,
        'specialty':specialty,
        'subj_specialty_class':subj_specialty_class,
    }

    if request.method == "POST":
        title           = request.POST.get('subject_title')
        # title = request.POST.get('subject_title')
        fr_title        = request.POST.get('subject_title_fren')
        coef            = request.POST.get('coeff')
        subject_code    = request.POST.get('subject_code')
        classroom       = request.POST.get('subject_class[]')
        
        description     = request.POST.get('description')
        category = request.POST.get('category')
        specialty = request.POST.get('specialty[]')
        modified_by     = request.user.username

        # 
        # obj_student_class = ClassRoom.objects.filter(classroom)

        
        subject.title = title
        subject.fr_title = fr_title
        subject.coef = coef
        subject.subject_code = subject_code
        subject.description = description
        subject.modified_by = modified_by
        subject.category = category

        # print("classroom")
        # print(classroom)

        count_class = 0
        for classr in classroom:
            # print(classr)
            obj_class = ClassRoom.objects.get(id=classr)
            subject.classroom.add(obj_class)
            count_class += 1
        # print(count_class)

        count_specialty = 0
        for specialt in specialty:
            # print(specialt)
            specialty_obj_class = Specialty.objects.get(id=specialt)
            subject.specialty.add(specialty_obj_class)
            count_specialty += 1
        # print(count_specialty)
        

        # obj_class = ClassRoom.objects.get(id=classroom)

        # subject.classroom.add(obj_class)

        # print("specialty")
        # print(specialty)

        # specialty_obj_class = Specialty.objects.get(id=specialty)
        # print(specialty_obj_class)

        # subject.specialty.add(specialty_obj_class)
        subject.save()

        messages.success(request, 'Subject updated Successfully')
        return redirect("subject_list")
    
    return render(request, "subjects/edit-subject.html", context)



def view_subject(request, slug):
    subject = get_object_or_404(Subject, id = slug)
    context = {
        'subject': subject
    }
    return render(request, "subjects/subject-details.html", context)


def delete_subject(request, slug):
    if request.method == "POST":
        #
        subject = get_object_or_404(Subject, id = slug)
        subject.delete()

        return redirect('subject_list')
    return HttpResponseForbidden()

