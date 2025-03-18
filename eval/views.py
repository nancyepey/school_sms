from django.shortcuts import render
#
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect

from school.models import ClassRoom

from .models import Eval
from student.models import Student
from subject.models import Subject
from django.contrib import messages
#login required
from django.contrib.auth.decorators import login_required



# Create your views here.

# def eval_list(request):
#     eval_list = Eval.objects.select_related('student').all()
#     context = {
#         'eval_list': eval_list,
#     }
#     return render(request, "eval/evals.html", context)


@login_required
def eval_list(request):
    eval_list = Eval.objects.select_related('student').all()
    classroom = ClassRoom.objects.all()
    context = {
        'eval_list': eval_list,
        'classroom':classroom,
    }
    if request.method == 'POST':
        # print(request)
        class_selected = request.POST.get('student_class')
        get_class = ClassRoom.objects.get(id = class_selected)
        eval_list = Eval.objects.filter( student__student_class=get_class )
        context = {
            'eval_list': eval_list,
            'classroom':classroom,
            'class_selected': get_class.class_name,
            'codeclass_selected': get_class.class_code,
        }
    return render(request, "eval/evals.html", context)


@login_required
def add_test(request):
    subject = Subject.objects.all()
    student = Student.objects.all()
    context = {
        'subject':subject,
        'student':student,
    }

    if request.method == "POST":
        title = request.POST.get('title')
        titre = request.POST.get('titre')
        student = request.POST.get('student')
        value = request.POST.get('value')
        coef = request.POST.get('coef')
        subject = request.POST.get('subject')
        teacher = "teacher"
        remarks = request.POST.get('remarks')
        added_by = "emnanlaptop"

        #get student class
        print('student')
        obj_student_class = Subject.objects.get(id=student)

        #get subject class
        print('subject')
        obj_subject_class = Subject.objects.get(id=subject)

        test = Eval.objects.create(
            title = title,
            titre = titre,
            value = value,
            coef = coef,
            subject = obj_subject_class,
            observation = remarks,
            student = obj_student_class,
            teacher = teacher,
            added_by = added_by,
        )

        messages.success(request, 'Eval added Successfully')
        return redirect("test_list")
    

    return render(request, "eval/add-eval.html", context=context)