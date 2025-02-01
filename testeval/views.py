
import html
from django.conf import settings
from django.shortcuts import render
#
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
# from sympy import Sum
from django.db.models import Sum
import decimal
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



# Create your views here.

def eval_list(request):
    eval_list = Eval.objects.select_related('student').all()
    context = {
        'eval_list': eval_list,
    }
    return render(request, "eval/evals.html", context)


def report_card_list(request):
    report_card = ReportCard.objects.select_related('student').all()
    context = {
        'report_card_list': report_card,
    }
    return render(request, "reports/report_card.html", context)




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
        title = request.POST.get('title')
        titre = request.POST.get('titre')
        student = request.POST.get('student')
        value = request.POST.get('value')
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

        messages.success(request, 'Eval added Successfully')
        return redirect("test_list")
    

    return render(request, "eval/add-eval.html", context=context)




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






def delete_test(request, slug):
    if request.method == "POST":
        #
        eval = get_object_or_404(Eval, id = slug)
        eval.delete()

        return redirect('test_list')
    return HttpResponseForbidden()



#report card
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


def delete_report_card(request, slug):
    if request.method == "POST":
        #
        report_card = get_object_or_404(ReportCard, id = slug)
        student_name =  report_card.student.name
        report_card.delete()

        messages.success(request, f'{student_name} Record card')

        return redirect('report_cards')
    return HttpResponseForbidden()



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

        #get student class
        try:
            # print('student')
            obj_student_class = Student.objects.get(id=student)

            classroomId = obj_student_class.student_class_id
            classroom =  ClassRoom.objects.get(id=classroomId)
            #get student class
            print('student')
            obj_student_class = Student.objects.get(id=student)
            # print(obj_student_class.specialty)

            classroomId = obj_student_class.student_class_id
            classroom =  ClassRoom.objects.get(id=classroomId)
            subjects = Subject.objects.filter(classroom=classroomId)
            # print(subjects)
            obj_eval_class = Eval.objects.filter(student_id=student, academic_year=academic_yr)
            obj_eval_cl_type = Eval.objects.filter(student_id=student, title='Test3', academic_year=academic_yr)
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
        term = term

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
                                    print(subj_moy)
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



        context = {}
        context['prof_sub_moy'] = round(prof_sub_moy, ndigits=2)
        context['prof_gen_tot_moy'] = round(prof_gen_tot_moy, ndigits=2)
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

        print(context)

        # using now() to get current time
        current_time = datetime.datetime.now()

        report_card = ReportCard.objects.create(
            student           = obj_student_class ,
            term              = term,
            student_rank      = 1,
            gen_coeff         = total_gen_coeff,
            prof_coeff        = total_prof_coeff,
            gen_total         = subject_gen_tot,
            prof_total        = total_prof_tot,
            general_subjs_avr = round(gen_sub_moy, ndigits=2),
            prof_subjs_avr    = round(prof_sub_moy, ndigits=2),
            total_avr         = round(prof_gen_tot_moy, ndigits=2),
            best_avr          = round(prof_gen_tot_moy, ndigits=2),
            worst_avr         = round(prof_gen_tot_moy, ndigits=2),
            firstterm_avr     = round(prof_gen_tot_moy, ndigits=2),
            secondterm_avr    = round(prof_gen_tot_moy, ndigits=2),
            # academic_year = '2023/2024',
            academic_year     = academic_yr,
            resumption        = resumptn,
            # teacher = teacher,
            added_by          = added_by,
        )

        messages.success(request, f'{obj_student_class.name} Record Card added Successfully')
        return redirect("report_cards")
    student = Student.objects.all()
    context = {
        'student':student,
    }

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

    # using now() to get current time
    current_time = datetime.datetime.now()

    #The name of your PDF file
    filename = f"{obj_student_class.name}_{classroom.class_name}_{obj_report_card.academic_year}_{current_time}.pdf"

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

