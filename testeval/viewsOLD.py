
import csv
import html
from django.conf import settings
from django.shortcuts import render
#
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
# from sympy import Sum
from django.db.models import Sum
import decimal
from department.models import Department
from teacher.models import Teacher
from school.models import ClassRoom, Settings, Specialty

from .models import ClassRanking, Eval, ReportCard, TestMoySpecialtySubjClass
from student.models import Student
from subject.models import Subject
from django.contrib import messages
#pdf
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.utils.timezone import now
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import datetime
import os , subprocess, platform

from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate
# from reportlab.platypus.tables import Tables, TableStyle, colors
#
from xhtml2pdf import pisa
from django.template.loader import get_template
#
import pdfkit
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Sum
#
#ranking
from django.db.models.expressions import Window
from django.db.models.functions import Rank
from django.db.models import Sum, F
#image cloudflare

from images import services as image_services

#login required
from django.contrib.auth.decorators import login_required



# Create your views here.

@login_required
def eval_list(request):
    eval_list = Eval.objects.select_related('student').all()
    classroom = ClassRoom.objects.all()
    specialtys = Specialty.objects.all()
    context = {
        'eval_list': eval_list,
        'classroom':classroom,
        'specialtys':specialtys,
    }
    if request.method == 'POST':
        # print(request)
        class_selected = request.POST.get('student_class')
        print(class_selected)
        # if class_selected == "all":
        #     context = {
        #         'eval_list': eval_list,
        #         'classroom':classroom,
        #         'codeclass_selected': "all",
        #     }
        # else:
        #     get_class = ClassRoom.objects.get(id = class_selected)
        #     eval_list = Eval.objects.filter( student__student_class=get_class )
        #     context = {
        #         'eval_list': eval_list,
        #         'classroom':classroom,
        #         'class_selected': get_class.class_name,
        #         'codeclass_selected': get_class.class_code,
        #     }
        specialty_selected = request.POST.get('specialty_eval')
        specialty_selected = request.POST.get('stud_specialty')
        if class_selected == "all" and specialty_selected == "all":
            # print("dff")
            context = {
                'eval_list': eval_list,
                'classroom':classroom,
                'specialtys':specialtys,
                'codeclass_selected': "all",
                'specialty_selected': "all",
            }
        if class_selected != "all" and specialty_selected == "all":
            get_class = ClassRoom.objects.get(id = class_selected)
            eval_list = Eval.objects.filter( student__student_class=get_class )
            context = {
                'eval_list': eval_list,
                'classroom':classroom,
                'specialtys':specialtys,
                'class_selected': get_class.class_name,
                'codeclass_selected': get_class.class_code,
                'specialty_selected': "all",
            }
        if class_selected == "all" and specialty_selected != "all":
            get_specialty = Specialty.objects.get(id = specialty_selected)
            eval_list = Eval.objects.filter( student__specialty=get_specialty )
            context = {
                'eval_list': eval_list,
                'classroom':classroom,
                'specialtys':specialtys,
                'specialty_selected': get_specialty.name,
                'codeclass_selected': "all",
            }
        if class_selected != "all" and specialty_selected != "all":
            get_class = ClassRoom.objects.get(id = class_selected)
            get_specialty = Specialty.objects.get(id = specialty_selected)
            eval_list = Eval.objects.filter( student__student_class=get_class, student__specialty=get_specialty )
            context = {
                'eval_list': eval_list,
                'classroom':classroom,
                'specialtys':specialtys,
                'class_selected': get_class.class_name,
                'codeclass_selected': get_class.class_code,
                'specialty_selected': get_specialty.name,
            }
        return render(request, "eval/evals.html", context)
    
    
    return render(request, "eval/evals.html", context)


def report_card_list(request):
    report_card = ReportCard.objects.select_related('student').all()
    
    classroom = ClassRoom.objects.all()
    specialtys = Specialty.objects.all()
    context = {
        'report_card_list': report_card,
        'classroom':classroom,
        'specialtys':specialtys,
    }
    if request.method == 'POST':
        # print(request)
        class_selected = request.POST.get('student_class')
        specialty_selected = request.POST.get('stud_specialty')
        get_class = ClassRoom.objects.get(id = class_selected)
        report_card_list = ReportCard.objects.filter( student__student_class=get_class )
        get_specialty = Specialty.objects.get(id = specialty_selected)
        context = {
            'report_card_list': report_card_list,
            'classroom':classroom,
            'specialtys':specialtys,
            'class_selected': get_class.class_name,
            'specialty_selected': get_specialty.name ,
            'codeclass_selected': get_class.class_code,
        }
    return render(request, "reports/report_card.html", context)



# @login_required
def add_test(request):
    subject = Subject.objects.all()
    student = Student.objects.all()
    teacher = Teacher.objects.all()
    context = {
        'subject':subject,
        'student':student,
        'teacher':teacher,
    }

    if request.method == "POST":
        # title = request.POST.get('title')
        # titre = request.POST.get('titre')
        # student = request.POST.get('student')
        # value = request.POST.get('value')
        # coef = request.POST.get('coeff')
        # subject = request.POST.get('subject')
        # # teacher = "teacher"
        # teacher = request.POST.get('teacher')
        # remarks = request.POST.get('remarks')
        # added_by = request.user.username
        term = request.POST.get('term')
        if term == "First":
            title = "Test1"
            titre =  "Eval1"
            title1 = "Test2"
            titre1 =  "Eval2"
        if term == "Second":
            title = "Test3"
            titre =  "Eval3"
            title1 = "Test4"
            titre1 =  "Eval4"
        if term == "Third":
            title = "Test5"
            titre =  "Eval5"
            title1 = "Test6"
            titre1 =  "Eval6"
        student = request.POST.get('student')
        value = request.POST.get('value')
        value_two = request.POST.get('value_two')
        coef = request.POST.get('coeff')
        subject = request.POST.get('subject')
        # teacher = "teacher"
        teacher = request.POST.get('teacher')
        remarks = request.POST.get('remarks')
        added_by = request.user.username


        #get student class
        # print('student')
        obj_student_class = Student.objects.get(id=student)

        #get teacher class
        # print('teacher')
        print(teacher)
        obj_teacher_class = Teacher.objects.get(id=teacher)
        # print(obj_teacher_class)

        #get subject class
        # print('subject')
        obj_subject_class = Subject.objects.get(id=subject)


        # check if test exist
        check_tests = Eval.objects.filter(student=obj_student_class, subject=obj_subject_class, academic_year="2024/2025").first()
        if check_tests:
            messages.error(request, f'{obj_student_class.name}-- {obj_subject_class.title} --- Already exist')
            return redirect("test_list")
        else:
            print(value_two)
            if float(value_two) > 0:
                value1 = value_two
                #test
                test = Eval.objects.create(
                    title = title,
                    titre = titre,
                    value = value,
                    sec_title = title1,
                    sec_titre = titre1,
                    sec_value = value1,
                    coef = coef,
                    subject = obj_subject_class,
                    observation = remarks,
                    student = obj_student_class,
                    teacher = obj_teacher_class,
                    teacher_class = obj_teacher_class,
                    added_by = added_by,
                )
            else:
                test = Eval.objects.create(
                    title = title,
                    titre = titre,
                    value = value,
                    coef = coef,
                    subject = obj_subject_class,
                    observation = remarks,
                    student = obj_student_class,
                    teacher = obj_teacher_class,
                    teacher_class = obj_teacher_class,
                    added_by = added_by,
                )

        messages.success(request, f'{obj_student_class.name}-- {obj_subject_class.title} --- Marks added Successfully')
        return redirect("test_list")
    

    return render(request, "eval/add-eval.html", context=context)



# @login_required
def edit_test(request, slug):
    eval = get_object_or_404(Eval, id=slug)
    # student = get_object_or_404(Student, id=slug)
    student = Student.objects.all()
    subject = Subject.objects.all()
    teacher = Teacher.objects.all()
    # parent = student.parent if hasattr(student, 'parent') else None
    context = {'eval':eval, 'student':student, 'subject':subject, 'teacher':teacher,}
    if request.method == "POST":
        # first_name = request.POST.get('first_name')
        title = request.POST.get('title')
        titre = request.POST.get('titre')
        student = request.POST.get('student')
        value = request.POST.get('value')
        coef = request.POST.get('coeff')
        subject = request.POST.get('subject')
        teacher = request.POST.get('teacher')
        remarks = request.POST.get('remarks')

        #get student class
        # print('student')
        obj_student_class = Student.objects.get(id=student)

        #get subject class
        # print('subject')
        obj_subject_class = Subject.objects.get(id=subject)

        #get teacher class
        print('teacher')
        print(teacher)
        obj_teacher_class = Teacher.objects.get(id=teacher)
        print(obj_teacher_class)

        
        eval.title = title
        eval.titre = titre
        eval.value = value
        eval.coef = coef
        eval.subject = obj_subject_class
        eval.observation = remarks
        eval.student = obj_student_class
        eval.teacher = obj_teacher_class.name
        eval.teacher_class = obj_teacher_class
        eval.modified_by = request.user.username
        eval.save()
        
        
        return redirect("test_list")
    return render(request, "eval/edit-eval.html", context )





# @login_required
def delete_test(request, slug):
    if request.method == "POST":
        #
        eval = get_object_or_404(Eval, id = slug)
        eval.delete()

        return redirect('test_list')
    return HttpResponseForbidden()



#report card
# @login_required
def see_marks(request, student_id):
    queryset = Eval.objects.filter(student_id=student_id)
    total_marks = queryset.aggregate(total_marks=Sum('value'))
    current_rank = -1
    ranks = Student.objects.annotate(marks=Sum('eval__value')).order_by('-value', '-student_date_of_birth')

    i = 1
    for rank in ranks:
        if student_id == rank.student_id.student_id:
            current_rank = i
            break
        i = i + 1
        return {'queryset': queryset, 'total_marks': total_marks, 'current_rank': current_rank}
        # return render(request, 'see_marks.html/', {'queryset': queryset, 'total_marks': total_marks, 'current_rank': current_rank})


# def get_marks(request):
#     student = Student.objects.all()

#appreciation
def appreciation_marks(marks):
    if marks >= 0 and marks < 5:
        return "WEAK"
    if marks >= 5 and marks < 8:
        return "POOR"
    if marks >= 8 and marks < 10:
        return "BELOW AVERAGE"
    if marks == 10:
        return "FAIRLY GOOD"
    if marks > 10 and marks < 12:
        return "AVERAGE"
    if marks >= 12 and marks < 15:
        return "GOOD"
    if marks >= 15 and marks < 17:
        return "VERY GOOD"
    if marks >= 17 and marks < 20:
        return "EXCELLENT"


# @login_required
def cal_mark_class(request):
    classrooms = ClassRoom.objects.all()
    subjects = Subject.objects.all()
    context = {
        'classrooms':classrooms,
    }

    get_testa = decimal.Decimal(0.0)
    get_testb = decimal.Decimal(0.0)
    get_test = decimal.Decimal(0.0)
    observation = ""

    if request.method == "POST":
        #
        try:
            #geting all required data
            classroom = request.POST.get('classroom')
            term = request.POST.get('term')
            added_by = request.user.username
            # print(added_by)
            # print()

            get_class = ClassRoom.objects.get(id = classroom)

            #get all students from the classroom
            students = Student.objects.filter(student_class=get_class)
            # print(students)

            #get all calculate marks
            get_cal_marks = TestMoySpecialtySubjClass.objects.all()
            # print("in")

            pass
        except:
            # print("out")
            messages.error(request, 'Something went wrong')
            return redirect('calculate_mark_class')
        
        if students:
            # print("in in")
            # print(Student.objects.filter(student_class=get_class).count())
            if Student.objects.filter(student_class=get_class).count() > 1:
            #loop through the students and get their marks
            # obj_eval_class = Eval.objects.filter(student_id=studentId)
            # print(students)
                for student in students:
                    # print(student)
                    for subject in subjects:
                        if term == "first":
                            # print(student_test.title)
                            get_testa_subj = Eval.objects.filter(student_id=student.id,subject_id = subject.id)
                            if get_testa_subj:
                                # print(get_testa_subj)
                                total = get_testa_subj.aggregate(s=Sum("value"))["s"]
                                # print(total)
                                if total  >= 0:
                                    # print(subject)
                                    # print('{:0.2f}'.format((total/ 2)* get_testa_subj[0].coef))
                                    get_test = '{:0.2f}'.format((total/ 2)* get_testa_subj[0].coef)
                                    observation = appreciation_marks((total/ 2))
                                    # print(observation)
                                    current_cal_marks = get_cal_marks.filter(term=term, classroom =student.student_class, specialty=student.specialty, student=student, subject=subject, is_actif=True)
                                    if current_cal_marks:
                                        for current_mark in current_cal_marks:
                                            # print(current_mark)
                                            # print(current_mark.is_actif)  
                                            current_mark.is_actif = False
                                            current_mark.modified_by = request.user.username
                                            current_mark.save()
                                    
                                    mark_subj = TestMoySpecialtySubjClass.objects.create(
                                        term = term,
                                        classroom = student.student_class,
                                        specialty = student.specialty,
                                        student = student,
                                        subject = subject,
                                        test_avg = get_test,
                                        subj_coef = get_testa_subj[0].coef,
                                        observation = observation,
                                        added_by = added_by,
                                    )
                        if term == "second":
                            # print(student_test.title)
                            get_testa_subj = Eval.objects.filter(student_id=student.id,subject_id = subject.id)
                            if get_testa_subj:
                                print(get_testa_subj)
                                total = get_testa_subj.aggregate(s=Sum("value"))["s"]
                                # print(total)
                                if total  >= 0:
                                    # print(subject)
                                    # print('{:0.2f}'.format((total/ 2)* get_testa_subj[0].coef))
                                    get_test = '{:0.2f}'.format((total/ 2)* get_testa_subj[0].coef)
                                    observation = appreciation_marks((total/ 2))
                                    # print(observation)
                                    current_cal_marks = get_cal_marks.filter(term=term, classroom =student.student_class, specialty=student.specialty, student=student, subject=subject, is_actif=True)
                                    if current_cal_marks:
                                        for current_mark in current_cal_marks:
                                            # print(current_mark)
                                            # print(current_mark.is_actif)  
                                            current_mark.is_actif = False
                                            current_mark.modified_by = request.user.username
                                            current_mark.save()
                                    
                                    mark_subj = TestMoySpecialtySubjClass.objects.create(
                                        term = term,
                                        classroom = student.student_class,
                                        specialty = student.specialty,
                                        student = student,
                                        subject = subject,
                                        test_avg = get_test,
                                        subj_coef = get_testa_subj[0].coef,
                                        observation = observation,
                                        added_by = added_by,
                                    )
                        if term == "third":
                            # print(student_test.title)
                            get_testa_subj = Eval.objects.filter(student_id=student.id,subject_id = subject.id)
                            if get_testa_subj:
                                # print(get_testa_subj)
                                total = get_testa_subj.aggregate(s=Sum("value"))["s"]
                                # print(total)
                                if total  >= 0:
                                    # print(subject)
                                    # print('{:0.2f}'.format((total/ 2)* get_testa_subj[0].coef))
                                    get_test = '{:0.2f}'.format((total/ 2)* get_testa_subj[0].coef)
                                    observation = appreciation_marks((total/ 2))
                                    # print(observation)
                                    current_cal_marks = get_cal_marks.filter(term=term, classroom =student.student_class, specialty=student.specialty, student=student, subject=subject, is_actif=True)
                                    if current_cal_marks:
                                        for current_mark in current_cal_marks:
                                            # print(current_mark)
                                            # print(current_mark.is_actif)  
                                            current_mark.is_actif = False
                                            current_mark.modified_by = request.user.username
                                            current_mark.save()
                                    
                                    mark_subj = TestMoySpecialtySubjClass.objects.create(
                                        term = term,
                                        classroom = student.student_class,
                                        specialty = student.specialty,
                                        student = student,
                                        subject = subject,
                                        test_avg = get_test,
                                        subj_coef = get_testa_subj[0].coef,
                                        observation = observation,
                                        added_by = added_by,
                                    )
                    # #get evaluations of the student based on the term
                    # obj_tests_class = Eval.objects.filter(student_id=student.id)
                    # #looping through the tests of a student
                    # for student_test in obj_tests_class:
                    #     # print(student_test)
                    #     if term == "first":
                    #         print(student_test.title)
                    #     if term == "second":
                    #         print(student_test.title)
                    #     if term == "third":
                    #         print(student_test.title)
            else:
                # obj_tests_class = Eval.objects.filter(student_id=students[0].id)
                #looping through the tests of a student
                for subject in subjects:
                    if term == "first":
                        # print(student_test.title)
                        get_testa_subj = Eval.objects.filter(student_id=students[0].id,subject_id = subject.id)
                        if get_testa_subj:
                            # print(get_testa_subj)
                            total = get_testa_subj.aggregate(s=Sum("value"))["s"]
                            # print(total)
                            if total >= 0:
                                # print(subject)
                                # print('{:0.2f}'.format((total/ 2)* get_testa_subj[0].coef))
                                get_test = '{:0.2f}'.format((total/ 2)* get_testa_subj[0].coef)
                                observation = appreciation_marks((total/ 2))
                                # print(observation)
                                current_cal_marks = get_cal_marks.filter(term=term, classroom =students[0].student_class, specialty=students[0].specialty, student=students[0], subject=subject, is_actif=True)
                                if current_cal_marks:
                                    for current_mark in current_cal_marks:
                                        # print(current_mark)
                                        # print(current_mark.is_actif)  
                                        current_mark.is_actif = False
                                        current_mark.modified_by = request.user.username
                                        current_mark.save()
                                
                                mark_subj = TestMoySpecialtySubjClass.objects.create(
                                    term = term,
                                    classroom = students[0].student_class,
                                    specialty = students[0].specialty,
                                    student = students[0],
                                    subject = subject,
                                    test_avg = get_test,
                                    subj_coef = get_testa_subj[0].coef,
                                    observation = observation,
                                    added_by = added_by,
                                )
                    if term == "second":
                        # print(student_test.title)
                        # print(count)
                        # print(subject)
                        get_testa_subj = Eval.objects.filter(student_id=students[0].id,subject_id = subject.id)
                        if get_testa_subj:
                            # print(get_testa_subj)
                            total = get_testa_subj.aggregate(s=Sum("value"))["s"]
                            # print(total)
                            if total >= 0:
                                # print(subject)
                                # print('{:0.2f}'.format((total/ 2)* get_testa_subj[0].coef))
                                get_test = '{:0.2f}'.format((total/ 2)* get_testa_subj[0].coef)
                                observation = appreciation_marks((total/ 2))
                                # print(observation)
                                current_cal_marks = get_cal_marks.filter(term=term, classroom =students[0].student_class, specialty=students[0].specialty, student=students[0], subject=subject, is_actif=True)
                                if current_cal_marks:
                                    for current_mark in current_cal_marks:
                                        print(current_mark)
                                        print(current_mark.is_actif)  
                                        current_mark.is_actif = False
                                        current_mark.modified_by = request.user.username
                                        current_mark.save()
                                
                                mark_subj = TestMoySpecialtySubjClass.objects.create(
                                    term = term,
                                    classroom = students[0].student_class,
                                    specialty = students[0].specialty,
                                    student = students[0],
                                    subject = subject,
                                    test_avg = get_test,
                                    subj_coef = get_testa_subj[0].coef,
                                    observation = observation,
                                    added_by = added_by,
                                )
                    if term == "third":
                        # print(student_test.title)
                        # print(count)
                        # print(subject)
                        get_testa_subj = Eval.objects.filter(student_id=students[0].id,subject_id = subject.id)
                        if get_testa_subj:
                            # print(get_testa_subj)
                            total = get_testa_subj.aggregate(s=Sum("value"))["s"]
                            # print(total)
                            if total >= 0:
                                print(subject)
                                # print('{:0.2f}'.format((total/ 2)* get_testa_subj[0].coef))
                                get_test = '{:0.2f}'.format((total/ 2)* get_testa_subj[0].coef)
                                observation = appreciation_marks((total/ 2))
                                # print(observation)
                                current_cal_marks = get_cal_marks.filter(term=term, classroom =students[0].student_class, specialty=students[0].specialty, student=students[0], subject=subject, is_actif=True)
                                if current_cal_marks:
                                    for current_mark in current_cal_marks:
                                        # print(current_mark)
                                        # print(current_mark.is_actif)  
                                        current_mark.is_actif = False
                                        current_mark.modified_by = request.user.username
                                        current_mark.save()
                                
                                mark_subj = TestMoySpecialtySubjClass.objects.create(
                                    term = term,
                                    classroom = students[0].student_class,
                                    specialty = students[0].specialty,
                                    student = students[0],
                                    subject = subject,
                                    test_avg = get_test,
                                    subj_coef = get_testa_subj[0].coef,
                                    observation = observation,
                                    added_by = added_by,
                                )
                        # print('{:0.2f}'.format((total/ 2)* get_testa_subj[0].coef))
                        
                        # if student_test.subject_id == subject.id:
                        #     print(f"{student_test.title}------{student_test.value}-----{subject}")
                        #     # print(count)
                        #     count = count + 1
                        #     print(subject)
                        #     get_testa_subj = Eval.objects.filter(student_id=students[0].id,subject_id = subject.id)
                        #     total = get_testa_subj.aggregate(s=Sum("value"))["s"]
                        #     print('{:0.2f}'.format((total/ 2)* student_test.coef))
                # count = 0
                # for student_test in obj_tests_class:
                    ##NEW
                    # count = 0
                    # array_for_vals = []
                    # for subject in subjects:
                    #     if student_test.subject_id == subject.id:
                    #         count = count + 1
                    #         print(student_test.subject_id)
                    #         # if student_test.title == "Test3":
                    #         #     print(student_test.title)
                            # array_for_vals.append([student_test.subject_id, subject.title, student_test.value, students[0].name])
                            # array_for_vals.append(f"{student_test.subject_id}_{subject.title}_{student_test.value}_{students[0].name}")
                    # print(array_for_vals)
                    # print(array_for_vals[0][1])
                    # for array_for_val in array_for_vals:
                    #     # print(array_for_val)
                    #     for subject in subjects:
                    #         if array_for_vals[0][0] == subject.id:
                    #             print(subject)
                    ##OLD
                    # if term == "first":
                    #     print(student_test.title)
                    # if term == "second":
                    #     # print(student_test.title)
                    #     count = 0
                    #     get_testa_stud = ""
                    #     get_testb_stud = ""
                    #     for subject in subjects:
                    #         # print(count)
                            
                    #         if student_test.subject_id == subject.id:
                    #             print(f"{student_test.title}------{student_test.value}-----{subject}")
                    #             # print(count)
                    #             count = count + 1
                    #             print(subject)
                    #             get_testa_subj = Eval.objects.filter(student_id=students[0].id,subject_id = subject.id)
                    #             total = get_testa_subj.aggregate(s=Sum("value"))["s"]
                    #             print('{:0.2f}'.format((total/ 2)* student_test.coef))
                                # if student_test.title == "Test3":
                                #     count = count + 1
                                #     # print(count)
                                #     get_testa = student_test.value
                                # if student_test.title == "Test4":
                                #     count = count + 1
                                #     # print(count)
                                #     get_testb = student_test.value
                                # print(count)
                                # if count == 2 and (get_testb > 0.0 and get_testa > 0.0):
                                #     get_test = ((get_testa + get_testb) / 2) * student_test.coef
                                #     print(f"{get_test}------{students[0]}")
                            # get_testa_subj = Eval.objects.filter(student_id=students[0].id,subject_id = subject.id, title = "Test3")
                            # print(get_testa_subj)
                            # if get_testa_subj:
                            #     print(get_testa_subj)
                            #     get_testa = get_testa_subj.value
                            # if student_test.title == "Test3":
                            #     get_testa = student_test.value
                            #     get_testa_stud = student_test.student_id
                            #     print(student_test.student_id)
                            # if student_test.title == "Test4":
                            #     get_testb = student_test.value
                            #     get_testb_stud = student_test.student_id
                            # if get_testa_stud == get_testb_stud:
                            #     print("same student")
                            #     get_test = ((get_testa + get_testb) / 2) * student_test.coef
                            #     print(get_test)
                            # print(subject)
                            # print(student_test.subject_id)
                            # print(subject.id)
                            # if student_test.title == "Test3":
                            #     get_testa = student_test.value
                            #     if student_test.subject_id == subject.id:
                            #         print("Test3")
                            #         print(get_testa)
                            #         get_test = ((get_testa + get_testb) / 2) * student_test.coef
                            #         print(get_test)
                            #         print(subject)
                            # if student_test.title == "Test4":
                            #     get_testb = student_test.value
                            #     # print("Test4")
                            #     # print(get_testb)
                            #     if student_test.subject_id == subject.id:
                            #         print("Test4")
                            #         print(get_testb)
                            #         get_test = ((get_testa + get_testb) / 2) * student_test.coef
                            #         print(get_test)
                            #         print(subject)
                            #     # print(get_test)
                            #     # print(students[0])
                            #     # print(students[0].student_class)
                            #     # print(students[0].specialty)
                            #     observation = appreciation_marks(get_testa)
                                #
                                ####
                                # if get_testb > 0.0 and get_testa > 0.0:
                                #     get_test = ((get_testa + get_testb) / 2) * student_test.coef
                                #     # print("info")
                                #     print(subject)
                                #     # print(get_test)
                                #     # print(students[0])
                                #     # print(students[0].student_class)
                                #     # print(students[0].specialty)
                                #     observation = appreciation_marks(get_testa)
                                    # print(observation)

                                    # current_cal_marks = get_cal_marks.filter(term="second", classroom =students[0].student_class, specialty=students[0].specialty, student=students[0], subject=subject, is_actif=True)
                                    # if current_cal_marks:
                                    #     for current_mark in current_cal_marks:
                                    #         print(current_mark)
                                    #         print(current_mark.is_actif)  
                                    #         current_mark.is_actif = False
                                    #         current_mark.modified_by = request.user.username
                                    #         current_mark.save()
                                    
                                    # mark_subj = TestMoySpecialtySubjClass.objects.create(
                                    #     term = term,
                                    #     classroom = students[0].student_class,
                                    #     specialty = students[0].specialty,
                                    #     student = students[0],
                                    #     subject = subject,
                                    #     test_avg = get_test,
                                    #     observation = observation,
                                    #     added_by = added_by,
                                    # )
                        # print(count)

                        # messages.success(request, 'Subject Marks added Successfully')
                        # return redirect("calculate_mark_class")

                                
                    # if term == "third":
                    #     print(student_test.title)

                    # print(student_test)
                            
                        
        else:
            messages.error(request, 'No Student')
            return redirect('calculate_mark_class')
        
    

    return render(request, "eval/call-results-class.html", context=context)


# def ranking(self, *args, **kwargs): 
#     marks = ClassRanking.objects.all().values_list('specialty', flat=True).order_by('-total_avg') 
#     rank = list(marks).index(self) 
#     return rank

# @login_required
def delete_report_card(request, slug):
    if request.method == "POST":
        #
        report_card = get_object_or_404(ReportCard, id = slug)
        student_name =  report_card.student.name
        report_card.delete()

        messages.success(request, f'{student_name} Record card Deleted')

        return redirect('report_cards')
    return HttpResponseForbidden()


# @login_required
def cal_classranking(request):
    #base on the id of TestMoySpecialtySubjClass 
    # students have specialty
    classrooms = ClassRoom.objects.all()
    subjects = Subject.objects.all()
    specialties = Specialty.objects.all()
    totalmarks_subject = TestMoySpecialtySubjClass.objects.all()
    students = Student.objects.all()
    #get all class ranking
    get_class_rankxs = ClassRanking.objects.all()

    
    

    # for classroom in classrooms:
    #     #get students
    #     for student in students:
    #         if student.student_class.id == classroom.id:
    #             print(classroom.class_name)
    #             print(student.specialty.name)
    #             #subjects marks
    #             for subject_marks in totalmarks_subject:
    #                 if subject_marks.is_actif == True:
    #                     # print(subject_marks.term)
    #                     #loop through subjects
    #                     for subject in subjects:
    #                         if subject_marks.subject_id == subject.id:
    #                             print(subject.title)

    # count = 0
        
    if students:
        print("in in")
        # loop thro students
        for student in students:
            get_coef = 0.0
            for classroom in classrooms:
                # print(classroom)

                #loop through subjects
                # for subject in subjects:
                    # print(f"{student.name}--{subject.title}--{subject_marks.specialty}--{subject_marks.test_avg}--{subject.coef}")
                    #
                # get_coef = subject.coef
                # print(f"{student.name}--")
                get_testa_subj = TestMoySpecialtySubjClass.objects.filter(classroom_id=classroom.id,student_id=student.id,is_actif = True)
                # print(f"{get_testa_subj}--{get_testa_subj}")
                # for get_tt in get_testa_subj:
                #     print(f"{get_tt.subject.title}--{get_tt.subj_coef}")
                if get_testa_subj:
                    # print(get_testa_subj)
                    #total marks
                    total_test = get_testa_subj.aggregate(s=Sum("test_avg"))["s"]
                    # print(total_test)
                    #total coef
                    total_coef = get_testa_subj.aggregate(s=Sum("subj_coef"))["s"]
                    # print(total_coef)
                    # print(get_testa_subj[0].specialty.name)
                    # print(get_testa_subj[0].term)
                    # print(get_testa_subj[0].classroom.class_name)
                    total_moy = '{:0.2f}'.format(total_test / total_coef) 
                    # print(total_moy)
                    print(student.name)
                    current_class_rankxs = get_class_rankxs.filter(term=get_testa_subj[0].term, classroom =student.student_class, specialty=get_testa_subj[0].specialty, student=student, is_actif=True)
                    if current_class_rankxs:
                        for class_rankx in current_class_rankxs:
                            print(class_rankx)
                            print(class_rankx.is_actif)  
                            class_rankx.is_actif = False
                            class_rankx.modified_by = request.user.username
                            class_rankx.save()
                    
                    class_ranking = ClassRanking.objects.create(
                        term = get_testa_subj[0].term,
                        classroom = student.student_class,
                        specialty = get_testa_subj[0].specialty,
                        total_coeff = total_coef,
                        total_marks = total_test,
                        total_avg = total_moy,
                        student = student,
                        added_by = request.user.username,
                    )
            


    # for subject_marks in totalmarks_subject:
    #     if subject_marks.is_actif == True:
    #         # print(subject_marks.term)
    #         #array of student and coef
    #         arr_stud_coef = []
    #         # loop thro students
    #         for student in students:
    #             get_coef = 0.0
    #             if student.id == subject_marks.student_id:

    #                 #loop through subjects
    #                 for subject in subjects:
    #                     if subject_marks.subject_id == subject.id:
    #                         print(f"{student.name}--{subject.title}--{subject_marks.specialty}--{subject_marks.test_avg}--{subject.coef}")
    #                         #
    #                         get_coef = subject.coef
                    # print(get_coef)
    
    #NB
    # Of course you can do it in one SQL query. Generating this query using django ORM is also easily achievable.
    # top_scores = (myModel.objects
    #                     .order_by('-score')
    #                     .values_list('score', flat=True)
    #                     .distinct())
    # top_records = (myModel.objects
    #                     .order_by('-score')
    #                     .filter(score__in=top_scores[:10]))



    #- before column name mean "descending order", while without - mean "ascending".
    #order be decending order
    get_class_rankings = ClassRanking.objects.filter(is_actif=True).order_by('-total_avg')
    # ranking(get_class_rankings)
    # rankings = ClassRanking.objects.filter(is_actif=True).annotate(
    #         rank=Window(
    #             expression=Rank(),
    #             order_by=F('total_avg').desc()
    #         ),
    #     )
    # print(rankings)
    # rank = 1
    # previous = None
    # entries = list(get_class_rankings)
    # previous = entries[0]
    # previous.rank = 1
    # for i, entry in enumerate(entries[1:]):
    #     if entry.total_avg != previous.total_avg:
    #         rank = i + 2
    #         entry.rank = str(rank)
    #     else:
    #         entry.rank = "%s=" % rank
    #         previous.rank = entry.rank
    #     previous = entry
    #     print(rank)
    
                    
    context = {
        'classrooms':classrooms,
        'class_rankings':get_class_rankings,
    }
    return render(request, "eval/call-classranks.html", context=context)


# @login_required
def create_report_card(request):
    # eval = Eval.objects.all()
    student = Student.objects.all()
    context = {
        'student':student,
    }

    if request.method == "POST":
        student = request.POST.get('student')
        term = request.POST.get('term')
        academic_yr = request.POST.get('academic_year')
        resumptn = request.POST.get('resumptn_date')
        added_by = request.user.username

        #get student class
        # print('student')
        obj_student_class = Student.objects.get(id=student)

        classroomId = obj_student_class.student_class_id
        classroom =  ClassRoom.objects.get(id=classroomId)

        #get test
        # print('test')
        obj_eval_class = Eval.objects.filter(student_id=student, academic_year=academic_yr)
        # print(obj_eval_class)

        #get subject
        # print('subject')
        # list_subject = Subject.classroom.all()
        # print(list_subject)
        # obj_eval_class = Eval.objects.filter(student_id=student)
        results = Subject.objects.filter(classroom=classroomId)
        # print(results)
        results_subjs = Subject.objects.filter(classroom=classroomId)

        #total coef
        # total_coeff = 0.00
        total_coeff = decimal.Decimal(0.0)
        #
        total_gen_coeff = decimal.Decimal(0.0)
        total_prof_coeff = decimal.Decimal(0.0)

        #total tot
        # total_tot = 0.00
        total_tot = decimal.Decimal(0.0)
        #
        total_gen_tot = decimal.Decimal(0.0)

        # Create an empty of subjects and marks
        subj_cat = []

        #array of all values and coef

        # Create an empty of gen et prof
        subject_gen_tot = decimal.Decimal(0.0)
        subject_prof_tot = decimal.Decimal(0.0)

        total_prof_tot = decimal.Decimal(0.0)

        try:

            if obj_eval_class is None:
                print("not results")
                messages.error("No Test Results In Record")
                return redirect('report_cards')
            else:
                for evals_record in obj_eval_class :
                    # print(evals_record)
                    for subject in results_subjs:
                        # print(subject)
                        if subject.id == evals_record.subject_id:
                            # print(f'{subject}___{evals_record}___{evals_record.subject_id}')
                            # obj_eval_first = Eval.objects.filter(student_id=student, academic_year=academic_yr).first()
                            # print(obj_eval_first)
                            # print(f'{subject}___{evals_record.coef}')
                            # print(f'{subject}___{obj_eval_first.coef}')
                            # evals_record.first()
                            # print(evals_record.first())
                            # tests_subj = obj_eval_class.filter(subject_id=subject.id)
                            # print(tests_subj)
                            # for test_subj in tests_subj:
                            #     if term == "second":
                            #         print(term)

                            testa_value = 0.0
                            testb_value = 0.0
                            testb_coef = 0.0
                            testa_coef = 0.0
                            if(term == 'second'):
                                obj_eval_first = Eval.objects.filter(title='Test3',student_id=student, academic_year=academic_yr).first()
                                print(obj_eval_first)
                                # print(f'{subject}___{evals_record.coef}')
                                testa = obj_eval_class.filter(title='Test3',subject_id=subject.id)
                                # testb = obj_eval_class.filter(title='Test4',subject_id=subject.id)

                                # testa = evals_record.filter(title='Test3')
                                # print(testa)
                                # print(f'{subject}___{testa}___{testa}')

                                # print(f'{subject}___{evals_record}___{evals_record.subject_id}')
                                # print(f'{subject}___{evals_record}___{evals_record.value}___{evals_record.subject_id}')
                                # print(evals_record.title)

                                if evals_record.title == 'Test3':
                                    print(f'{subject}___{evals_record}___{evals_record.value}___{evals_record.subject_id}')
                                    testa_value =  decimal.Decimal(testa_value) + evals_record.value
                                    testa_coef = decimal.Decimal(testa_coef) + evals_record.coef

                                if evals_record.title == 'Test4':
                                    print(f'{subject}___{evals_record}___{evals_record.value}___{evals_record.subject_id}')
                                    testb_value =  decimal.Decimal(testb_value) + evals_record.value
                                    testb_coef = decimal.Decimal(testb_coef) +  evals_record.coef
                                
                                if(subject.category == 'General'):
                                    # print(f"General {subject.coef} {subject.title}")
                                    total_gen_coeff = total_gen_coeff + decimal.Decimal(testb_coef)
                                    subj_cat.append(subject.category)
                                    # total_gen_tot = total_gen_tot + decimal.Decimal(testb_coef)
                                #)
                                if(subject.category == 'Professional'):
                                    # print(f"Professional {testb_coef}")
                                    total_prof_coeff = total_prof_coeff + decimal.Decimal(testb_coef)
                                    subj_cat.append(subject.category)
                                
                            total_eval = decimal.Decimal(testa_value) + decimal.Decimal(testb_value)
                            # moyentt = total_eval / 2
                            # print(moyentt)
                            print(total_eval)


                                # print(testa)
                                # print(testb)
                                # if testa:
                                #     for test1 in testa:
                                #         if(test1.subject_id == subject.id):
                                #             testa_value = test1.value
                                #             testa_coef = test1.coef
                                #             # print(subject.title)
                                #             print(f'{testa}_______{testa_value}_____{testa_coef}')
                                # print(student)

                                # if testb:
                                #     for test2 in testb:
                                #         if(test2.subject_id == subject.id):
                                #             testb_value = test2.value
                                #             testb_coef = test2.coef
                                #             # print(subject.title)
                                # if(subject.category == 'General'):
                                #     print(f"General {subject.coef} {subject.title}")
                                #     total_gen_coeff = total_gen_coeff + decimal.Decimal(testb_coef)
                                #     subj_cat.append(subject.category)
                                #     # total_gen_tot = total_gen_tot + decimal.Decimal(testb_coef)
                                # #)
                                # if(subject.category == 'Professional'):
                                #     # print(f"Professional {testb_coef}")
                                #     total_prof_coeff = total_prof_coeff + decimal.Decimal(testb_coef)
                                #     subj_cat.append(subject.category)
                                
                                # total_eval = testa_value + testb_value
                                # moyentt = total_eval / 2
                                # # print(moyentt)

                                # subj_moy = f"{subject.id}_{moyentt}_{subject.title}"
                                # total_coeff = total_coeff + decimal.Decimal(evals_record.subject.coef)
                                # # total
                                # moy_tot = moyentt  * int(evals_record.subject.coef)
                                # total_tot = total_tot + decimal.Decimal(moy_tot)
                                # subj_moy_tot = f"{subject.title}_{subject.id}_{moyentt}_{moy_tot}"
                                # # print(subj_moy_tot)
                                # # print(testb)
                                # if(subject.category == 'General'):
                                #     total_gen_tot = total_gen_tot + total_tot
                                #     #
                                # if(subject.category == 'Professional'):
                                #     total_prof_tot = total_prof_tot + moy_tot
                #total
            # print(total_coeff)
            # print(total_tot)
            # print("general")
            # print(total_gen_coeff)
            # print(f"General tot: {total_gen_tot}")
            # print("prof")
            # print(total_prof_coeff)
        

            # report_card = ReportCard.objects.create(
            #     student = obj_student_class ,
            #     term = term,
            #     student_rank = 1,
            #     general_subjs_avr = total_gen_tot,
            #     prof_subjs_avr = total_tot - total_gen_tot,
            #     total_avr = total_tot,
            #     best_avr = total_tot,
            #     worst_avr = total_tot,
            #     firstterm_avr = total_tot,
            #     secondterm_avr = total_tot,
            #     # academic_year = '2023/2024',
            #     academic_year = academic_yr,
            #     resumption = resumptn,
            #     # teacher = teacher,
            #     added_by = added_by,
            # )

            # messages.success(request, 'Eval added Successfully')
            # return redirect("test_list")

        except Exception as e:
            #error occurs
            messages.error("Erreur-- ")
            # messages.error(request, f"Erreur-- {e}")
            return redirect('add_report_cards')

        # if results is None:
        #     print("not results")
        #     print(results)
        # else:
        #     for subjj_cl in results:
        #         print(subjj_cl.id)
        #         print(subjj_cl.coef)
        #         if subjj_cl.coef is None:
        #             print('no subjj coef')
        #         else:
        #             if(subjj_cl.category == 'General'):
        #                 print(f"General {subjj_cl.coef}")
        #                 total_gen_coeff = total_gen_coeff + decimal.Decimal(subjj_cl.coef)
        #                 # total_gen_tot = total_gen_tot + decimal.Decimal(subjj_cl.coef)
        #             #)
        #             if(subjj_cl.category == 'Professional'):
        #                 print(f"Professional {subjj_cl.coef}")
        #                 total_prof_coeff = total_prof_coeff + decimal.Decimal(subjj_cl.coef)
        #             #
        #             if(term == 'first'):
        #                 testa = obj_eval_class.filter(title='Test1',subject_id=subjj_cl.id)
        #                 testb = obj_eval_class.filter(title='Test2',subject_id=subjj_cl.id)
        #                 # print('first')
        #                 if not testa:
        #                     print("no vale a")
        #                     testa_value = 0.0
        #                 else:
        #                     for test1 in testa:
        #                         if(test1.subject_id == subjj_cl.id):
        #                             testa_value = test1.value
        #                 if not testb:
        #                     print("no vale b")
        #                     testb_value = 0.0
        #                 else:
        #                     for test2 in testb:
        #                         if(test2.subject_id == subjj_cl.id):
        #                             testb_value = test2.value
        #                 total_eval = testa_value + testb_value
        #                 moyentt = total_eval / 2
        #                 # print(moyentt)

        #                 subj_moy = f"{subjj_cl.id}_{moyentt}_{subjj_cl.title}"
        #                 total_coeff = total_coeff + decimal.Decimal(subjj_cl.coef)
        #                 # total
        #                 moy_tot = moyentt  * int(subjj_cl.coef)
        #                 total_tot = total_tot + decimal.Decimal(moy_tot)
        #                 subj_moy_tot = f"{subjj_cl.title}_{subjj_cl.id}_{moyentt}_{moy_tot}"
        #                 print(subj_moy_tot)
        #                 # print(testb)
        #                 if(subjj_cl.category == 'General'):
        #                     total_gen_tot = total_gen_tot + total_tot

        #             if(term == 'second'):
        #                 testa = obj_eval_class.filter(title='Test3').filter(subject_id=subjj_cl.id)
        #                 testb = obj_eval_class.filter(title='Test4',subject_id=subjj_cl.id)
        #                 # print('test3')
        #                 # print(testa.filter(subject_id=subjj_cl.id))
        #                 if not testa:
        #                     print("no vale a")
        #                     testa_value = 0.0
        #                 else:
        #                     for test1 in testa:
        #                         # print(test.value)
        #                         if(test1.subject_id == subjj_cl.id):
        #                             # print("yes")
        #                             # print('test3')
        #                             # print(test1.value)
        #                             testa_value = test1.value
        #                 if not testb:
        #                     print("no vale b")
        #                     testb_value = 0.0
        #                 else:
        #                     for test2 in testb:
        #                         if(test2.subject_id == subjj_cl.id):
        #                             # print("yes")
        #                             # print('test4')
        #                             # print(test2.value)
        #                             testb_value = test2.value
        #                 # print(testa.values().value)
        #                 # print('type')
        #                 # print(type(testa_value))
        #                 # print(type(testb_value))
        #                 total_eval = decimal.Decimal(testa_value) + decimal.Decimal(testb_value) 
        #                 moyentt = total_eval / 2
        #                 # print(moyentt)

        #                 subj_moy = f"{subjj_cl.id}_{moyentt}_{subjj_cl.title}"
        #                 print(subj_moy)

        #                 # print("coef")
        #                 # print(subjj_cl.coef)
        #                 # print("type(subjj_cl.id)")
        #                 # print(type(subjj_cl.coef))
        #                 # print(subjj_cl.title)
        #                 # print(type(total_coeff))
        #                 total_coeff = total_coeff + decimal.Decimal(subjj_cl.coef)
        #                 # total
        #                 moy_tot = moyentt  * int(subjj_cl.coef)
        #                 # print(type(moy_tot))
        #                 # print(type(total_tot))
        #                 # print(total_tot)
        #                 total_tot = total_tot + decimal.Decimal(moy_tot)
        #                 subj_moy_tot = f"{subjj_cl.title}_{subjj_cl.id}_{moyentt}_{moy_tot}"
        #                 print(subj_moy_tot)

        #                 # print('test4')
        #                 # print(testb)
        #                 if(subjj_cl.category == 'General'):
        #                     total_gen_tot = total_gen_tot + total_tot

        #             if(term == 'third'):
        #                 testa = obj_eval_class.filter(title='Test5')
        #                 testb = obj_eval_class.filter(title='Test6')
        #                 # print('first')
        #                 if not testa:
        #                     print("no vale a")
        #                     testa_value = 0.0
        #                 else:
        #                     for test1 in testa:
        #                         if(test1.subject_id == subjj_cl.id):
        #                             testa_value = test1.value
        #                 if not testb:
        #                     print("no vale b")
        #                     testb_value = 0.0
        #                 else:
        #                     for test2 in testb:
        #                         if(test2.subject_id == subjj_cl.id):
        #                             testb_value = test2.value
        #                 total_eval = testa_value + testb_value
        #                 moyentt = total_eval / 2
        #                 # print(moyentt)

        #                 subj_moy = f"{subjj_cl.id}_{moyentt}_{subjj_cl.title}"
        #                 total_coeff = total_coeff + decimal.Decimal(subjj_cl.coef)
        #                 # total
        #                 moy_tot = moyentt  * int(subjj_cl.coef)
        #                 total_tot = total_tot + decimal.Decimal(moy_tot)
        #                 subj_moy_tot = f"{subjj_cl.title}_{subjj_cl.id}_{moyentt}_{moy_tot}"
        #                 print(subj_moy_tot)
        #                 # print(testb)
        #                 if(subjj_cl.category == 'General'):
        #                     total_gen_tot = total_gen_tot + total_tot
        #     #

        #     #total
        #     print(total_coeff)
        #     print(total_tot)
        #     print("general")
        #     print(total_gen_coeff)
        #     print(f"General tot: {total_gen_tot}")
        #     print("prof")
        #     print(total_prof_coeff)
        

        #     report_card = ReportCard.objects.create(
        #         student = obj_student_class ,
        #         term = term,
        #         student_rank = 1,
        #         general_subjs_avr = total_gen_tot,
        #         prof_subjs_avr = total_tot - total_gen_tot,
        #         total_avr = total_tot,
        #         best_avr = total_tot,
        #         worst_avr = total_tot,
        #         firstterm_avr = total_tot,
        #         secondterm_avr = total_tot,
        #         # academic_year = '2023/2024',
        #         academic_year = academic_yr,
        #         resumption = resumptn,
        #         # teacher = teacher,
        #         added_by = added_by,
        #     )

        # messages.success(request, 'Eval added Successfully')
        # return redirect("test_list")
    

    return render(request, "reports/add-card.html", context=context)



# @login_required
def addReportCard(request):
    student = Student.objects.all()
    context = {
        'student':student,
    }
    #add reportcard
    
    
    if request.method == "POST":
        student = request.POST.get('student')
        term = request.POST.get('term')
        academic_yr = request.POST.get('academic_year')
        resumptn = request.POST.get('resumptn_date')
        added_by = request.user.username

        #total coef
        # total_coeff = 0.00
        total_coeff = decimal.Decimal(0.0)
        #
        total_gen_coeff = decimal.Decimal(0.0)
        total_prof_coeff = decimal.Decimal(0.0)

        #total tot
        # total_tot = 0.00
        total_tot = decimal.Decimal(0.0)
        #
        total_gen_tot = decimal.Decimal(0.0)
        total_prof_tot = decimal.Decimal(0.0)


        #get subjects
        term = term

        # Create an empty of subjects and marks
        subject_value_cat = []

        # Create an empty of subjects and marks
        subj_cat = []

        # Create an empty of gen et prof
        subject_gen_tot = 0.0
        subject_prof_tot = 0.0

        subjt_rang = "1"
        #get student class
        try:
            #Get Client Settings
            p_settings = Settings.objects.get(clientName='GILEAD TECHNICAL HIGH SCHOOL')
            # print('student')
            if student == "all":
                obj_student_class = Student.objects.all()
            else:
                #get student class
                obj_student_class = Student.objects.get(id=student)
                # count_obj_student_class = Student.objects.get(id=student).count()
                print(obj_student_class)
                # print(count_obj_student_class)

                classroomId = obj_student_class.student_class_id
                classroom =  ClassRoom.objects.get(id=classroomId)
            
                print('student')
            # obj_student_class = Student.objects.get(id=student)
            # print(obj_student_class.specialty)

            # classroomId = obj_student_class.student_class_id
            # classroom =  ClassRoom.objects.get(id=classroomId)
                subjects = Subject.objects.filter(classroom=classroomId)
                print(subjects)
                obj_eval_class = Eval.objects.filter(student_id=student, academic_year=academic_yr)
                obj_eval_cl_type = Eval.objects.filter(student_id=student, academic_year=academic_yr)
            # print(obj_eval_class)
            # pass
        except:
            messages.error(request, 'Something went wrong')
            return redirect('report_cards')
        
        


        #Calculate the Avg Total
        if obj_student_class:
            print("stud exits")
            if subjects.count() > 0 :
                #
                print("subjects")
                print(subjects)
                for subject in subjects:
                    print(subject)
                    if subject.coef is None:
                        # print('no subjj coef')
                        messages.error(request, 'No Coef found')
                        return redirect('report_cards')
                    else:
                        if obj_eval_cl_type:
                            print("obj_eval_cl_type:")
                            for evals in obj_eval_cl_type:
                                if evals.subject_id == subject.id:
                                    if(term == 'first'):
                                        print("term")
                                        print(term)
                                        # testa = obj_eval_class.filter(title='Test1',subject_id=subject.id, student=student)
                                        # testb = obj_eval_class.filter(title='Test2',subject_id=subject.id, student=student)
                                        testa = obj_eval_class.filter(title='Test1',subject_id=subject.id)
                                        testb = obj_eval_class.filter(title='Test2',subject_id=subject.id)
                                        # print('first')
                                        print("testa")
                                        print(testa)
                                        if testa:
                                            print(testa)
                                        print("testb")
                                        print(testb)
                                        if testb:
                                            print(testb)
                                        if not testa:
                                            # print("no vale a")
                                            testa_value = 0.0
                                        else:
                                            # testa_value = testa.value
                                            for test1 in testa:
                                                if(test1.subject_id == subject.id):
                                                    testa_value = test1.value
                                                    #
                                        if not testb:
                                            # print("no vale b")
                                            testb_value = 0.0
                                        else:
                                            # testb_value = testb.value
                                            for test2 in testb:
                                                if(test2.subject_id == subject.id):
                                                    testb_value = test2.value
                                        total_eval = testa_value + testb_value
                                        moyentt = total_eval / 2
                                        # print(moyentt)

                                        subj_moy = f"{subject.id}_{moyentt}_{subject.title}"
                                        total_coeff = total_coeff + decimal.Decimal(evals.subject.coef)
                                        # total
                                        moy_tot = moyentt  * int(evals.subject.coef)
                                        total_tot = total_tot + decimal.Decimal(moy_tot)
                                        subj_moy_tot = f"{subject.title}_{subject.id}_{moyentt}_{moy_tot}"
                                        # print(subj_moy_tot)
                                        # print(testb)
                                        if(subject.category == 'General'):
                                            total_gen_tot = total_gen_tot + total_tot
                                            #
                                        if(subject.category == 'Professional'):
                                            total_prof_tot = total_prof_tot + moy_tot
                                            #
                                        # subject_value_cat.append([test1.subject.title,testa_value,testb_value, moyentt, moy_tot,evals.subject.coef, test2.observation, subject.category, test1.teacher])
                                        subject_value_cat.append([testa.subject.title,testa_value,testb_value, moyentt, moy_tot,evals.subject.coef, testb.observation, subject.category, testa.teacher])
                                    
                                        print(subject_value_cat)
            #                             #
                        else:
                            messages.error(request, 'No Tests Record')
                            return redirect('report_cards')
            #             # follow_object = Teacher.objects.filter(classrooms = classroom, t_subjects = subjects)
            #             # followers_of_teach = follow_object.t_subjects.all()
            #             # print(follow_object)
            #             # print("subject title")
            #             # print(subject.title)
            #             # print("subject term")
            #             # print(obj_report_card.term)
            #             for evals in obj_eval_cl_type:
            #                     if evals.subject_id == subject.id:
            #                         # if(subject.category == 'General'):
            #                         #     # print(f"General {subject.coef}")
            #                         #     total_gen_coeff = total_gen_coeff + decimal.Decimal(evals.subject.coef)
            #                         #     subj_cat.append(subject.category)
            #                         #     # total_gen_tot = total_gen_tot + decimal.Decimal(evals.subject.coef)
            #                         # #)
            #                         # if(subject.category == 'Professional'):
            #                         #     # print(f"Professional {evals.subject.coef}")
            #                         #     total_prof_coeff = total_prof_coeff + decimal.Decimal(evals.subject.coef)
            #                         #     subj_cat.append(subject.category)
            #                         #
            #                         if(term == 'first'):
            #                             print("term")
            #                             print(term)
            #                             subjt_rang = "1"
            #                             testa = obj_eval_class.filter(title='Test1',subject_id=subject.id)
            #                             testb = obj_eval_class.filter(title='Test2',subject_id=subject.id)
            #                             # print('first')
            #                             if not testa:
            #                                 # print("no vale a")
            #                                 testa_value = 0.0
            #                             else:
            #                                 for test1 in testa:
            #                                     if(test1.subject_id == subject.id):
            #                                         testa_value = test1.value
            #                                         #
            #                             if not testb:
            #                                 # print("no vale b")
            #                                 testb_value = 0.0
            #                             else:
            #                                 for test2 in testb:
            #                                     if(test2.subject_id == subject.id):
            #                                         testb_value = test2.value
            #                             total_eval = testa_value + testb_value
            #                             moyentt = total_eval / 2
            #                             # print(moyentt)

            #                             subj_moy = f"{subject.id}_{moyentt}_{subject.title}"
            #                             total_coeff = total_coeff + decimal.Decimal(evals.subject.coef)
            #                             # total
            #                             moy_tot = moyentt  * int(evals.subject.coef)
            #                             total_tot = total_tot + decimal.Decimal(moy_tot)
            #                             subj_moy_tot = f"{subject.title}_{subject.id}_{moyentt}_{moy_tot}"
            #                             # print(subj_moy_tot)
            #                             # print(testb)
            #                             if(subject.category == 'General'):
            #                                 total_gen_tot = total_gen_tot + total_tot
            #                                 #
            #                             if(subject.category == 'Professional'):
            #                                 total_prof_tot = total_prof_tot + moy_tot
            #                                 #
            #                             # subject_value_cat.append([test1.subject.title,testa_value,testb_value, moyentt, moy_tot,evals.subject.coef, test2.observation, subject.category, test1.teacher])
            #                             #
            #                         if(term == 'second'):
            #                             subjt_rang = "1"
            #                             testa = obj_eval_class.filter(title='Test3',subject_id=subject.id)
            #                             testb = obj_eval_class.filter(title='Test4',subject_id=subject.id)
            #                             print(term)
            #                             testa_value = 0.0
            #                             testb_value = 0.0
            #                             testb_coef = 0.0
            #                             testa_coef = 0.0

            #                             if testa:
            #                                 for test1 in testa:
            #                                     if(test1.subject_id == subject.id):
            #                                         testa_value = test1.value
            #                                         testa_coef = test1.coef

            #                             if testb:
            #                                 for test2 in testb:
            #                                     if(test2.subject_id == subject.id):
            #                                         testb_value = test2.value
            #                                         testb_coef = test2.coef
            #                             if(subject.category == 'General'):
            #                                 # print(f"General {subject.coef}")
            #                                 total_gen_coeff = total_gen_coeff + decimal.Decimal(testb_coef)
            #                                 subj_cat.append(subject.category)
            #                                 # total_gen_tot = total_gen_tot + decimal.Decimal(testb_coef)
            #                             #)
            #                             if(subject.category == 'Professional'):
            #                                 # print(f"Professional {testb_coef}")
            #                                 total_prof_coeff = total_prof_coeff + decimal.Decimal(testb_coef)
            #                                 subj_cat.append(subject.category)
            #                             # print(testa.teacher)
            #                             # print(testb)
            #                             # print('first')
            #                             # if not testa:
            #                             #     # print("no vale a")
            #                             #     testa_value = 0.0
            #                             # else:
            #                             #     for test1 in testa:
            #                             #         if(test1.subject_id == subject.id):
            #                             #             testa_value = test1.value
            #                             # if not testb:
            #                             #     # print("no vale b")
            #                             #     testb_value = 0.0
            #                             # else:
            #                             #     for test2 in testb:
            #                             #         if(test2.subject_id == subject.id):
            #                             #             testb_value = test2.value
            #                             total_eval = decimal.Decimal(testa_value) + decimal.Decimal(testb_value)
            #                             moyentt = total_eval / 2
            #                             # print(moyentt)

            #                             subj_moy = f"{subject.id}_{moyentt}_{subject.title}"
            #                             print(subj_moy)
            #                             total_coeff = total_coeff + decimal.Decimal(testb_coef)
            #                             # total
            #                             moy_tot = moyentt  * int(testb_coef)
            #                             total_tot = total_tot + decimal.Decimal(moy_tot)
            #                             subj_moy_tot = f"{subject.title}_{subject.id}_{moyentt}_{moy_tot}"
            #                             # print(subj_moy_tot)
            #                             # print(testb)
            #                             if(subject.category == 'General'):
            #                                 total_gen_tot = total_gen_tot + total_tot
            #                                 subject_gen_tot = subject_gen_tot + float(moy_tot)
            #                             if(subject.category == 'Professional'):
            #                                 # total_gen_tot = total_gen_tot + total_tot
            #                                 subject_prof_tot = subject_prof_tot + float(moy_tot)
            #                                 total_prof_tot = total_prof_tot + moy_tot
            #                                 #
            #                             # if(test1.subject.title == "English Langauge"):
            #                             #     print(subject.category)
            #                                 #
            #                             subject_value_cat.append([test1.subject.title,testa_value,testb_value, moyentt, testb_coef, moy_tot, test1.observation, subject.category, test1.teacher])
            #                             # subject_value_cat.append([test1.subject.title,testa_value,testb_value, moyentt, subject.coef, moy_tot, test2.observation, subject.category, test1.teacher])
            #                             #
            #                         if(term == 'third'):
            #                             subjt_rang = "1"
            #                             testa = obj_eval_class.filter(title='Test5',subject_id=subject.id)
            #                             testb = obj_eval_class.filter(title='Test6',subject_id=subject.id)
            #                             # print('first')
            #                             if not testa:
            #                                 # print("no vale a")
            #                                 testa_value = 0.0
            #                             else:
            #                                 for test1 in testa:
            #                                     if(test1.subject_id == subject.id):
            #                                         testa_value = test1.value
            #                             if not testb:
            #                                 # print("no vale b")
            #                                 testb_value = 0.0
            #                             else:
            #                                 for test2 in testb:
            #                                     if(test2.subject_id == subject.id):
            #                                         testb_value = test2.value
            #                             total_eval = testa_value + testb_value
            #                             moyentt = total_eval / 2
            #                             # print(moyentt)

            #                             subj_moy = f"{subject.id}_{moyentt}_{subject.title}"
            #                             total_coeff = total_coeff + decimal.Decimal(evals.subject.coef)
            #                             # total
            #                             moy_tot = moyentt  * int(evals.subject.coef)
            #                             total_tot = total_tot + decimal.Decimal(moy_tot)
            #                             subj_moy_tot = f"{subject.title}_{subject.id}_{moyentt}_{moy_tot}"
            #                             # print(subj_moy_tot)
            #                             # print(testb)
            #                             if(subject.category == 'General'):
            #                                 total_gen_tot = total_gen_tot + total_tot
            #                             if(subject.category == 'Professional'):
            #                                 total_prof_tot = total_prof_tot + moy_tot
            #                                 #
            #                             # subject_value_cat.append([test1.subject.title,testa_value,testb_value, moyentt, moy_tot, subject.coef, test2.observation, subject.category,  test1.teacher])
            #                             subject_value_cat.append([test1.subject.title,testa_value,testb_value, moyentt, moy_tot, evals.subject.coef, test2.observation, subject.category,  test1.teacher])

            #         # y = float(x.quantity) * float(x.price)
            #     # invoiceTotal += y
        
        
            # print("subject_gen_tot")
            # print(subject_gen_tot)
            # print("subject_prof_tot")
            # print(subject_prof_tot)
            # print("total_tot ")
            # print(total_tot )

            # if subject_gen_tot == 0:
            #     gen_sub_moy = 0
            
            # else:
            #     gen_sub_moy = subject_gen_tot / decimal.Decimal(total_gen_coeff)
            # if subject_prof_tot == 0:
            #     prof_sub_moy = 0
            # else:
            #     prof_sub_moy = subject_prof_tot / decimal.Decimal(total_prof_coeff)
            # if total_tot == 0:
            #     prof_gen_tot_moy = 0
            # else:
            #     prof_gen_tot_moy = total_tot / decimal.Decimal(total_coeff)
            
            
            # # gen_sub_moy = decimal.Decimal(subject_gen_tot ) / total_gen_coeff
            # # prof_sub_moy = decimal.Decimal(subject_prof_tot ) / total_prof_coeff
            # # prof_gen_tot_moy = decimal.Decimal(total_tot ) / total_coeff

            

            # # print(subject_value_cat)



            # context = {}
            # context['prof_sub_moy'] = round(prof_sub_moy, ndigits=2)
            # context['prof_gen_tot_moy'] = round(prof_gen_tot_moy, ndigits=2)
            # context['subject_line'] = subject_value_cat
            # context['p_settings'] = p_settings
            # context['student'] = obj_student_class
            # context['classroom'] = classroom
            # context['total_coeff'] = total_coeff
            # context['total_tot'] = total_tot
            # context['total_gen_coeff'] = total_gen_coeff
            # context['total_prof_coeff'] = total_prof_coeff
            # context['gen_tot'] = total_gen_tot
            # context['subject_gen_tot'] = subject_gen_tot #gen total subj
            # context['gen_sub_moy'] = round(gen_sub_moy, ndigits=2)
            # context['subj_cat'] = subj_cat
            # context['total_prof_tot'] = total_prof_tot
            # # context['avgTotal'] = "{:.2f}".format(invoiceTotal)

            # print(context)

            # # using now() to get current time
            # current_time = datetime.datetime.now()

            # report_card = ReportCard.objects.create(
            #     student           = obj_student_class ,
            #     term              = term,
            #     student_rank      = 1,
            #     gen_coeff         = total_gen_coeff,
            #     prof_coeff        = total_prof_coeff,
            #     gen_total         = subject_gen_tot,
            #     prof_total        = total_prof_tot,
            #     general_subjs_avr = round(gen_sub_moy, ndigits=2),
            #     prof_subjs_avr    = round(prof_sub_moy, ndigits=2),
            #     total_avr         = round(prof_gen_tot_moy, ndigits=2),
            #     best_avr          = round(prof_gen_tot_moy, ndigits=2),
            #     worst_avr         = round(prof_gen_tot_moy, ndigits=2),
            #     firstterm_avr     = round(prof_gen_tot_moy, ndigits=2),
            #     secondterm_avr    = round(prof_gen_tot_moy, ndigits=2),
            #     # academic_year = '2023/2024',
            #     academic_year     = academic_yr,
            #     resumption        = resumptn,
            #     # teacher = teacher,
            #     added_by          = added_by,
            # )

            # messages.success(request, f'{obj_student_class.name} Record Card added Successfully')
            # return redirect("report_cards")
        # messages.error(request, 'Something went wrong')
        # return redirect('report_cards')
    # student = Student.objects.all()
    # context = {
    #     'student':student,
    # }

    #Return
    return render(request, "reports/add-card.html", context=context)


# def generate_pdf(request):
#     response = FileResponse(generate_pdf_file(), 
#                             as_attachment=True, 
#                             filename='book_catalog.pdf')
#     return response
 
 
# def generate_pdf_file():
#     from io import BytesIO
 
#     buffer = BytesIO()
#     p = canvas.Canvas(buffer)
 
#     # Create a PDF document
#     reportCards = ReportCard.objects.all()
#     p.drawString(100, 750, "ReportCard Catalog")
 
#     y = 700
#     for reportCard in reportCards:
#         p.drawString(100, y, f"Title: {reportCard.student.name}")
#         p.drawString(100, y - 20, f"Author: {reportCard.student_rank}")
#         p.drawString(100, y - 40, f"Year: {reportCard.academic_year}")
#         p.rect(0.2*inch,0.2*inch,1*inch,1.5*inch, fill=1)

#         y -= 60

#         #
 
#     p.showPage()
#     p.save()
 
#     buffer.seek(0)
#     return buffer



# @login_required
def viewDocumentInvoice(request, slug):
    #fetch that reportcard
    try:
        #get student class
        print('student')
        obj_report_card = ReportCard.objects.get(id=slug)
        studentId = obj_report_card.student.id
        obj_student_class = Student.objects.get(id=studentId)
        # print(obj_student_class.specialty)

        classroomId = obj_student_class.student_class_id
        classroom =  ClassRoom.objects.get(id=classroomId)
        subjects = Subject.objects.filter(classroom=classroomId)
        # print(subjects)
        obj_eval_class = Eval.objects.filter(student_id=studentId)
        obj_eval_cl_type = Eval.objects.filter(student_id=studentId, title='Test3')
        # print(obj_eval_class)
        pass
    except:
        messages.error(request, 'Something went wrong')
        return redirect('report_cards')

    #total coef
    # total_coeff = 0.00
    total_coeff = decimal.Decimal(0.0)
    #
    total_gen_coeff = decimal.Decimal(0.0)
    total_prof_coeff = decimal.Decimal(0.0)

    #total tot
    # total_tot = 0.00
    total_tot = decimal.Decimal(0.0)
    #
    total_gen_tot = decimal.Decimal(0.0)
    total_prof_tot = decimal.Decimal(0.0)

    #Get Client Settings
    p_settings = Settings.objects.get(clientName='GILEAD TECHNICAL HIGH SCHOOL')

    #get subjects
    term = obj_report_card.term

    # Create an empty of subjects and marks
    subject_value_cat = []

    # Create an empty of subjects and marks
    subj_cat = []

    # Create an empty of gen et prof
    subject_gen_tot = 0.0
    subject_prof_tot = 0.0

    subjt_rang = "1"

    #Calculate the Avg Total
    if len(subjects) > 0:
        for subject in subjects:
            # print(subject.coef)
            if subject.coef is None:
                # print('no subjj coef')
                messages.error(request, 'Something went wrong')
                return redirect('report_cards')
            else:
                # follow_object = Teacher.objects.filter(classrooms = classroom, t_subjects = subjects)
                # followers_of_teach = follow_object.t_subjects.all()
                # print(follow_object)
                # print("subject title")
                # print(subject.title)
                # print("subject term")
                # print(obj_report_card.term)
                for evals in obj_eval_cl_type:
                        if evals.subject_id == subject.id:
                            # if(subject.category == 'General'):
                            #     # print(f"General {subject.coef}")
                            #     total_gen_coeff = total_gen_coeff + decimal.Decimal(evals.subject.coef)
                            #     subj_cat.append(subject.category)
                            #     # total_gen_tot = total_gen_tot + decimal.Decimal(evals.subject.coef)
                            # #)
                            # if(subject.category == 'Professional'):
                            #     # print(f"Professional {evals.subject.coef}")
                            #     total_prof_coeff = total_prof_coeff + decimal.Decimal(evals.subject.coef)
                            #     subj_cat.append(subject.category)
                            #
                            if(term == 'first'):
                                subjt_rang = "1"
                                testa = obj_eval_class.filter(title='Test1',subject_id=subject.id)
                                testb = obj_eval_class.filter(title='Test2',subject_id=subject.id)
                                # print('first')
                                if not testa:
                                    # print("no vale a")
                                    testa_value = 0.0
                                else:
                                    for test1 in testa:
                                        if(test1.subject_id == subject.id):
                                            testa_value = test1.value
                                            #
                                if not testb:
                                    # print("no vale b")
                                    testb_value = 0.0
                                else:
                                    for test2 in testb:
                                        if(test2.subject_id == subject.id):
                                            testb_value = test2.value
                                total_eval = testa_value + testb_value
                                moyentt = total_eval / 2
                                # print(moyentt)

                                subj_moy = f"{subject.id}_{moyentt}_{subject.title}"
                                total_coeff = total_coeff + decimal.Decimal(evals.subject.coef)
                                # total
                                moy_tot = moyentt  * int(evals.subject.coef)
                                total_tot = total_tot + decimal.Decimal(moy_tot)
                                subj_moy_tot = f"{subject.title}_{subject.id}_{moyentt}_{moy_tot}"
                                # print(subj_moy_tot)
                                # print(testb)
                                if(subject.category == 'General'):
                                    total_gen_tot = total_gen_tot + total_tot
                                    #
                                if(subject.category == 'Professional'):
                                    total_prof_tot = total_prof_tot + moy_tot
                                    #
                                # subject_value_cat.append([test1.subject.title,testa_value,testb_value, moyentt, moy_tot,evals.subject.coef, test2.observation, subject.category, test1.teacher])
                                #
                            if(term == 'second'):
                                subjt_rang = "1"
                                testa = obj_eval_class.filter(title='Test3',subject_id=subject.id)
                                testb = obj_eval_class.filter(title='Test4',subject_id=subject.id)
                                print(term)
                                testa_value = 0.0
                                testb_value = 0.0
                                testb_coef = 0.0
                                testa_coef = 0.0

                                if testa:
                                    for test1 in testa:
                                        if(test1.subject_id == subject.id):
                                            testa_value = test1.value
                                            testa_coef = test1.coef

                                if testb:
                                    for test2 in testb:
                                        if(test2.subject_id == subject.id):
                                            testb_value = test2.value
                                            testb_coef = test2.coef
                                if(subject.category == 'General'):
                                    # print(f"General {subject.coef}")
                                    total_gen_coeff = total_gen_coeff + decimal.Decimal(testb_coef)
                                    subj_cat.append(subject.category)
                                    # total_gen_tot = total_gen_tot + decimal.Decimal(testb_coef)
                                #)
                                if(subject.category == 'Professional'):
                                    # print(f"Professional {testb_coef}")
                                    total_prof_coeff = total_prof_coeff + decimal.Decimal(testb_coef)
                                    subj_cat.append(subject.category)
                                # print(testa.teacher)
                                # print(testb)
                                # print('first')
                                # if not testa:
                                #     # print("no vale a")
                                #     testa_value = 0.0
                                # else:
                                #     for test1 in testa:
                                #         if(test1.subject_id == subject.id):
                                #             testa_value = test1.value
                                # if not testb:
                                #     # print("no vale b")
                                #     testb_value = 0.0
                                # else:
                                #     for test2 in testb:
                                #         if(test2.subject_id == subject.id):
                                #             testb_value = test2.value
                                total_eval = decimal.Decimal(testa_value) + decimal.Decimal(testb_value)
                                moyentt = total_eval / 2
                                # print(moyentt)

                                subj_moy = f"{subject.id}_{moyentt}_{subject.title}"
                                # print(subj_moy)
                                total_coeff = total_coeff + decimal.Decimal(testb_coef)
                                # total
                                moy_tot = moyentt  * int(testb_coef)
                                total_tot = total_tot + decimal.Decimal(moy_tot)
                                subj_moy_tot = f"{subject.title}_{subject.id}_{moyentt}_{moy_tot}"
                                # print(subj_moy_tot)
                                # print(testb)
                                if(subject.category == 'General'):
                                    total_gen_tot = total_gen_tot + total_tot
                                    subject_gen_tot = subject_gen_tot + float(moy_tot)
                                if(subject.category == 'Professional'):
                                    # total_gen_tot = total_gen_tot + total_tot
                                    subject_prof_tot = subject_prof_tot + float(moy_tot)
                                    total_prof_tot = total_prof_tot + moy_tot
                                    #
                                # if(test1.subject.title == "English Langauge"):
                                #     print(subject.category)
                                    #
                                subject_value_cat.append([test1.subject.title,testa_value,testb_value, moyentt, testb_coef, moy_tot, test1.observation, subject.category, test1.teacher])
                                # subject_value_cat.append([test1.subject.title,testa_value,testb_value, moyentt, subject.coef, moy_tot, test2.observation, subject.category, test1.teacher])
                                #
                            if(term == 'third'):
                                subjt_rang = "1"
                                testa = obj_eval_class.filter(title='Test5',subject_id=subject.id)
                                testb = obj_eval_class.filter(title='Test6',subject_id=subject.id)
                                # print('first')
                                if not testa:
                                    # print("no vale a")
                                    testa_value = 0.0
                                else:
                                    for test1 in testa:
                                        if(test1.subject_id == subject.id):
                                            testa_value = test1.value
                                if not testb:
                                    # print("no vale b")
                                    testb_value = 0.0
                                else:
                                    for test2 in testb:
                                        if(test2.subject_id == subject.id):
                                            testb_value = test2.value
                                total_eval = testa_value + testb_value
                                moyentt = total_eval / 2
                                # print(moyentt)

                                subj_moy = f"{subject.id}_{moyentt}_{subject.title}"
                                total_coeff = total_coeff + decimal.Decimal(evals.subject.coef)
                                # total
                                moy_tot = moyentt  * int(evals.subject.coef)
                                total_tot = total_tot + decimal.Decimal(moy_tot)
                                subj_moy_tot = f"{subject.title}_{subject.id}_{moyentt}_{moy_tot}"
                                # print(subj_moy_tot)
                                # print(testb)
                                if(subject.category == 'General'):
                                    total_gen_tot = total_gen_tot + total_tot
                                if(subject.category == 'Professional'):
                                    total_prof_tot = total_prof_tot + moy_tot
                                    #
                                # subject_value_cat.append([test1.subject.title,testa_value,testb_value, moyentt, moy_tot, subject.coef, test2.observation, subject.category,  test1.teacher])
                                subject_value_cat.append([test1.subject.title,testa_value,testb_value, moyentt, moy_tot, evals.subject.coef, test2.observation, subject.category,  test1.teacher])

            # y = float(x.quantity) * float(x.price)
            # invoiceTotal += y
    
    gen_sub_moy = decimal.Decimal(subject_gen_tot, ) / total_gen_coeff
    prof_sub_moy = decimal.Decimal(subject_prof_tot, ) / total_prof_coeff
    prof_gen_tot_moy = decimal.Decimal(total_tot, ) / total_coeff

    

    # print(subject_value_cat)
    # get student image obj_student_class
    def display_image( obj):
        if obj.stud_image:
            img_url = image_services.get_image_url_from_cloudflare(
                obj.stud_image.cloudflare_id, variant="thumbnailSmall"
                # obj.stud_image.cloudflare_id
            )
            print("obj")
            return img_url
        return "https://imagedelivery.net/FGazjujafzdf38AXQFJ0qw/834941c7-4e47-4404-a47c-c27bd18a4e00/thumbnailSmall"
    myimage = display_image(obj_student_class)

    meimage = "https://imagedelivery.net/FGazjujafzdf38AXQFJ0qw/834941c7-4e47-4404-a47c-c27bd18a4e00/thumbnailSmall"



    context = {}
    context['testimag'] = meimage
    context['onlinestudimag'] = myimage
    context['prof_sub_moy'] = round(prof_sub_moy, ndigits=2)
    context['prof_gen_tot_moy'] = round(prof_gen_tot_moy, ndigits=2)
    context['reportcard'] = obj_report_card
    context['subject_line'] = subject_value_cat
    context['p_settings'] = p_settings
    context['student'] = obj_student_class
    context['classroom'] = classroom
    context['total_coeff'] = total_coeff
    context['total_tot'] = total_tot
    context['total_gen_coeff'] = total_gen_coeff
    context['total_prof_coeff'] = total_prof_coeff
    context['gen_tot'] = total_gen_tot
    context['subject_gen_tot'] = subject_gen_tot #gen total subj
    context['gen_sub_moy'] = round(gen_sub_moy, ndigits=2)
    context['subj_cat'] = subj_cat
    context['total_prof_tot'] = total_prof_tot
    # context['avgTotal'] = "{:.2f}".format(invoiceTotal)

    # using now() to get current time
    current_time = datetime.datetime.now()

    #The name of your PDF file
    filename = f"{obj_student_class.name}_{classroom.class_name}_{obj_report_card.academic_year}_{current_time}.pdf"

    #HTML FIle to be converted to PDF - inside your Django directory
    template = get_template('reports/cards/pdf-template.html')


    #Render the HTML
    html = template.render(context)

    #Options - Very Important [Don't forget this]
      #Javascript delay is optional

    #Remember that location to wkhtmltopdf
    # path_wkthmltopdf = b'C:\wkhtmltopdf\\bin\wkhtmltopdf.exe'
    # config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    # config = pdfkit.configuration(wkhtmltopdf='C:/wkhtmltopdf/bin/wkhtmltopdf')
    #
    if platform.system() == "Windows":
        config = pdfkit.configuration(wkhtmltopdf=os.environ.get("WKHTMLTOPDF_PATH", "C:\wkhtmltopdf\\bin\wkhtmltopdf.exe"))
    else:
        WKHTMLTOPDF_CMD = subprocess.Popen(["which", os.environ.get("WKHTMLTOPDF_PATH", "/app/bin/wkhtmltopdf")],
        stdout=subprocess.PIPE).communicate()[0].strip()
        config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD)
    

    # css
    # html
    _html = template.render(context)
     # remove header
    _html = _html[_html.find('<body>'):] 
    new_header = '''<!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8" />
        <style>
        '''

    #IF you have CSS to add to template
    css1 = os.path.join(settings.CSS_LOCATION, 'assets', 'css', 'bootstrap.min.css')
    css_path = os.path.join(settings.CSS_LOCATION, 'assets', 'css', 'bootstrap.min.css')
    # css2 = os.path.join(settings.CSS_LOCATION, 'assets', 'css', 'dashboard.css')

    with open(css_path, 'r') as f:
        new_header += f.read()
    new_header += '\n</style>'
    print(new_header)

    # add head to html
    _html = new_header + _html[_html.find('<body>'):]
    # with open('../reports/cards/pdf-template.html', 'w') as f: f.write(_html)  # for debug

    options = {
          'encoding': 'UTF-8',
          'javascript-delay':'10', #Optional
        #   'enable-local-file-access': None, #To be able to access CSS
          'enable-local-file-access': "", #To be able to access CSS
          'page-size': 'A4',
          'custom-header' : [
              ('Accept-Encoding', 'gzip')
          ],
      }

    #Create the file
    file_content = pdfkit.from_string(html, False, configuration=config, options=options)
    # file_content = pdfkit.from_string(_html, False, configuration=config, options=options)

    #Create the HTTP Response
    response = HttpResponse(file_content, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename = {}'.format(filename)

    #Return
    return response





# @login_required
def viewDocumentInvoiceERRUR(request, slug):
    #fetch that reportcard
    try:
        #get student class
        print('student')
        obj_report_card = ReportCard.objects.get(id=slug)
        studentId = obj_report_card.student.id
        obj_student_class = Student.objects.get(id=studentId)
        # print(obj_student_class.specialty)

        classroomId = obj_student_class.student_class_id
        classroom =  ClassRoom.objects.get(id=classroomId)
        subjects = Subject.objects.filter(classroom=classroomId)
        # print(subjects)
        obj_eval_class = Eval.objects.filter(student_id=studentId)
        # print(obj_eval_class)
        pass
    except:
        messages.error(request, 'Something went wrong')
        return redirect('report_cards')

    #total coef
    # total_coeff = 0.00
    total_coeff = decimal.Decimal(0.0)
    #
    total_gen_coeff = decimal.Decimal(0.0)
    total_prof_coeff = decimal.Decimal(0.0)

    #total tot
    # total_tot = 0.00
    total_tot = decimal.Decimal(0.0)
    #
    total_gen_tot = decimal.Decimal(0.0)
    total_prof_tot = decimal.Decimal(0.0)

    #Get Client Settings
    p_settings = Settings.objects.get(clientName='GILEAD TECHNICAL HIGH SCHOOL')

    #get subjects
    term = obj_report_card.term

    # Create an empty of subjects and marks
    subject_value_cat = []

    # Create an empty of subjects and marks
    subj_cat = []

    # Create an empty of gen et prof
    subject_gen_tot = 0.0
    subject_prof_tot = 0.0

    subjt_rang = "1"

    #Calculate the Avg Total
    if len(subjects) > 0:
        for subject in subjects:
            # print(subject.coef)
            if subject.coef is None:
                # print('no subjj coef')
                messages.error(request, 'Something went wrong')
                return redirect('report_cards')
            else:
                # follow_object = Teacher.objects.filter(classrooms = classroom, t_subjects = subjects)
                # followers_of_teach = follow_object.t_subjects.all()
                # print(follow_object)
                # print("subject title")
                # print(subject.title)
                # print("subject term")
                # print(obj_report_card.term)
                if(subject.category == 'General'):
                    # print(f"General {subject.coef}")
                    total_gen_coeff = total_gen_coeff + decimal.Decimal(subject.coef)
                    subj_cat.append(subject.category)
                    # total_gen_tot = total_gen_tot + decimal.Decimal(subject.coef)
                #)
                if(subject.category == 'Professional'):
                    # print(f"Professional {subject.coef}")
                    total_prof_coeff = total_prof_coeff + decimal.Decimal(subject.coef)
                    subj_cat.append(subject.category)
                #
                if(term == 'first'):
                    subjt_rang = "1"
                    testa = obj_eval_class.filter(title='Test1',subject_id=subject.id)
                    testb = obj_eval_class.filter(title='Test2',subject_id=subject.id)
                    # print('first')
                    if not testa:
                        # print("no vale a")
                        testa_value = 0.0
                    else:
                        for test1 in testa:
                            if(test1.subject_id == subject.id):
                                testa_value = test1.value
                                #
                    if not testb:
                        # print("no vale b")
                        testb_value = 0.0
                    else:
                        for test2 in testb:
                            if(test2.subject_id == subject.id):
                                testb_value = test2.value
                    total_eval = testa_value + testb_value
                    moyentt = total_eval / 2
                    # print(moyentt)

                    subj_moy = f"{subject.id}_{moyentt}_{subject.title}"
                    total_coeff = total_coeff + decimal.Decimal(subject.coef)
                    # total
                    moy_tot = moyentt  * int(subject.coef)
                    total_tot = total_tot + decimal.Decimal(moy_tot)
                    subj_moy_tot = f"{subject.title}_{subject.id}_{moyentt}_{moy_tot}"
                    # print(subj_moy_tot)
                    # print(testb)
                    if(subject.category == 'General'):
                        total_gen_tot = total_gen_tot + total_tot
                        #
                    if(subject.category == 'Professional'):
                        total_prof_tot = total_prof_tot + moy_tot
                        #
                    # subject_value_cat.append([test1.subject.title,testa_value,testb_value, moyentt, moy_tot,subject.coef, test2.observation, subject.category, test1.teacher])
                    #
                if(term == 'second'):
                    subjt_rang = "1"
                    testa = obj_eval_class.filter(title='Test3',subject_id=subject.id)
                    testb = obj_eval_class.filter(title='Test4',subject_id=subject.id)
                    print(term)
                    # print(testa.teacher)
                    print(testb)
                    # print('first')
                    if not testa:
                        # print("no vale a")
                        testa_value = 0.0
                    else:
                        for test1 in testa:
                            if(test1.subject_id == subject.id):
                                testa_value = test1.value
                    if not testb:
                        # print("no vale b")
                        testb_value = 0.0
                    else:
                        for test2 in testb:
                            if(test2.subject_id == subject.id):
                                testb_value = test2.value
                    total_eval = decimal.Decimal(testa_value) + decimal.Decimal(testb_value)
                    moyentt = total_eval / 2
                    # print(moyentt)

                    subj_moy = f"{subject.id}_{moyentt}_{subject.title}"
                    print(subj_moy)
                    total_coeff = total_coeff + decimal.Decimal(subject.coef)
                    # total
                    moy_tot = moyentt  * int(subject.coef)
                    total_tot = total_tot + decimal.Decimal(moy_tot)
                    subj_moy_tot = f"{subject.title}_{subject.id}_{moyentt}_{moy_tot}"
                    # print(subj_moy_tot)
                    # print(testb)
                    if(subject.category == 'General'):
                        total_gen_tot = total_gen_tot + total_tot
                        subject_gen_tot = subject_gen_tot + float(moy_tot)
                    if(subject.category == 'Professional'):
                        # total_gen_tot = total_gen_tot + total_tot
                        subject_prof_tot = subject_prof_tot + float(moy_tot)
                        total_prof_tot = total_prof_tot + moy_tot
                        #
                    # if(test1.subject.title == "English Langauge"):
                    #     print(subject.category)
                        #
                    subject_value_cat.append([subject.title,testa_value,testb_value, moyentt, subject.coef, moy_tot, test2.observation, subject.category, test2.teacher])
                    # subject_value_cat.append([test1.subject.title,testa_value,testb_value, moyentt, subject.coef, moy_tot, test2.observation, subject.category, test1.teacher])
                    #
                if(term == 'third'):
                    subjt_rang = "1"
                    testa = obj_eval_class.filter(title='Test5',subject_id=subject.id)
                    testb = obj_eval_class.filter(title='Test6',subject_id=subject.id)
                    # print('first')
                    if not testa:
                        # print("no vale a")
                        testa_value = 0.0
                    else:
                        for test1 in testa:
                            if(test1.subject_id == subject.id):
                                testa_value = test1.value
                    if not testb:
                        # print("no vale b")
                        testb_value = 0.0
                    else:
                        for test2 in testb:
                            if(test2.subject_id == subject.id):
                                testb_value = test2.value
                    total_eval = testa_value + testb_value
                    moyentt = total_eval / 2
                    # print(moyentt)

                    subj_moy = f"{subject.id}_{moyentt}_{subject.title}"
                    total_coeff = total_coeff + decimal.Decimal(subject.coef)
                    # total
                    moy_tot = moyentt  * int(subject.coef)
                    total_tot = total_tot + decimal.Decimal(moy_tot)
                    subj_moy_tot = f"{subject.title}_{subject.id}_{moyentt}_{moy_tot}"
                    # print(subj_moy_tot)
                    # print(testb)
                    if(subject.category == 'General'):
                        total_gen_tot = total_gen_tot + total_tot
                    if(subject.category == 'Professional'):
                        total_prof_tot = total_prof_tot + moy_tot
                        #
                    # subject_value_cat.append([test1.subject.title,testa_value,testb_value, moyentt, moy_tot, subject.coef, test2.observation, subject.category,  test1.teacher])
                    subject_value_cat.append([test1.subject.title,testa_value,testb_value, moyentt, moy_tot, subject.coef, test2.observation, subject.category,  test1.teacher])

            # y = float(x.quantity) * float(x.price)
            # invoiceTotal += y
    
    gen_sub_moy = decimal.Decimal(subject_gen_tot, ) / total_gen_coeff
    prof_sub_moy = decimal.Decimal(subject_prof_tot, ) / total_prof_coeff
    prof_gen_tot_moy = decimal.Decimal(total_tot, ) / total_coeff

    

    # print(subject_value_cat)



    context = {}
    context['prof_sub_moy'] = round(prof_sub_moy, ndigits=2)
    context['prof_gen_tot_moy'] = round(prof_gen_tot_moy, ndigits=2)
    context['reportcard'] = obj_report_card
    context['subject_line'] = subject_value_cat
    context['p_settings'] = p_settings
    context['student'] = obj_student_class
    context['classroom'] = classroom
    context['total_coeff'] = total_coeff
    context['total_tot'] = total_tot
    context['total_gen_coeff'] = total_gen_coeff
    context['total_prof_coeff'] = total_prof_coeff
    context['gen_tot'] = total_gen_tot
    context['subject_gen_tot'] = subject_gen_tot #gen total subj
    context['gen_sub_moy'] = round(gen_sub_moy, ndigits=2)
    context['subj_cat'] = subj_cat
    context['total_prof_tot'] = total_prof_tot
    # context['avgTotal'] = "{:.2f}".format(invoiceTotal)

    #The name of your PDF file
    filename = f"{obj_student_class.name}_{classroom.class_name}_{obj_report_card.academic_year}.pdf"

    #HTML FIle to be converted to PDF - inside your Django directory
    template = get_template('reports/cards/pdf-template.html')


    #Render the HTML
    html = template.render(context)

    #Options - Very Important [Don't forget this]
    options = {
          'encoding': 'UTF-8',
          'javascript-delay':'10', #Optional
          'enable-local-file-access': None, #To be able to access CSS
          'page-size': 'A4',
          'custom-header' : [
              ('Accept-Encoding', 'gzip')
          ],
      }
      #Javascript delay is optional

    #Remember that location to wkhtmltopdf
    # path_wkthmltopdf = b'C:\wkhtmltopdf\\bin\wkhtmltopdf.exe'
    # config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    # config = pdfkit.configuration(wkhtmltopdf='C:/wkhtmltopdf/bin/wkhtmltopdf')
    #
    if platform.system() == "Windows":
        config = pdfkit.configuration(wkhtmltopdf=os.environ.get("WKHTMLTOPDF_PATH", "C:\wkhtmltopdf\\bin\wkhtmltopdf.exe"))
    else:
        WKHTMLTOPDF_CMD = subprocess.Popen(["which", os.environ.get("WKHTMLTOPDF_PATH", "/app/bin/wkhtmltopdf")],
        stdout=subprocess.PIPE).communicate()[0].strip()
        config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD)

    #IF you have CSS to add to template
    css1 = os.path.join(settings.CSS_LOCATION, 'assets', 'css', 'bootstrap.min.css')
    # css2 = os.path.join(settings.CSS_LOCATION, 'assets', 'css', 'dashboard.css')

    #Create the file
    file_content = pdfkit.from_string(html, False, configuration=config, options=options)

    #Create the HTTP Response
    response = HttpResponse(file_content, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename = {}'.format(filename)

    #Return
    return response






def OLDcreate_report_card(request):
    # eval = Eval.objects.all()
    student = Student.objects.all()
    context = {
        'student':student,
    }

    if request.method == "POST":
        student = request.POST.get('student')
        term = request.POST.get('term')
        academic_yr = request.POST.get('academic_year')
        resumptn = request.POST.get('resumptn_date')
        added_by = request.user.username

        #get student class
        print('student')
        obj_student_class = Student.objects.get(id=student)

        classroomId = obj_student_class.student_class_id
        classroom =  ClassRoom.objects.get(id=classroomId)

        #get test
        print('test')
        obj_eval_class = Eval.objects.filter(student_id=student)
        # print(obj_eval_class)

        #get subject
        print('subject')
        # list_subject = Subject.classroom.all()
        # print(list_subject)
        # obj_eval_class = Eval.objects.filter(student_id=student)
        results = Subject.objects.filter(classroom=classroomId)
        # print(results)

        #total coef
        # total_coeff = 0.00
        total_coeff = decimal.Decimal(0.0)
        #
        total_gen_coeff = decimal.Decimal(0.0)
        total_prof_coeff = decimal.Decimal(0.0)

        #total tot
        # total_tot = 0.00
        total_tot = decimal.Decimal(0.0)
        #
        total_gen_tot = decimal.Decimal(0.0)

        if results is None:
            print("not results")
            print(results)
        else:
            for subjj_cl in results:
                print(subjj_cl.id)
                print(subjj_cl.coef)
                if subjj_cl.coef is None:
                    print('no subjj coef')
                else:
                    if(subjj_cl.category == 'General'):
                        print(f"General {subjj_cl.coef}")
                        total_gen_coeff = total_gen_coeff + decimal.Decimal(subjj_cl.coef)
                        # total_gen_tot = total_gen_tot + decimal.Decimal(subjj_cl.coef)
                    #)
                    if(subjj_cl.category == 'Professional'):
                        print(f"Professional {subjj_cl.coef}")
                        total_prof_coeff = total_prof_coeff + decimal.Decimal(subjj_cl.coef)
                    #
                    if(term == 'first'):
                        testa = obj_eval_class.filter(title='Test1',subject_id=subjj_cl.id)
                        testb = obj_eval_class.filter(title='Test2',subject_id=subjj_cl.id)
                        # print('first')
                        if not testa:
                            print("no vale a")
                            testa_value = 0.0
                        else:
                            for test1 in testa:
                                if(test1.subject_id == subjj_cl.id):
                                    testa_value = test1.value
                        if not testb:
                            print("no vale b")
                            testb_value = 0.0
                        else:
                            for test2 in testb:
                                if(test2.subject_id == subjj_cl.id):
                                    testb_value = test2.value
                        total_eval = testa_value + testb_value
                        moyentt = total_eval / 2
                        # print(moyentt)

                        subj_moy = f"{subjj_cl.id}_{moyentt}_{subjj_cl.title}"
                        total_coeff = total_coeff + decimal.Decimal(subjj_cl.coef)
                        # total
                        moy_tot = moyentt  * int(subjj_cl.coef)
                        total_tot = total_tot + decimal.Decimal(moy_tot)
                        subj_moy_tot = f"{subjj_cl.title}_{subjj_cl.id}_{moyentt}_{moy_tot}"
                        print(subj_moy_tot)
                        # print(testb)
                        if(subjj_cl.category == 'General'):
                            total_gen_tot = total_gen_tot + total_tot

                    if(term == 'second'):
                        testa = obj_eval_class.filter(title='Test3').filter(subject_id=subjj_cl.id)
                        testb = obj_eval_class.filter(title='Test4',subject_id=subjj_cl.id)
                        # print('test3')
                        # print(testa.filter(subject_id=subjj_cl.id))
                        if not testa:
                            print("no vale a")
                            testa_value = 0.0
                        else:
                            for test1 in testa:
                                # print(test.value)
                                if(test1.subject_id == subjj_cl.id):
                                    # print("yes")
                                    # print('test3')
                                    # print(test1.value)
                                    testa_value = test1.value
                        if not testb:
                            print("no vale b")
                            testb_value = 0.0
                        else:
                            for test2 in testb:
                                if(test2.subject_id == subjj_cl.id):
                                    # print("yes")
                                    # print('test4')
                                    # print(test2.value)
                                    testb_value = test2.value
                        # print(testa.values().value)
                        # print('type')
                        # print(type(testa_value))
                        # print(type(testb_value))
                        total_eval = decimal.Decimal(testa_value) + decimal.Decimal(testb_value) 
                        moyentt = total_eval / 2
                        # print(moyentt)

                        subj_moy = f"{subjj_cl.id}_{moyentt}_{subjj_cl.title}"
                        print(subj_moy)

                        # print("coef")
                        # print(subjj_cl.coef)
                        # print("type(subjj_cl.id)")
                        # print(type(subjj_cl.coef))
                        # print(subjj_cl.title)
                        # print(type(total_coeff))
                        total_coeff = total_coeff + decimal.Decimal(subjj_cl.coef)
                        # total
                        moy_tot = moyentt  * int(subjj_cl.coef)
                        # print(type(moy_tot))
                        # print(type(total_tot))
                        # print(total_tot)
                        total_tot = total_tot + decimal.Decimal(moy_tot)
                        subj_moy_tot = f"{subjj_cl.title}_{subjj_cl.id}_{moyentt}_{moy_tot}"
                        print(subj_moy_tot)

                        # print('test4')
                        # print(testb)
                        if(subjj_cl.category == 'General'):
                            total_gen_tot = total_gen_tot + total_tot

                    if(term == 'third'):
                        testa = obj_eval_class.filter(title='Test5')
                        testb = obj_eval_class.filter(title='Test6')
                        # print('first')
                        if not testa:
                            print("no vale a")
                            testa_value = 0.0
                        else:
                            for test1 in testa:
                                if(test1.subject_id == subjj_cl.id):
                                    testa_value = test1.value
                        if not testb:
                            print("no vale b")
                            testb_value = 0.0
                        else:
                            for test2 in testb:
                                if(test2.subject_id == subjj_cl.id):
                                    testb_value = test2.value
                        total_eval = testa_value + testb_value
                        moyentt = total_eval / 2
                        # print(moyentt)

                        subj_moy = f"{subjj_cl.id}_{moyentt}_{subjj_cl.title}"
                        total_coeff = total_coeff + decimal.Decimal(subjj_cl.coef)
                        # total
                        moy_tot = moyentt  * int(subjj_cl.coef)
                        total_tot = total_tot + decimal.Decimal(moy_tot)
                        subj_moy_tot = f"{subjj_cl.title}_{subjj_cl.id}_{moyentt}_{moy_tot}"
                        print(subj_moy_tot)
                        # print(testb)
                        if(subjj_cl.category == 'General'):
                            total_gen_tot = total_gen_tot + total_tot
            #

            #total
            print(total_coeff)
            print(total_tot)
            print("general")
            print(total_gen_coeff)
            print(f"General tot: {total_gen_tot}")
            print("prof")
            print(total_prof_coeff)
        

            report_card = ReportCard.objects.create(
                student = obj_student_class ,
                term = term,
                student_rank = 1,
                general_subjs_avr = total_gen_tot,
                prof_subjs_avr = total_tot - total_gen_tot,
                total_avr = total_tot,
                best_avr = total_tot,
                worst_avr = total_tot,
                firstterm_avr = total_tot,
                secondterm_avr = total_tot,
                # academic_year = '2023/2024',
                academic_year = academic_yr,
                resumption = resumptn,
                # teacher = teacher,
                added_by = added_by,
            )

        # messages.success(request, 'Eval added Successfully')
        # return redirect("test_list")
    

    return render(request, "reports/add-card.html", context=context)




def ANCIENcreate_report_card(request):
    # eval = Eval.objects.all()
    student = Student.objects.all()
    context = {
        'student':student,
    }

    if request.method == "POST":
        student = request.POST.get('student')
        term = request.POST.get('term')
        academic_yr = request.POST.get('academic_year')
        resumptn = request.POST.get('resumptn_date')
        added_by = request.user.username

        #get student class
        print('student')
        obj_student_class = Student.objects.get(id=student)

        classroomId = obj_student_class.student_class_id
        classroom =  ClassRoom.objects.get(id=classroomId)

        #get test
        print('test')
        obj_eval_class = Eval.objects.filter(student_id=student)
        # print(obj_eval_class)

        #get subject
        print('subject')
        # list_subject = Subject.classroom.all()
        # print(list_subject)
        # obj_eval_class = Eval.objects.filter(student_id=student)
        results = Subject.objects.filter(classroom=classroomId)
        # print(results)

        #total coef
        # total_coeff = 0.00
        total_coeff = decimal.Decimal(0.0)
        #
        total_gen_coeff = decimal.Decimal(0.0)
        total_prof_coeff = decimal.Decimal(0.0)

        #total tot
        # total_tot = 0.00
        total_tot = decimal.Decimal(0.0)
        #
        total_gen_tot = decimal.Decimal(0.0)

        if results is None:
            print("not results")
            print(results)
        else:
            for subjj_cl in results:
                print(subjj_cl.id)
                print(subjj_cl.coef)
                if subjj_cl.coef is None:
                    print('no subjj coef')
                else:
                    if(subjj_cl.category == 'General'):
                        print(f"General {subjj_cl.coef}")
                        total_gen_coeff = total_gen_coeff + decimal.Decimal(subjj_cl.coef)
                        # total_gen_tot = total_gen_tot + decimal.Decimal(subjj_cl.coef)
                    #)
                    if(subjj_cl.category == 'Professional'):
                        print(f"Professional {subjj_cl.coef}")
                        total_prof_coeff = total_prof_coeff + decimal.Decimal(subjj_cl.coef)
                    #
                    if(term == 'first'):
                        testa = obj_eval_class.filter(title='Test1',subject_id=subjj_cl.id)
                        testb = obj_eval_class.filter(title='Test2',subject_id=subjj_cl.id)
                        # print('first')
                        if not testa:
                            print("no vale a")
                            testa_value = 0.0
                        else:
                            for test1 in testa:
                                if(test1.subject_id == subjj_cl.id):
                                    testa_value = test1.value
                        if not testb:
                            print("no vale b")
                            testb_value = 0.0
                        else:
                            for test2 in testb:
                                if(test2.subject_id == subjj_cl.id):
                                    testb_value = test2.value
                        total_eval = testa_value + testb_value
                        moyentt = total_eval / 2
                        # print(moyentt)

                        subj_moy = f"{subjj_cl.id}_{moyentt}_{subjj_cl.title}"
                        total_coeff = total_coeff + decimal.Decimal(subjj_cl.coef)
                        # total
                        moy_tot = moyentt  * int(subjj_cl.coef)
                        total_tot = total_tot + decimal.Decimal(moy_tot)
                        subj_moy_tot = f"{subjj_cl.title}_{subjj_cl.id}_{moyentt}_{moy_tot}"
                        print(subj_moy_tot)
                        # print(testb)
                        if(subjj_cl.category == 'General'):
                            total_gen_tot = total_gen_tot + total_tot

                    if(term == 'second'):
                        testa = obj_eval_class.filter(title='Test3').filter(subject_id=subjj_cl.id)
                        testb = obj_eval_class.filter(title='Test4',subject_id=subjj_cl.id)
                        # print('test3')
                        # print(testa.filter(subject_id=subjj_cl.id))
                        if not testa:
                            print("no vale a")
                            testa_value = 0.0
                        else:
                            for test1 in testa:
                                # print(test.value)
                                if(test1.subject_id == subjj_cl.id):
                                    # print("yes")
                                    # print('test3')
                                    # print(test1.value)
                                    testa_value = test1.value
                        if not testb:
                            print("no vale b")
                            testb_value = 0.0
                        else:
                            for test2 in testb:
                                if(test2.subject_id == subjj_cl.id):
                                    # print("yes")
                                    # print('test4')
                                    # print(test2.value)
                                    testb_value = test2.value
                        # print(testa.values().value)
                        # print('type')
                        # print(type(testa_value))
                        # print(type(testb_value))
                        total_eval = decimal.Decimal(testa_value) + decimal.Decimal(testb_value) 
                        moyentt = total_eval / 2
                        # print(moyentt)

                        subj_moy = f"{subjj_cl.id}_{moyentt}_{subjj_cl.title}"
                        print(subj_moy)

                        # print("coef")
                        # print(subjj_cl.coef)
                        # print("type(subjj_cl.id)")
                        # print(type(subjj_cl.coef))
                        # print(subjj_cl.title)
                        # print(type(total_coeff))
                        total_coeff = total_coeff + decimal.Decimal(subjj_cl.coef)
                        # total
                        moy_tot = moyentt  * int(subjj_cl.coef)
                        # print(type(moy_tot))
                        # print(type(total_tot))
                        # print(total_tot)
                        total_tot = total_tot + decimal.Decimal(moy_tot)
                        subj_moy_tot = f"{subjj_cl.title}_{subjj_cl.id}_{moyentt}_{moy_tot}"
                        print(subj_moy_tot)

                        # print('test4')
                        # print(testb)
                        if(subjj_cl.category == 'General'):
                            total_gen_tot = total_gen_tot + total_tot

                    if(term == 'third'):
                        testa = obj_eval_class.filter(title='Test5')
                        testb = obj_eval_class.filter(title='Test6')
                        # print('first')
                        if not testa:
                            print("no vale a")
                            testa_value = 0.0
                        else:
                            for test1 in testa:
                                if(test1.subject_id == subjj_cl.id):
                                    testa_value = test1.value
                        if not testb:
                            print("no vale b")
                            testb_value = 0.0
                        else:
                            for test2 in testb:
                                if(test2.subject_id == subjj_cl.id):
                                    testb_value = test2.value
                        total_eval = testa_value + testb_value
                        moyentt = total_eval / 2
                        # print(moyentt)

                        subj_moy = f"{subjj_cl.id}_{moyentt}_{subjj_cl.title}"
                        total_coeff = total_coeff + decimal.Decimal(subjj_cl.coef)
                        # total
                        moy_tot = moyentt  * int(subjj_cl.coef)
                        total_tot = total_tot + decimal.Decimal(moy_tot)
                        subj_moy_tot = f"{subjj_cl.title}_{subjj_cl.id}_{moyentt}_{moy_tot}"
                        print(subj_moy_tot)
                        # print(testb)
                        if(subjj_cl.category == 'General'):
                            total_gen_tot = total_gen_tot + total_tot
            #

            #total
            print(total_coeff)
            print(total_tot)
            print("general")
            print(total_gen_coeff)
            print(f"General tot: {total_gen_tot}")
            print("prof")
            print(total_prof_coeff)
        

            report_card = ReportCard.objects.create(
                student = obj_student_class ,
                term = term,
                student_rank = 1,
                general_subjs_avr = total_gen_tot,
                prof_subjs_avr = total_tot - total_gen_tot,
                total_avr = total_tot,
                best_avr = total_tot,
                worst_avr = total_tot,
                firstterm_avr = total_tot,
                secondterm_avr = total_tot,
                # academic_year = '2023/2024',
                academic_year = academic_yr,
                resumption = resumptn,
                # teacher = teacher,
                added_by = added_by,
            )

        # messages.success(request, 'Eval added Successfully')
        # return redirect("test_list")
    

    return render(request, "reports/add-card.html", context=context)



#stats
# @login_required
def consolidation(request):
    students = Student.objects.all()
    context = {
        'students':students,
    }
    #consolidation


    if request.method == "POST":
    
        #get student class
        try:
            #les element du form
            annee = request.POST.get('academic_year')
            term = request.POST.get('school_term')
            type = request.POST.get('type')
            # 
            classrooms =  ClassRoom.objects.all()
            specialties =  Specialty.objects.all()
            num_specialties = Specialty.objects.all().count()
            # print("num_specialties")
            # print(num_specialties)
            departments =  Department.objects.all()
            # evaluations = Eval.objects.filter(term=term, academic_year=annee )
            # print(subjects)
            pass
        except Exception as e:
            messages.error(request, f' {e} Something went wrong')
            return redirect('consolidations')
        

        #get the number of students per class
        #count number of female in class 1
        count_girl_form1 = Student.objects.filter(gender="Female",student_class="1").count()
        print(f"num of girls in form 1 is {count_girl_form1}")

        count_male_form = 0
        count_female_form = 0
        count_form_total = 0
        student_gender_count = []
        data_non_consolidation = []
        spec_count_male_form = 0
        spec_count_female_form = 0

        for classes in classrooms:
            # print(classes)
            for student in students:
                if student.gender == "Male":
                    count_male_form = Student.objects.filter(gender="Male",student_class=classes.id).count()
                    
                if student.gender == "Female":
                    count_female_form = Student.objects.filter(gender="Female",student_class=classes.id).count()
                
            # print(f"num of females in form 1 is {count_female_form}")
            # print(f"num of males in form 1 is {count_male_form}")
            # count_form_total = count_female_form + count_male_form
            # print(f"num of Students in {classes.class_name} is {count_form_total}")
            count_form = Student.objects.filter(student_class=classes.id).count()
            # print(f"NEW num of Students in {classes.class_name} is {count_form}")
            student_gender_count.append([count_male_form,count_female_form,count_form,classes.class_name])
            # student_gender_count.append([count_male_form,count_female_form,count_form,classes.class_name])
        for specialty in specialties:
            for classes in classrooms:
                spec_count_male_form = Student.objects.filter(gender="Male",student_class=classes.id, specialty=specialty).count()
                        
                spec_count_female_form = Student.objects.filter(gender="Female",student_class=classes.id, specialty=specialty).count()
                spec_count_form = Student.objects.filter(student_class=classes.id, specialty=specialty).count()
            data_non_consolidation.append([specialty.name,spec_count_male_form,spec_count_female_form,spec_count_form])
    

        #total coef
        # total_coeff = 0.00
        total_coeff = decimal.Decimal(0.0)
        #
        total_gen_coeff = decimal.Decimal(0.0)
        total_prof_coeff = decimal.Decimal(0.0)

        #total tot
        # total_tot = 0.00
        total_tot = decimal.Decimal(0.0)
        #
        total_gen_tot = decimal.Decimal(0.0)
        total_prof_tot = decimal.Decimal(0.0)

        #Get Client Settings
        p_settings = Settings.objects.get(clientName='GILEAD TECHNICAL HIGH SCHOOL')

        #get subjects
        term = term

        #heading
        pdf_heading = ""
        
        # if term == "first":
        #     print(term)
        # elif term == "second":
        #     print(term)
        #     #get the test relatives too students
        # elif term == "third":
        #     print(term)
        
        # if type == "consolidation":
        #     print(type)
        #     # pdf_heading = ""
        # elif type == "non_consolidation":
        #     print(type)
        
        if term == "second" and type == "consolidation":
            pdf_heading = f"SECOND TERM GENERAL CONSOLIDATED STATISTICS, ACADEMIC YEAR {annee} "
        if term == "frist" and type == "consolidation":
            pdf_heading = f"FRIST TERM GENERAL CONSOLIDATED STATISTICS, ACADEMIC YEAR {annee} "
        if term == "third" and type == "consolidation":
            pdf_heading = f"THIRD TERM GENERAL CONSOLIDATED STATISTICS, ACADEMIC YEAR {annee} "
        
        if term == "second" and type == "non_consolidation":
            pdf_heading = f"SECOND TERM GENERAL CONSOLIDATED STATISTICS, ACADEMIC YEAR {annee} "
        if term == "frist" and type == "non_consolidation":
            pdf_heading = f"FRIST TERM GENERAL CONSOLIDATED STATISTICS, ACADEMIC YEAR {annee} "
        if term == "third" and type == "non_consolidation":
            pdf_heading = f"THIRD TERM GENERAL CONSOLIDATED STATISTICS, ACADEMIC YEAR {annee} "

        # Create an empty of subjects and marks
        subject_value_cat = []

        # Create an empty of subjects and marks
        subj_cat = []

        # Create an empty of gen et prof
        subject_gen_tot = 0.0
        subject_prof_tot = 0.0

        subjt_rang = "1"

        #Calculate the Avg Total
        

            

        # print(subject_value_cat)

        # print(student_gender_count)
        print(data_non_consolidation)

        print("num_specialties")
        num_specialties = num_specialties + 2
        print(num_specialties)



        context = {}
        context['heading'] = pdf_heading
        context['classrooms'] = classrooms
        context['p_settings'] = p_settings
        context['classroom'] = classrooms
        context['stud_gen_count'] = student_gender_count
        context['specialtys'] = specialties
        context['num_specialtys'] = num_specialties
        context['info_non_consolidation'] = data_non_consolidation

        
        

        context['total_tot'] = total_tot
        context['total_gen_coeff'] = total_gen_coeff
        context['total_prof_coeff'] = total_prof_coeff
        context['gen_tot'] = total_gen_tot
        context['subject_gen_tot'] = subject_gen_tot #
        context['subj_cat'] = subj_cat
        context['total_prof_tot'] = total_prof_tot
        # context['avgTotal'] = "{:.2f}".format(invoiceTotal)

        # print(context)

        # using now() to get current time
        current_time = datetime.datetime.now()

        # return redirect("consolidations")
        #The name of your PDF file
        filename = f"{type}_{annee}_{current_time}.pdf"

        #HTML FIle to be converted to PDF - inside your Django directory
        template = get_template('reports/stats/pdf-consolidations.html')
        if type == "consolidation":
            template = get_template('reports/stats/pdf-consolidations.html')
        if type == "non_consolidation":
            template = get_template('reports/stats/pdf-non_consolidations.html')


        #Render the HTML
        html = template.render(context)

        #Options - Very Important [Don't forget this]
        options = {
            'encoding': 'UTF-8',
            'javascript-delay':'10', #Optional
            # 'enable-local-file-access': None, #To be able to access CSS
            'enable-local-file-access': None, #To be able to access CSS
            'page-size': 'A4',
            'orientation': 'Landscape',
            'custom-header' : [
                ('Accept-Encoding', 'gzip')
            ],
        }
        #Javascript delay is optional

        #Remember that location to wkhtmltopdf
        # path_wkthmltopdf = b'C:\wkhtmltopdf\\bin\wkhtmltopdf.exe'
        # config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
        # config = pdfkit.configuration(wkhtmltopdf='C:/wkhtmltopdf/bin/wkhtmltopdf')
        #
        if platform.system() == "Windows":
            config = pdfkit.configuration(wkhtmltopdf=os.environ.get("WKHTMLTOPDF_PATH", "C:\wkhtmltopdf\\bin\wkhtmltopdf.exe"))
        else:
            WKHTMLTOPDF_CMD = subprocess.Popen(["which", os.environ.get("WKHTMLTOPDF_PATH", "/app/bin/wkhtmltopdf")],
            stdout=subprocess.PIPE).communicate()[0].strip()
            config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD)

        #IF you have CSS to add to template
        css1 = os.path.join(settings.CSS_LOCATION, 'assets', 'css', 'bootstrap.min.css')
        # css2 = os.path.join(settings.CSS_LOCATION, 'assets', 'css', 'dashboard.css')

        #Create the file
        file_content = pdfkit.from_string(html, False, configuration=config, options=options)

        #Create the HTTP Response
        response = HttpResponse(file_content, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename = {}'.format(filename)

        #Return
        return response
    

    #Return
    return render(request, "consolidation/type-consolidation.html", context=context)






def tests_generate_csv(request): 
    response = HttpResponse(content_type='text/csv') 
    formatted_datetime = datetime.datetime.now()
    file_name = f"tests_{formatted_datetime}.csv"
    response['Content-Disposition'] = f'attachment; filename={file_name}'

    response.write(u'\ufeff'.encode('utf8'))
  
    writer = csv.writer(response) 
    writer.writerow(["title", "titre", "value",   "coef", "subject_code", "observation", "student", "teacher", "teacher_class", "academic_year", "added_by" ]) 
    # 

    tests = Eval.objects.all() 
    for test in tests: 
        # print("test_")
        # print(test)
            
        writer.writerow([ test.title, test.titre, test.value, test.coef, test.subject_code,test.observation, test.student, test.teacher, test.teacher_class, test.academic_year, test.added_by ]) 
        # 
        # 
  
    return response 


# @login_required
def testmoyspecsubj_generate_csv(request): 
    response = HttpResponse(content_type='text/csv') 
    formatted_datetime = datetime.datetime.now()
    file_name = f"testmoyspecsubjs_{formatted_datetime}.csv"
    response['Content-Disposition'] = f'attachment; filename={file_name}'

    response.write(u'\ufeff'.encode('utf8'))
  
    writer = csv.writer(response) 
    writer.writerow(["term", "classroom", "specialty", "student", "subject", "test_avg", "subj_coef", "observation", "academic_year", "freefield", "added_by" ]) 
    # 

    tests_moy_spec_subj = TestMoySpecialtySubjClass.objects.all() 
    for testmoyspec in tests_moy_spec_subj: 
        # print("test_")
        # print(test)
            
        writer.writerow([ testmoyspec.term, testmoyspec.classroom, testmoyspec.specialty, testmoyspec.student, testmoyspec.subject, testmoyspec.test_avg, testmoyspec.subj_coef, testmoyspec.observation, testmoyspec.academic_year, testmoyspec.freefield, testmoyspec.added_by ]) 
        # 
        # 
  
    return response 


# @login_required
def ranking_generate_csv(request): 
    response = HttpResponse(content_type='text/csv') 
    formatted_datetime = datetime.datetime.now()
    file_name = f"rankings_{formatted_datetime}.csv"
    response['Content-Disposition'] = f'attachment; filename={file_name}'

    response.write(u'\ufeff'.encode('utf8'))
  
    writer = csv.writer(response) 
    writer.writerow(["term", "classroom", "specialty", "total_coeff", "total_marks", "total_avg", "observation", "student", "academic_year", "freefield", "freefield2", "added_by" ]) 
    # 

    class_rankxs = ClassRanking.objects.all() 
    for class_rank in class_rankxs: 
        # print("test_")
        # print(test)
            
        writer.writerow([ class_rank.term, class_rank.classroom, class_rank.specialty,  class_rank.total_coeff, class_rank.total_marks, class_rank.total_avg, class_rank.observation, class_rank.student, class_rank.academic_year, class_rank.freefield, class_rank.freefield2, class_rank.added_by ]) 
        # 
        # 
  
    return response 


# @login_required
def reportcard_generate_csv(request): 
    response = HttpResponse(content_type='text/csv') 
    formatted_datetime = datetime.datetime.now()
    file_name = f"reportcard_{formatted_datetime}.csv"
    response['Content-Disposition'] = f'attachment; filename={file_name}'

    response.write(u'\ufeff'.encode('utf8'))
  
    writer = csv.writer(response) 
    writer.writerow(["student", "student_rank", "gen_coeff", "prof_coeff", "gen_total", "prof_total", "general_subjs_avr", "prof_subjs_avr", "total_avr", "best_avr", "worst_avr", "firstterm_avr", "secondterm_avr", "annuelle_avr", "date_of_report_card_generation", "first_subj_passed", "second_subj_passed", "third_subj_passed", "annual_subj_passed", "term", "academic_year", "resumption", "subj_moy", "moreinfo", "added_by" ]) 
    # 

    reportcards = ReportCard.objects.all() 
    for reportcd in reportcards: 
        # print("test_")
        # print(test)
            
        writer.writerow([ reportcd.student, reportcd.student_rank, reportcd.gen_coeff,  reportcd.prof_coeff, reportcd.gen_total, reportcd.prof_total, reportcd.general_subjs_avr, reportcd.prof_subjs_avr, reportcd.total_avr, reportcd.best_avr, reportcd.worst_avr, reportcd.firstterm_avr, reportcd.secondterm_avr, reportcd.annuelle_avr, reportcd.date_of_report_card_generation, reportcd.first_subj_passed,  reportcd.second_subj_passed, reportcd.third_subj_passed, reportcd.annual_subj_passed, reportcd.term, reportcd.academic_year, reportcd.resumption, reportcd.subj_moy, reportcd.moreinfo, reportcd.added_by ]) 
        # 
        # 
  
    return response 




