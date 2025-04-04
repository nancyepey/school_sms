
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

from django.db.models import Count, Max, Min, Avg
from department.models import Department
from teacher.models import Teacher
from school.models import ClassRoom, Settings, Specialty

from .models import ClassRanking, Eval, ReportCard, SchoolClasRanking, TestMoySpecialtySubjClass
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
# 
from django.db.models import Q
#paginator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



# Create your views here.

@login_required
def eval_list(request):
    # print("in")
    if request.user.is_teacher:
        eval_list = Eval.objects.filter(teacher_class=request.user.teacher_profile)
    else:
        eval_list = Eval.objects.all()
    # print("in all")
    classroom = ClassRoom.objects.all()
    specialtys = Specialty.objects.all()
    # print("in in")
    # pagination
    paginator = None

    # search
    if 'q_test' in request.GET:
        search=request.GET['q_test']
        if request.user.is_teacher:
            eval_list =  Eval.objects.filter(Q(teacher_class__usname__icontains = request.user.username) | Q(title__icontains = search) | Q(titre__icontains = search) | Q(academic_year__icontains = search) | Q(teacher__icontains = search)  | Q(subject_code__icontains = search)  | Q(subject__title__icontains = search) | Q(student__name__icontains = search) | Q(student__admission_number__icontains = search) | Q(teacher_class__name__icontains = search) )
        else:
            eval_list =  Eval.objects.filter(Q(title__icontains = search) | Q(titre__icontains = search) | Q(academic_year__icontains = search) | Q(teacher__icontains = search)  | Q(subject_code__icontains = search)  | Q(subject__title__icontains = search) | Q(student__name__icontains = search) | Q(student__admission_number__icontains = search) | Q(teacher_class__name__icontains = search) )

        
        try:
            if eval_list:
                # print(eval_list)
                if eval_list.exists():
                    paginator = Paginator(eval_list, 20)
                    eval_list = paginator.page(1)
                    page = request.GET.get("page")
        
                    try:
                        eval_list = paginator.page(page)
                        
                    except PageNotAnInteger:
                        eval_list = paginator.page(1)
                    
                    except EmptyPage:
                        eval_list = paginator.page(paginator.num_pages)
        except:
            # print("nooo")
            pass
        
        # else:
        #     msg = "There is no article with the keyword"
    
    # 
       
    else:
        paginator = Paginator(eval_list, 20)
        page = request.GET.get("page")
        # print(page)
        
        try:
            eval_list = paginator.page(page)
            
        except PageNotAnInteger:
            eval_list = paginator.page(1)
        
        except EmptyPage:
            eval_list = paginator.page(paginator.num_pages)
        
    if page:
        page_n1 = int(page) - 1

        page_p1 = int(page) + 1
    else:
        page_n1 = 0
        page_p1 = 0

    
    context = {
        'eval_list': eval_list,
        'classroom':classroom,
        'specialtys':specialtys,
        "paginator": paginator,
        
        "pag_prev": page_n1,
        "pag_next": page_p1,
    }
    if request.method == 'POST':
        # print(request)
        class_selected = request.POST.get('student_class')
        # print(class_selected)
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
            try:
                if eval_list:
                    if eval_list.exists():
                        paginator = Paginator(eval_list, 20)
                        eval_list = paginator.page(1)
                        page = request.GET.get("page")
            
                        try:
                            eval_list = paginator.page(page)
                            
                        except PageNotAnInteger:
                            eval_list = paginator.page(1)
                        
                        except EmptyPage:
                            eval_list = paginator.page(paginator.num_pages)
            except:
                # print("nooo")
                pass
            context = {
                'eval_list': eval_list,
                'classroom':classroom,
                'specialtys':specialtys,
                'codeclass_selected': "all",
                'specialty_selected': "all",
                 "paginator": paginator,
            }
        if class_selected != "all" and specialty_selected == "all":
            get_class = ClassRoom.objects.get(id = class_selected)
            eval_list = Eval.objects.filter( student__student_class=get_class )
            
            try:
                if eval_list:
                    if eval_list.exists():
                        paginator = Paginator(eval_list, 20)
                        eval_list = paginator.page(1)
                        page = request.GET.get("page")
            
                        try:
                            eval_list = paginator.page(page)
                            
                        except PageNotAnInteger:
                            eval_list = paginator.page(1)
                        
                        except EmptyPage:
                            eval_list = paginator.page(paginator.num_pages)
            except:
                # print("nooo")
                pass
            context = {
                'eval_list': eval_list,
                'classroom':classroom,
                'specialtys':specialtys,
                'class_selected': get_class.class_name,
                'codeclass_selected': get_class.class_code,
                'specialty_selected': "all",
                 "paginator": paginator,
            }
        if class_selected == "all" and specialty_selected != "all":
            get_specialty = Specialty.objects.get(id = specialty_selected)
            eval_list = Eval.objects.filter( student__specialty=get_specialty )
            try:
                if eval_list:
                    if eval_list.exists():
                        paginator = Paginator(eval_list, 20)
                        eval_list = paginator.page(1)
                        page = request.GET.get("page")
            
                        try:
                            eval_list = paginator.page(page)
                            
                        except PageNotAnInteger:
                            eval_list = paginator.page(1)
                        
                        except EmptyPage:
                            eval_list = paginator.page(paginator.num_pages)
            except:
                # print("nooo")
                pass
            context = {
                'eval_list': eval_list,
                'classroom':classroom,
                'specialtys':specialtys,
                'specialty_selected': get_specialty.name,
                'codeclass_selected': "all",
                 "paginator": paginator,
            }
        if class_selected != "all" and specialty_selected != "all":
            get_class = ClassRoom.objects.get(id = class_selected)
            get_specialty = Specialty.objects.get(id = specialty_selected)
            eval_list = Eval.objects.filter( student__student_class=get_class, student__specialty=get_specialty )
            try:
                if eval_list:
                    if eval_list.exists():
                        paginator = Paginator(eval_list, 20)
                        eval_list = paginator.page(1)
            except:
                # print("nooo")
                pass
            context = {
                'eval_list': eval_list,
                'classroom':classroom,
                'specialtys':specialtys,
                'class_selected': get_class.class_name,
                'codeclass_selected': get_class.class_code,
                'specialty_selected': get_specialty.name,
                 "paginator": paginator,
            }
        return render(request, "eval/evals.html", context)
    
    
    return render(request, "eval/evals.html", context)


@login_required
def report_card_list(request):
    report_card = ReportCard.objects.select_related('student').filter(is_actif=True)
    report_card_count = ReportCard.objects.select_related('student').filter(is_actif=True).count()
    print(f"{report_card_count}----report_card_count")
    
    classroom = ClassRoom.objects.all()
    specialtys = Specialty.objects.all()

    

    # search
    if 'q_card' in request.GET:
        search=request.GET['q_card']
        report_card = ReportCard.objects.filter(Q(student__name__icontains = search) | Q(term__icontains = search) | Q(total_avr__icontains = search) | Q(academic_year__icontains = search))


    context = {
        'report_card_list': report_card,
        'classroom':classroom,
        'specialtys':specialtys,
    }


    if request.method == 'POST':
        # print(request)
        class_selected = request.POST.get('student_class')
        specialty_selected = request.POST.get('stud_specialty')
        # get_class = ClassRoom.objects.get(id = class_selected)
        # report_card_list = ReportCard.objects.filter( student__student_class=get_class )
        # get_specialty = Specialty.objects.get(id = specialty_selected) 
        if class_selected == "all":
            get_class = ClassRoom.objects.all()
            if specialty_selected == "all":
                report_card_list = ReportCard.objects.filter(is_actif=True)
                get_specialty = Specialty.objects.all()
                context = {
                    'report_card_list': report_card_list,
                    'classroom':classroom,
                    'specialtys':specialtys,
                    'class_selected': class_selected,
                    'specialty_selected': get_specialty ,
                    # 'codeclass_selected': get_class.class_code,
                    "curent_rslt": f"{specialty_selected}_{class_selected}"
                }
            else:
                get_specialty = Specialty.objects.get(id = specialty_selected)
                report_card_list = ReportCard.objects.filter( student__specialty=get_specialty, is_actif=True)
                context = {
                    'report_card_list': report_card_list,
                    'classroom':classroom,
                    'specialtys':specialtys,
                    'class_selected': class_selected,
                    'specialty_selected': get_specialty.name ,
                    # 'codeclass_selected': get_class.class_code,
                    "curent_rslt": f"{specialty_selected}_{class_selected}"
                }
        else:
            get_class = ClassRoom.objects.get(id = class_selected)
            if specialty_selected == "all":
                get_specialty = Specialty.objects.all()
                report_card_list = ReportCard.objects.filter( student__student_class=get_class, is_actif=True)
                specialty_selected = "all"
                context = {
                    'report_card_list': report_card_list,
                    'classroom':classroom,
                    'specialtys':specialtys,
                    'class_selected': get_class.class_name,
                    'specialty_selected': get_specialty,
                    'codeclass_selected': get_class.class_code,
                    "curent_rslt": f"{specialty_selected}_{class_selected}"
                }
            else:
                get_specialty = Specialty.objects.get(id = specialty_selected)
                report_card_list = ReportCard.objects.filter( student__student_class=get_class, is_actif=True)
                context = {
                    'report_card_list': report_card_list,
                    'classroom':classroom,
                    'specialtys':specialtys,
                    'class_selected': get_class.class_name,
                    'specialty_selected': get_specialty.name,
                    'codeclass_selected': get_class.class_code,
                    "curent_rslt": f"{specialty_selected}_{class_selected}"
                }


        # context = {
        #     'report_card_list': report_card_list,
        #     'classroom':classroom,
        #     'specialtys':specialtys,
        #     'class_selected': get_class.class_name,
        #     'specialty_selected': get_specialty.name,
        #     'codeclass_selected': get_class.class_code,
        # }
    return render(request, "reports/report_card.html", context)



@login_required
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
        
        
        # student = request.POST.get('student')
        # browser = request.POST.get('browser')
        # print("browser")
        # print(browser)
        student = request.POST.get('selected_stud')
        # print(student)
        value = request.POST.get('value')
        value_two = request.POST.get('value_two')
        coef = request.POST.get('coeff')
        subject = request.POST.get('subject')
        # teacher = "teacher"
        teacher = request.POST.get('teacher')
        remarks = request.POST.get('remarks')
        added_by = request.user.username
        

        
        
        if not value:
            value = 0.00
            absent_one = True
        if not value_two:
            value_two = 0.00
            absent_two = True
        
        

        try:


            #get student class
            # print('student')
            # obj_student_class = Student.objects.get(id=student)
            obj_student_class = Student.objects.filter(name=student).first()

            #get teacher class
            # print('teacher')
            # print(teacher)
            obj_teacher_class = Teacher.objects.get(id=teacher)
            # print(obj_teacher_class)

            #get subject class
            # print('subject')
            obj_subject_class = Subject.objects.get(id=subject)
        except:
            messages.error(request, f'Oops and error occured')
            return redirect("test_list")


        # check if test exist
        check_tests = Eval.objects.filter(student=obj_student_class, subject=obj_subject_class, title=title, academic_year="2024/2025").first()
        if check_tests:
            messages.error(request, f'{obj_student_class.name}-- {obj_subject_class.title} --- Already exist')
            return redirect("test_list")
        else:
            # print(value_two)
            if not value and value_two:
                value = 0.00
                absent_one = True
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
                    seqone_is_absent = absent_one
                )
            if not value_two and value:
                value_two = 0.00
                absent_two = True
                test = Eval.objects.create(
                    title = title,
                    titre = titre,
                    value = value,
                    sec_title = title1,
                    sec_titre = titre1,
                    sec_value = value_two,
                    coef = coef,
                    subject = obj_subject_class,
                    observation = remarks,
                    student = obj_student_class,
                    teacher = obj_teacher_class,
                    teacher_class = obj_teacher_class,
                    added_by = added_by,
                    seqtwo_is_absent = absent_two
                )
            if value_two and value:
                test = Eval.objects.create(
                    title = title,
                    titre = titre,
                    value = value,
                    sec_title = title1,
                    sec_titre = titre1,
                    sec_value = value_two,
                    coef = coef,
                    subject = obj_subject_class,
                    observation = remarks,
                    student = obj_student_class,
                    teacher = obj_teacher_class,
                    teacher_class = obj_teacher_class,
                    added_by = added_by,
                )
            # if float(value_two) >= 0:
            #     value1 = value_two
            #     #test
            #     test = Eval.objects.create(
            #         title = title,
            #         titre = titre,
            #         value = value,
            #         sec_title = title1,
            #         sec_titre = titre1,
            #         sec_value = value1,
            #         coef = coef,
            #         subject = obj_subject_class,
            #         observation = remarks,
            #         student = obj_student_class,
            #         teacher = obj_teacher_class,
            #         teacher_class = obj_teacher_class,
            #         added_by = added_by,
            #     )
            # else:
            #     test = Eval.objects.create(
            #         title = title,
            #         titre = titre,
            #         value = value,
            #         coef = coef,
            #         subject = obj_subject_class,
            #         observation = remarks,
            #         student = obj_student_class,
            #         teacher = obj_teacher_class,
            #         teacher_class = obj_teacher_class,
            #         added_by = added_by,
            #     )

        messages.success(request, f'{obj_student_class.name}-- {obj_subject_class.title} --- Marks added Successfully')
        return redirect("test_list")
    

    return render(request, "eval/add-eval.html", context=context)



@login_required
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
        # title = request.POST.get('title')
        # titre = request.POST.get('titre')
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
        teacher = request.POST.get('teacher')
        remarks = request.POST.get('remarks')
        absent_one = False
        absent_two = False

        if not value:
            value = 0.00
            absent_one = True
        if not value_two:
            absent_two = True
            value_two = 0.00

        #get student class
        # print('student')
        obj_student_class = Student.objects.get(id=student)

        #get subject class
        # print('subject')
        obj_subject_class = Subject.objects.get(id=subject)

        #get teacher class
        # print('teacher')
        # print(teacher)
        obj_teacher_class = Teacher.objects.get(id=teacher)
        # print(obj_teacher_class)
        
        sec_title = title1,
        sec_titre = titre1,
        # sec_value = value_two,

        
        eval.title = title
        eval.titre = titre
        eval.value = value
        eval.sec_title = sec_title
        eval.sec_titre = sec_titre
        eval.sec_value = value_two
        eval.coef = coef
        eval.subject = obj_subject_class
        eval.observation = remarks
        eval.student = obj_student_class
        eval.teacher = obj_teacher_class.name
        eval.teacher_class = obj_teacher_class
        eval.modified_by = request.user.username
        eval.seqone_is_absent =  absent_one
        eval.seqtwo_is_absent = absent_two
        eval.save()
      
        messages.success(request, f'{obj_student_class.name}--{eval.title}-- {obj_subject_class.title} --- Updated Successfully')
        return redirect("test_list")
    return render(request, "eval/edit-eval.html", context )





@login_required
def delete_test(request, slug):
    if request.method == "POST":
        #
        eval = get_object_or_404(Eval, id = slug)
        eval.delete()

        return redirect('test_list')
    return HttpResponseForbidden()



#report card
@login_required
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
    if marks >= 0.00 and marks < 5.00:
        return "WEAK"
    if marks >= 5.00 and marks < 8.00:
        return "POOR"
    if marks >= 8.00 and marks < 10.00:
        return "BELOW AVERAGE"
    if marks == 10.00:
        return "FAIRLY GOOD"
    if marks > 10.00 and marks < 12.00:
        return "AVERAGE"
    if marks >= 12.00 and marks < 15.00:
        return "GOOD"
    if marks >= 15.00 and marks < 17.00:
        return "VERY GOOD"
    if marks >= 17.00 and marks < 20.00:
        return "EXCELLENT"


#grade
def grade_marks(marks):
    if marks >= 0.00 and marks < 5.00:
        return "F"
    if marks >= 5.00 and marks < 8.00:
        return "E"
    if marks >= 8.00 and marks < 10.00:
        return "D"
    if marks == 10.00:
        return "C"
    if marks > 10.00 and marks < 12.00:
        return "C+"
    if marks >= 12.00 and marks < 15.00:
        return "B"
    if marks >= 15.00 and marks < 17.00:
        return "B+"
    if marks >= 17.00 and marks < 20.00:
        return "A"

@login_required
def stud_cal_mark(request):
    current_aced_year = "2024/2025"
    subjects = Subject.objects.all()
    student_all = Student.objects.filter(is_actif=True)
    # print(student_all)
    context = {
        'students':student_all,
    }
    # print(context)
    if request.method == "POST":
        try:
            student_in = request.POST.get('student_in')
            print(student_in)
            # students = Student.objects.filter(is_actif=True, name=student_in).first()
            students = Student.objects.filter( name=student_in).first()
            print(f"{students}---students")
            term = request.POST.get('term')
            added_by = request.user.username
            get_class = students.student_class
            print(f"{get_class}---get_class")
        except:
            # print("out")
            messages.error(request, 'Something went wrong')
            return redirect('cal_stud_marks')
        
        # 
        if students:
            does_stud_has_test = Eval.objects.filter(student_id=students, academic_year=current_aced_year, is_actif=True)
            if does_stud_has_test:
                # 
                subjects = Subject.classroom.through.objects.filter(classroom_id=get_class.id)
                if subjects:
                    for subjs in subjects:
                        subj = Subject.objects.get(id=subjs.subject_id)
                        if term == "second":
                            # print("second")
                            # 
                            get_testa = Eval.objects.filter(title="Test3",student_id=students.id,subject_id = subj.id, academic_year=current_aced_year, is_actif=True).first()
                            # print(get_testa)
                            if get_testa:
                                subj_avg = (get_testa.value + get_testa.sec_value) / 2
                                # 
                                observation = appreciation_marks(subj_avg)
                                grade_tot_subj = subj_avg * get_testa.coef
                                # print(f"subj Average:  --- {subj_avg}--- {subj.title} --- {grade_tot_subj}---- {observation}")
                                current_mark = TestMoySpecialtySubjClass.objects.filter(term=term, classroom =get_class, specialty=students.specialty, student=students, subject=subj, academic_year=current_aced_year, is_actif=True).first()
                                if current_mark:
                                    current_mark.is_actif = False
                                    current_mark.modified_by = request.user.username
                                    current_mark.save()
                                    mark_subj = TestMoySpecialtySubjClass.objects.create(
                                        term = term,
                                        classroom = students.student_class,
                                        specialty = students.specialty,
                                        student = students,
                                        subject = subj,
                                        test_avg = grade_tot_subj,
                                        subj_coef = get_testa.coef,
                                        observation = observation,
                                        added_by = added_by,
                                    )
                                else:
                                    # 
                                    mark_subj = TestMoySpecialtySubjClass.objects.create(
                                        term = term,
                                        classroom = students.student_class,
                                        specialty = students.specialty,
                                        student = students,
                                        subject = subj,
                                        test_avg = grade_tot_subj,
                                        subj_coef = get_testa.coef,
                                        observation = observation,
                                        added_by = added_by,
                                    )
                messages.success(request, f'{students} Marks Calculated successfully')
                return redirect("cal_stud_marks")
            else:
                # print("out")
                messages.error(request, 'Student has not marks')
                return redirect('cal_stud_marks')
    return render(request, "eval/cal_stud_marks.html", context=context)


@login_required
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
    current_aced_year = "2024/2025"

    if request.method == "POST":
        #
        try:
            #geting all required data
            classroom = request.POST.get('classroom')
            term = request.POST.get('term')
            added_by = request.user.username
            # print(added_by)request.user.username
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
        

        # print("classroom")
        # print(classroom)
        if classroom:
            # print("inn class")
            get_class = ClassRoom.objects.get(id = classroom)
            # class_subj = Subject.classroom.classroom_id
            if Student.objects.filter(student_class=get_class).count() > 1:
                # print("class stud")
                class_students = Student.objects.filter(student_class=get_class)
                # print(class_students)
                for student in class_students:
                    does_stud_has_test = Eval.objects.filter(student_id=student.id, academic_year=current_aced_year, is_actif=True)
                    if does_stud_has_test:
                        #
                        # print("has test marks")
                        # print("student")
                        # print(student)
                        # print(subjs)
                        # print(subjs.title)
                        # print("Subject.classroom")
                        # print(Subject.classroom)
                        # print("Subject.classroom.classroom_id")
                        # print(Subject.classroom.through.objects.all())
                        #
                        # subjects = Subject.classroom.through.objects.all()
                        subjects = Subject.classroom.through.objects.filter(classroom_id=classroom)
                        
                        if subjects:
                            # print("in sub")
                            # print(subjects)
                            
                            for subjs in subjects:
                                subj = Subject.objects.get(id=subjs.subject_id)
                                # if subjs.subject_id == 74:
                                    
                                    # print(f"subject 74 is------------------{subj.title}")
                                # subj = Subject.objects.get(id=subjs.subject_id)
                                # print("subjs")
                                # print(subj)
                                # print(f"subject {subj}--- with it {subj.id}")
                                # print(f"subject {subj}--- with it {subjs.subject_id}")
                                # print(subj)
                                # print('studt')
                                # print(student)
                                if term == "first":
                                    # print("first")
                                    # 
                                    # print(student_test.title)
                                    # get_testa_subj = Eval.objects.filter(title="Test1",student_id=student.id,subject_id = subj.id, academic_year=current_aced_year)
                                    get_testa = Eval.objects.filter(title="Test1",student_id=student.id,subject_id = subj.id, academic_year=current_aced_year, is_actif=True).first()
                                    # print(get_testa)
                                    if get_testa:
                                        # print("we here")
                                        # print(f"test {get_testa.title}--- test1 {get_testa.value} --- test2: {get_testa.sec_value} with it {subjs.subject_id} subject {subj}--- with it {subjs.subject_id}")
                                        # print(f"test {get_testa.title}--- with it {subjs.subject_id}")
                                        # print(f"test1: {get_testa.value} --- test2: {get_testa.sec_value}")
                                        # test1_val = decimal.Decimal(0.00)
                                        # test2_val = decimal.Decimal(0.00)
                                        # if get_testa.sec_value:
                                        #     test2_val = get_testa.sec_value
                                        # if get_testa.value:
                                        #     test1_val = get_testa.value
                                        # subj_avg = (test1_val + test2_val) / 2
                                        subj_avg = (get_testa.value + get_testa.sec_value) / 2
                                        # 
                                        observation = appreciation_marks(subj_avg)
                                        # print(f"subj Average:  --- {subj_avg}--- {subj.title}---- {observation}")
                                        grade_tot_subj = subj_avg * get_testa.coef
                                        # print(f"subj Average:  --- {subj_avg}--- {subj.title} --- {grade_tot_subj}---- {observation}")
                                        # current_cal_marks = TestMoySpecialtySubjClass.objects.filter(term=term, classroom =classroom, specialty=student.specialty, student=student, subject=subj, is_actif=True)
                                        current_mark = TestMoySpecialtySubjClass.objects.filter(term=term, classroom =classroom, specialty=student.specialty, student=student, subject=subj, is_actif=True).first()
                                        if current_mark:
                                            current_mark.is_actif = False
                                            current_mark.modified_by = request.user.username
                                            current_mark.save()
                                            mark_subj = TestMoySpecialtySubjClass.objects.create(
                                                term = term,
                                                classroom = student.student_class,
                                                specialty = student.specialty,
                                                student = student,
                                                subject = subj,
                                                test_avg = grade_tot_subj,
                                                subj_coef = get_testa.coef,
                                                observation = observation,
                                                added_by = added_by,
                                            )
                                            # for current_mark in current_cal_marks:
                                            #     # print(current_mark)
                                            #     # print(current_mark.is_actif)  
                                            #     current_mark.is_actif = False
                                            #     current_mark.modified_by = request.user.username
                                            #     current_mark.save()
                                                # mark_subj = TestMoySpecialtySubjClass.objects.create(
                                                #     term = term,
                                                #     classroom = student.student_class,
                                                #     specialty = student.specialty,
                                                #     student = student,
                                                #     subject = subj,
                                                #     test_avg = grade_tot_subj,
                                                #     subj_coef = get_testa.coef,
                                                #     observation = observation,
                                                #     added_by = added_by,
                                                # )
                                        else:
                                            # 
                                            mark_subj = TestMoySpecialtySubjClass.objects.create(
                                                term = term,
                                                classroom = student.student_class,
                                                specialty = student.specialty,
                                                student = student,
                                                subject = subj,
                                                test_avg = grade_tot_subj,
                                                subj_coef = get_testa.coef,
                                                observation = observation,
                                                added_by = added_by,
                                            )

                                        # if mark_subj:
                                        #     # good
                                        #     messages.success(request, f'Test Average per Subject Created Successfully')
                                        #     return redirect("calculate_mark_class")
                                        # else:
                                        #     # erreur
                                        #     messages.error(request, f'An error occurred during creation')
                                        #     return redirect("calculate_mark_class")
                                    
                                    # if get_testa_subj:
                                    #     print("get_testa_subj innnnnnn")
                                    #     print(get_testa_subj)
                                    # #     # 
                                    # #     for test_marks in get_testa_subj:
                                    # #         #
                                    #         print(f"test {test_marks.title}--- with it {subjs.subject_id}")
                                    #         print(f"test1: {test_marks.value} --- test2: {test_marks.sec_value}")
                                    # #         subj_avg = (test_marks.value + test_marks.sec_value) / 2
                                    #         print(f"subj Average:  --- {subj_avg}--- {subj.title} ")
                                    
                                if term == "second":
                                    # print("second")
                                    # 
                                    get_testa = Eval.objects.filter(title="Test3",student_id=student.id,subject_id = subj.id, academic_year=current_aced_year, is_actif=True).first()
                                    # print(get_testa)
                                    if get_testa:
                                        subj_avg = (get_testa.value + get_testa.sec_value) / 2
                                        # 
                                        observation = appreciation_marks(subj_avg)
                                        grade_tot_subj = subj_avg * get_testa.coef
                                        # print(f"subj Average:  --- {subj_avg}--- {subj.title} --- {grade_tot_subj}---- {observation}")
                                        current_mark = TestMoySpecialtySubjClass.objects.filter(term=term, classroom =classroom, specialty=student.specialty, student=student, subject=subj, academic_year=current_aced_year, is_actif=True).first()
                                        if current_mark:
                                            current_mark.is_actif = False
                                            current_mark.modified_by = request.user.username
                                            current_mark.save()
                                            mark_subj = TestMoySpecialtySubjClass.objects.create(
                                                term = term,
                                                classroom = student.student_class,
                                                specialty = student.specialty,
                                                student = student,
                                                subject = subj,
                                                test_avg = grade_tot_subj,
                                                subj_coef = get_testa.coef,
                                                observation = observation,
                                                added_by = added_by,
                                            )
                                        else:
                                            # 
                                            mark_subj = TestMoySpecialtySubjClass.objects.create(
                                                term = term,
                                                classroom = student.student_class,
                                                specialty = student.specialty,
                                                student = student,
                                                subject = subj,
                                                test_avg = grade_tot_subj,
                                                subj_coef = get_testa.coef,
                                                observation = observation,
                                                added_by = added_by,
                                            )
                                    
                                if term == "third":
                                    # print("third")
                                    # 
                                    get_testa = Eval.objects.filter(title="Test5",student_id=student.id,subject_id = subj.id, academic_year=current_aced_year, is_actif=True).first()
                                    # print(get_testa)
                                    if get_testa:
                                        subj_avg = (get_testa.value + get_testa.sec_value) / 2
                                        # 
                                        observation = appreciation_marks(subj_avg)
                                        grade_tot_subj = subj_avg * get_testa.coef
                                        # print(f"subj Average:  --- {subj_avg}--- {subj.title} --- {grade_tot_subj}---- {observation}")
                                        current_mark = TestMoySpecialtySubjClass.objects.filter(term=term, classroom =classroom, specialty=student.specialty, student=student, subject=subj, is_actif=True).first()
                                        if current_mark:
                                            current_mark.is_actif = False
                                            current_mark.modified_by = request.user.username
                                            current_mark.save()
                                            mark_subj = TestMoySpecialtySubjClass.objects.create(
                                                term = term,
                                                classroom = student.student_class,
                                                specialty = student.specialty,
                                                student = student,
                                                subject = subj,
                                                test_avg = grade_tot_subj,
                                                subj_coef = get_testa.coef,
                                                observation = observation,
                                                added_by = added_by,
                                            )
                                        else:
                                            # 
                                            mark_subj = TestMoySpecialtySubjClass.objects.create(
                                                term = term,
                                                classroom = student.student_class,
                                                specialty = student.specialty,
                                                student = student,
                                                subject = subj,
                                                test_avg = grade_tot_subj,
                                                subj_coef = get_testa.coef,
                                                observation = observation,
                                                added_by = added_by,
                                            )

                        # else:
                        #     # no student
                        #     messages.error(request, f'NO STUDENT')
                        #     return redirect("calculate_mark_class")
                    # else:
                    #     # no subj
                    #     messages.error(request, f'NO STUDENT HAS NO TEST')
                    #     return redirect("calculate_mark_class")

            elif Student.objects.filter(student_class=get_class).count() == 1:
                # one student
                # print("one student")
                class_students = Student.objects.filter(student_class=get_class)
                # print(class_students)
            else:
                # no student
                messages.error(request, f'NO STUDENT')
                return redirect("calculate_mark_class")


        messages.success(request, f'Classroom {classroom} Marks Calculated successfully')
        return redirect("calculate_mark_class")
        
        # if students:
        #     # print("in in")
        #     # print(Student.objects.filter(student_class=get_class).count())
        #     if Student.objects.filter(student_class=get_class).count() > 1:
        #         #loop through the students and get their marks
        #         # obj_eval_class = Eval.objects.filter(student_id=studentId)
        #         # print(students)
                # print("many stud")
        #         for student in students:
        #             # print(student)
                    # print("many stud, in stud")
        #             subjects = Subject.objects.all()
        #             for subject in subjects:
                        # print("many stud in stud in subj")
        #                 if term == "first":
                            # print("first")
        #                     # print(student_test.title)
        #                     get_testa_subj = Eval.objects.filter(student_id=student.id,subject_id = subject.id)
        #                     if get_testa_subj:
                                # print("get_testa_subj")
                                # print(get_testa_subj)
        #         messages.success(request, f'OK NO GOOD')
        #         return redirect("calculate_mark_class")
        #                         # print(get_testa_subj)
        #                         # total = get_testa_subj.aggregate(s=Sum("value"))["s"]
        #                         # # print(total)
        #                         # if total  >= 0:
        #                         #     # print(subject)
        #                         #     # print('{:0.2f}'.format((total/ 2)* get_testa_subj[0].coef))
        #                         #     get_test = '{:0.2f}'.format((total/ 2)* get_testa_subj[0].coef)
        #                         #     observation = appreciation_marks((total/ 2))
        #                         #     # print(observation)
        #                         #     current_cal_marks = get_cal_marks.filter(term=term, classroom =student.student_class, specialty=student.specialty, student=student, subject=subject, is_actif=True)
        #                         #     if current_cal_marks:
        #                         #         for current_mark in current_cal_marks:
        #                         #             # print(current_mark)
        #                         #             # print(current_mark.is_actif)  
        #                         #             current_mark.is_actif = False
        #                         #             current_mark.modified_by = request.user.username
        #                         #             current_mark.save()
                                    
        #                         #     mark_subj = TestMoySpecialtySubjClass.objects.create(
        #                         #         term = term,
        #                         #         classroom = student.student_class,
        #                         #         specialty = student.specialty,
        #                         #         student = student,
        #                         #         subject = subject,
        #                         #         test_avg = get_test,
        #                         #         subj_coef = get_testa_subj[0].coef,
        #                         #         observation = observation,
        #                         #         added_by = added_by,
        #                         #     )
        #                 # if term == "second":
        #                 #     # print(student_test.title)
        #                 #     get_testa_subj = Eval.objects.filter(student_id=student.id,subject_id = subject.id)
        #                 #     if get_testa_subj:
                        #         print(get_testa_subj)
        #                 #         total = get_testa_subj.aggregate(s=Sum("value"))["s"]
        #                 #         # print(total)
        #                 #         if total  >= 0:
        #                 #             # print(subject)
        #                 #             # print('{:0.2f}'.format((total/ 2)* get_testa_subj[0].coef))
        #                 #             get_test = '{:0.2f}'.format((total/ 2)* get_testa_subj[0].coef)
        #                 #             observation = appreciation_marks((total/ 2))
        #                 #             # print(observation)
        #                 #             current_cal_marks = get_cal_marks.filter(term=term, classroom =student.student_class, specialty=student.specialty, student=student, subject=subject, is_actif=True)
        #                 #             if current_cal_marks:
        #                 #                 for current_mark in current_cal_marks:
        #                 #                     # print(current_mark)
        #                 #                     # print(current_mark.is_actif)  
        #                 #                     current_mark.is_actif = False
        #                 #                     current_mark.modified_by = request.user.username
        #                 #                     current_mark.save()
                                    
        #                 #             mark_subj = TestMoySpecialtySubjClass.objects.create(
        #                 #                 term = term,
        #                 #                 classroom = student.student_class,
        #                 #                 specialty = student.specialty,
        #                 #                 student = student,
        #                 #                 subject = subject,
        #                 #                 test_avg = get_test,
        #                 #                 subj_coef = get_testa_subj[0].coef,
        #                 #                 observation = observation,
        #                 #                 added_by = added_by,
        #                 #             )
        #                 # if term == "third":
        #                 #     # print(student_test.title)
        #                 #     get_testa_subj = Eval.objects.filter(student_id=student.id,subject_id = subject.id)
        #                 #     if get_testa_subj:
        #                 #         # print(get_testa_subj)
        #                 #         total = get_testa_subj.aggregate(s=Sum("value"))["s"]
        #                 #         # print(total)
        #                 #         if total  >= 0:
        #                 #             # print(subject)
        #                 #             # print('{:0.2f}'.format((total/ 2)* get_testa_subj[0].coef))
        #                 #             get_test = '{:0.2f}'.format((total/ 2)* get_testa_subj[0].coef)
        #                 #             observation = appreciation_marks((total/ 2))
        #                 #             # print(observation)
        #                 #             current_cal_marks = get_cal_marks.filter(term=term, classroom =student.student_class, specialty=student.specialty, student=student, subject=subject, is_actif=True)
        #                 #             if current_cal_marks:
        #                 #                 for current_mark in current_cal_marks:
        #                 #                     # print(current_mark)
        #                 #                     # print(current_mark.is_actif)  
        #                 #                     current_mark.is_actif = False
        #                 #                     current_mark.modified_by = request.user.username
        #                 #                     current_mark.save()
                                    
        #                 #             mark_subj = TestMoySpecialtySubjClass.objects.create(
        #                 #                 term = term,
        #                 #                 classroom = student.student_class,
        #                 #                 specialty = student.specialty,
        #                 #                 student = student,
        #                 #                 subject = subject,
        #                 #                 test_avg = get_test,
        #                 #                 subj_coef = get_testa_subj[0].coef,
        #                 #                 observation = observation,
        #                 #                 added_by = added_by,
        #                 #             )
        #             # #get evaluations of the student based on the term
        #             # obj_tests_class = Eval.objects.filter(student_id=student.id)
        #             # #looping through the tests of a student
        #             # for student_test in obj_tests_class:
        #             #     # print(student_test)
        #             #     if term == "first":
                    #         print(student_test.title)
        #             #     if term == "second":
                    #         print(student_test.title)
        #             #     if term == "third":
                    #         print(student_test.title)
        #     else:
        #         # obj_tests_class = Eval.objects.filter(student_id=students[0].id)
        #         #looping through the tests of a student
        #         for subject in subjects:
                    # print("stud innn")
        #             if term == "first":
                        # print("innnn")
        #                 # print(student_test.title)
        #                 get_testa_subj = Eval.objects.filter(student_id=student.id,subject_id = subject.id)
        #                 if get_testa_subj:
                    #         print("get_testa_subj")
                    #         print(get_testa_subj)
                    # print("done")
        #                 # get_testa_subj = Eval.objects.filter(student_id=students[0].id,subject_id = subject.id)
        #                 # if get_testa_subj:
        #                 #     # print(get_testa_subj)
        #                 #     total = get_testa_subj.aggregate(s=Sum("value"))["s"]
        #                 #     # print(total)
        #                 #     if total >= 0:
        #                 #         # print(subject)
        #                 #         # print('{:0.2f}'.format((total/ 2)* get_testa_subj[0].coef))
        #                 #         get_test = '{:0.2f}'.format((total/ 2)* get_testa_subj[0].coef)
        #                 #         observation = appreciation_marks((total/ 2))
        #                 #         # print(observation)
        #                 #         current_cal_marks = get_cal_marks.filter(term=term, classroom =students[0].student_class, specialty=students[0].specialty, student=students[0], subject=subject, is_actif=True)
        #                 #         if current_cal_marks:
        #                 #             for current_mark in current_cal_marks:
        #                 #                 # print(current_mark)
        #                 #                 # print(current_mark.is_actif)  
        #                 #                 current_mark.is_actif = False
        #                 #                 current_mark.modified_by = request.user.username
        #                 #                 current_mark.save()
                                
        #                 #         mark_subj = TestMoySpecialtySubjClass.objects.create(
        #                 #             term = term,
        #                 #             classroom = students[0].student_class,
        #                 #             specialty = students[0].specialty,
        #                 #             student = students[0],
        #                 #             subject = subject,
        #                 #             test_avg = get_test,
        #                 #             subj_coef = get_testa_subj[0].coef,
        #                 #             observation = observation,
        #                 #             added_by = added_by,
        #                 #         )
        #             # if term == "second":
        #             #     # print(student_test.title)
        #             #     # print(count)
        #             #     # print(subject)
        #             #     get_testa_subj = Eval.objects.filter(student_id=students[0].id,subject_id = subject.id)
        #             #     if get_testa_subj:
        #             #         # print(get_testa_subj)
        #             #         total = get_testa_subj.aggregate(s=Sum("value"))["s"]
        #             #         # print(total)
        #             #         if total >= 0:
        #             #             # print(subject)
        #             #             # print('{:0.2f}'.format((total/ 2)* get_testa_subj[0].coef))
        #             #             get_test = '{:0.2f}'.format((total/ 2)* get_testa_subj[0].coef)
        #             #             observation = appreciation_marks((total/ 2))
        #             #             # print(observation)
        #             #             current_cal_marks = get_cal_marks.filter(term=term, classroom =students[0].student_class, specialty=students[0].specialty, student=students[0], subject=subject, is_actif=True)
        #             #             if current_cal_marks:
        #             #                 for current_mark in current_cal_marks:
                    #                     print(current_mark)
                    #                     print(current_mark.is_actif)  
        #             #                     current_mark.is_actif = False
        #             #                     current_mark.modified_by = request.user.username
        #             #                     current_mark.save()
                                
        #             #             mark_subj = TestMoySpecialtySubjClass.objects.create(
        #             #                 term = term,
        #             #                 classroom = students[0].student_class,
        #             #                 specialty = students[0].specialty,
        #             #                 student = students[0],
        #             #                 subject = subject,
        #             #                 test_avg = get_test,
        #             #                 subj_coef = get_testa_subj[0].coef,
        #             #                 observation = observation,
        #             #                 added_by = added_by,
        #             #             )
        #             # if term == "third":
        #             #     # print(student_test.title)
        #             #     # print(count)
        #             #     # print(subject)
        #             #     get_testa_subj = Eval.objects.filter(student_id=students[0].id,subject_id = subject.id)
        #             #     if get_testa_subj:
        #             #         # print(get_testa_subj)
        #             #         total = get_testa_subj.aggregate(s=Sum("value"))["s"]
        #             #         # print(total)
        #             #         if total >= 0:
                    #             print(subject)
        #             #             # print('{:0.2f}'.format((total/ 2)* get_testa_subj[0].coef))
        #             #             get_test = '{:0.2f}'.format((total/ 2)* get_testa_subj[0].coef)
        #             #             observation = appreciation_marks((total/ 2))
        #             #             # print(observation)
        #             #             current_cal_marks = get_cal_marks.filter(term=term, classroom =students[0].student_class, specialty=students[0].specialty, student=students[0], subject=subject, is_actif=True)
        #             #             if current_cal_marks:
        #             #                 for current_mark in current_cal_marks:
        #             #                     # print(current_mark)
        #             #                     # print(current_mark.is_actif)  
        #             #                     current_mark.is_actif = False
        #             #                     current_mark.modified_by = request.user.username
        #             #                     current_mark.save()
                                
        #             #             mark_subj = TestMoySpecialtySubjClass.objects.create(
        #             #                 term = term,
        #             #                 classroom = students[0].student_class,
        #             #                 specialty = students[0].specialty,
        #             #                 student = students[0],
        #             #                 subject = subject,
        #             #                 test_avg = get_test,
        #             #                 subj_coef = get_testa_subj[0].coef,
        #             #                 observation = observation,
        #             #                 added_by = added_by,
        #             #             )


        #                         # 
        #                     # 
        #                 # 
        #             # 
        #         messages.success(request, f'OK NO GOOD')
        #         return redirect("calculate_mark_class")
        #                 # print('{:0.2f}'.format((total/ 2)* get_testa_subj[0].coef))
                        
        #                 # if student_test.subject_id == subject.id:
                        #     print(f"{student_test.title}------{student_test.value}-----{subject}")
        #                 #     # print(count)
        #                 #     count = count + 1
                        #     print(subject)
        #                 #     get_testa_subj = Eval.objects.filter(student_id=students[0].id,subject_id = subject.id)
        #                 #     total = get_testa_subj.aggregate(s=Sum("value"))["s"]
                        #     print('{:0.2f}'.format((total/ 2)* student_test.coef))
        #         # count = 0
        #         # for student_test in obj_tests_class:
        #             ##NEW
        #             # count = 0
        #             # array_for_vals = []
        #             # for subject in subjects:
        #             #     if student_test.subject_id == subject.id:
        #             #         count = count + 1
                    #         print(student_test.subject_id)
        #             #         # if student_test.title == "Test3":
                    #         #     print(student_test.title)
        #                     # array_for_vals.append([student_test.subject_id, subject.title, student_test.value, students[0].name])
        #                     # array_for_vals.append(f"{student_test.subject_id}_{subject.title}_{student_test.value}_{students[0].name}")
        #             # print(array_for_vals)
        #             # print(array_for_vals[0][1])
        #             # for array_for_val in array_for_vals:
        #             #     # print(array_for_val)
        #             #     for subject in subjects:
        #             #         if array_for_vals[0][0] == subject.id:
                    #             print(subject)
        #             ##OLD
        #             # if term == "first":
                    #     print(student_test.title)
        #             # if term == "second":
        #             #     # print(student_test.title)
        #             #     count = 0
        #             #     get_testa_stud = ""
        #             #     get_testb_stud = ""
        #             #     for subject in subjects:
        #             #         # print(count)
                            
        #             #         if student_test.subject_id == subject.id:
                    #             print(f"{student_test.title}------{student_test.value}-----{subject}")
        #             #             # print(count)
        #             #             count = count + 1
                    #             print(subject)
        #             #             get_testa_subj = Eval.objects.filter(student_id=students[0].id,subject_id = subject.id)
        #             #             total = get_testa_subj.aggregate(s=Sum("value"))["s"]
                    #             print('{:0.2f}'.format((total/ 2)* student_test.coef))
        #                         # if student_test.title == "Test3":
        #                         #     count = count + 1
        #                         #     # print(count)
        #                         #     get_testa = student_test.value
        #                         # if student_test.title == "Test4":
        #                         #     count = count + 1
        #                         #     # print(count)
        #                         #     get_testb = student_test.value
        #                         # print(count)
        #                         # if count == 2 and (get_testb > 0.0 and get_testa > 0.0):
        #                         #     get_test = ((get_testa + get_testb) / 2) * student_test.coef
                                #     print(f"{get_test}------{students[0]}")
        #                     # get_testa_subj = Eval.objects.filter(student_id=students[0].id,subject_id = subject.id, title = "Test3")
        #                     # print(get_testa_subj)
        #                     # if get_testa_subj:
                            #     print(get_testa_subj)
        #                     #     get_testa = get_testa_subj.value
        #                     # if student_test.title == "Test3":
        #                     #     get_testa = student_test.value
        #                     #     get_testa_stud = student_test.student_id
                            #     print(student_test.student_id)
        #                     # if student_test.title == "Test4":
        #                     #     get_testb = student_test.value
        #                     #     get_testb_stud = student_test.student_id
        #                     # if get_testa_stud == get_testb_stud:
                            #     print("same student")
        #                     #     get_test = ((get_testa + get_testb) / 2) * student_test.coef
                            #     print(get_test)
        #                     # print(subject)
        #                     # print(student_test.subject_id)
        #                     # print(subject.id)
        #                     # if student_test.title == "Test3":
        #                     #     get_testa = student_test.value
        #                     #     if student_test.subject_id == subject.id:
                            #         print("Test3")
                            #         print(get_testa)
        #                     #         get_test = ((get_testa + get_testb) / 2) * student_test.coef
                            #         print(get_test)
                            #         print(subject)
        #                     # if student_test.title == "Test4":
        #                     #     get_testb = student_test.value
        #                     #     # print("Test4")
        #                     #     # print(get_testb)
        #                     #     if student_test.subject_id == subject.id:
                            #         print("Test4")
                            #         print(get_testb)
        #                     #         get_test = ((get_testa + get_testb) / 2) * student_test.coef
                            #         print(get_test)
                            #         print(subject)
        #                     #     # print(get_test)
        #                     #     # print(students[0])
        #                     #     # print(students[0].student_class)
        #                     #     # print(students[0].specialty)
        #                     #     observation = appreciation_marks(get_testa)
        #                         #
        #                         ####
        #                         # if get_testb > 0.0 and get_testa > 0.0:
        #                         #     get_test = ((get_testa + get_testb) / 2) * student_test.coef
        #                         #     # print("info")
                                #     print(subject)
        #                         #     # print(get_test)
        #                         #     # print(students[0])
        #                         #     # print(students[0].student_class)
        #                         #     # print(students[0].specialty)
        #                         #     observation = appreciation_marks(get_testa)
        #                             # print(observation)

        #                             # current_cal_marks = get_cal_marks.filter(term="second", classroom =students[0].student_class, specialty=students[0].specialty, student=students[0], subject=subject, is_actif=True)
        #                             # if current_cal_marks:
        #                             #     for current_mark in current_cal_marks:
                                    #         print(current_mark)
                                    #         print(current_mark.is_actif)  
        #                             #         current_mark.is_actif = False
        #                             #         current_mark.modified_by = request.user.username
        #                             #         current_mark.save()
                                    
        #                             # mark_subj = TestMoySpecialtySubjClass.objects.create(
        #                             #     term = term,
        #                             #     classroom = students[0].student_class,
        #                             #     specialty = students[0].specialty,
        #                             #     student = students[0],
        #                             #     subject = subject,
        #                             #     test_avg = get_test,
        #                             #     observation = observation,
        #                             #     added_by = added_by,
        #                             # )
        #                 # print(count)

        #                 # messages.success(request, 'Subject Marks added Successfully')
        #                 # return redirect("calculate_mark_class")

                                
        #             # if term == "third":
                    #     print(student_test.title)

        #             # print(student_test)
                            
                        
        # else:
        #     messages.error(request, 'No Student')
        #     return redirect('calculate_mark_class')
        

    

    return render(request, "eval/call-results-class.html", context=context)


# def ranking(self, *args, **kwargs): 
#     marks = ClassRanking.objects.all().values_list('specialty', flat=True).order_by('-total_avg') 
#     rank = list(marks).index(self) 
#     return rank

@login_required
def delete_report_card(request, slug):
    if request.method == "POST":
        #
        report_card = get_object_or_404(ReportCard, id = slug)
        student_name =  report_card.student.name
        report_card.delete()

        messages.success(request, f'{student_name} Record card Deleted')

        return redirect('report_cards')
    return HttpResponseForbidden()

@login_required
def all_classrank(request):
    testmoyspesubclass = TestMoySpecialtySubjClass.objects.all()
    get_class_rankings = ClassRanking.objects.filter(is_actif=True)
    context = {
        'testmoy': testmoyspesubclass,
        'class_rankings':get_class_rankings,
    }
    return render(request, "eval/call-classranks.html", context=context)

@login_required
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
    current_academic_year = "2024/2025"




    if request.method == "POST":
        # print("in post")
        total_coef = 0.00
        get_classrooms = request.POST.get('get_classrooms')
        # print(get_classrooms)
        cur_term = request.POST.get('cur_term')
        # print(cur_term)

        if get_classrooms:
            # print("in get_classrooms")
            #
            #get all student in the class
            students_call = Student.objects.filter(student_class_id = get_classrooms)
            if students_call:
                # print("stud")
                for student in students_call:
                    if cur_term == "first":
                        # print("in first")
                        get_testa_subj = TestMoySpecialtySubjClass.objects.filter(term=cur_term,classroom_id=get_classrooms,student_id=student.id,is_actif = True)
                        # print(get_testa_subj)
                        # get total coeff
                        if get_testa_subj:
                            # print("in gg")
                            # print(get_testa_subj)
                            total_coef = get_testa_subj.aggregate(tot_coeff=Sum('subj_coef'))
                            total_testavg = get_testa_subj.aggregate(tot_testavg=Sum('test_avg'))
                            # print("tot coef")
                            # print(total_coef)
                            # print(total_coef.get("tot_coeff"))
                            tt_coeff = total_coef.get("tot_coeff")
                            # print("tot testavg")
                            # print(total_testavg)
                            # print(total_testavg.get("tot_testavg"))
                            tot_testavg = total_testavg.get("tot_testavg")
                            student_avg = float('{:0.2f}'.format(tot_testavg  / tt_coeff))
                            avg_observatn = appreciation_marks(student_avg)
                            # print(f"{total_coef}-----{total_testavg}---{student_avg}--of specialty:{student.specialty.name}--thus {avg_observatn}")
                            current_class_rankxs = ClassRanking.objects.filter(term=cur_term, classroom =student.student_class, specialty_id=student.specialty.id, student=student, academic_year=current_academic_year, is_actif=True)
                            if current_class_rankxs:
                                for class_rankx in current_class_rankxs:
                                    # print(class_rankx)
                                    # print(class_rankx.is_actif)  
                                    class_rankx.is_actif = False
                                    class_rankx.modified_by = request.user.username
                                    class_rankx.save()
                                    class_ranking = ClassRanking.objects.create(
                                        term = cur_term,
                                        classroom = student.student_class,
                                        specialty = student.specialty,
                                        total_coeff = tt_coeff,
                                        total_marks = tot_testavg,
                                        total_avg = student_avg,
                                        observation = avg_observatn,
                                        student = student,
                                        added_by = request.user.username,
                                    )
                            else:
                                class_ranking = ClassRanking.objects.create(
                                    term = cur_term,
                                    classroom = student.student_class,
                                    specialty = student.specialty,
                                    total_coeff = tt_coeff,
                                    total_marks = tot_testavg,
                                    total_avg = student_avg,
                                    observation = avg_observatn,
                                    student = student,
                                    added_by = request.user.username,
                                )
                    if cur_term == "second":
                        # print("in second")
                        get_testa_subj = TestMoySpecialtySubjClass.objects.filter(term=cur_term,classroom_id=get_classrooms,student_id=student.id, academic_year=current_academic_year, is_actif = True)
                        #
                        if get_testa_subj:
                            # print("in gg")
                            # print(get_testa_subj)
                            total_coef = get_testa_subj.aggregate(tot_coeff=Sum('subj_coef'))
                            total_testavg = get_testa_subj.aggregate(tot_testavg=Sum('test_avg'))
                            tt_coeff = total_coef.get("tot_coeff")
                            tot_testavg = total_testavg.get("tot_testavg")
                            student_avg = float('{:0.2f}'.format(tot_testavg  / tt_coeff))
                            avg_observatn = appreciation_marks(student_avg)
                            # print(f"{total_coef}-----{total_testavg}---{student_avg}--of specialty:{student.specialty.name}--thus {avg_observatn}")
                            current_class_rankxs = ClassRanking.objects.filter(term=cur_term, classroom =student.student_class, specialty_id=student.specialty.id, student=student, academic_year=current_academic_year, is_actif=True)
                            if current_class_rankxs:
                                for class_rankx in current_class_rankxs:
                                    # print(class_rankx)
                                    # print(class_rankx.is_actif)  
                                    class_rankx.is_actif = False
                                    class_rankx.modified_by = request.user.username
                                    class_rankx.save()
                                    class_ranking = ClassRanking.objects.create(
                                        term = cur_term,
                                        classroom = student.student_class,
                                        specialty = student.specialty,
                                        total_coeff = tt_coeff,
                                        total_marks = tot_testavg,
                                        total_avg = student_avg,
                                        observation = avg_observatn,
                                        student = student,
                                        added_by = request.user.username,
                                    )
                            else:
                                class_ranking = ClassRanking.objects.create(
                                    term = cur_term,
                                    classroom = student.student_class,
                                    specialty = student.specialty,
                                    total_coeff = tt_coeff,
                                    total_marks = tot_testavg,
                                    total_avg = student_avg,
                                    observation = avg_observatn,
                                    student = student,
                                    added_by = request.user.username,
                                )
                    if cur_term == "third":
                        # print("in third")
                        get_testa_subj = TestMoySpecialtySubjClass.objects.filter(term=cur_term,classroom_id=get_classrooms,student_id=student.id,is_actif = True)
                        #
                        if get_testa_subj:
                            # print("in gg")
                            # print(get_testa_subj)
                            total_coef = get_testa_subj.aggregate(tot_coeff=Sum('subj_coef'))
                            total_testavg = get_testa_subj.aggregate(tot_testavg=Sum('test_avg'))
                            tt_coeff = total_coef.get("tot_coeff")
                            tot_testavg = total_testavg.get("tot_testavg")
                            student_avg = float('{:0.2f}'.format(tot_testavg  / tt_coeff))
                            avg_observatn = appreciation_marks(student_avg)
                            # print(f"{total_coef}-----{total_testavg}---{student_avg}--of specialty:{student.specialty.name}--thus {avg_observatn}")
                            current_class_rankxs = ClassRanking.objects.filter(term=cur_term, classroom =student.student_class, specialty_id=student.specialty.id, student=student, academic_year=current_academic_year, is_actif=True)
                            if current_class_rankxs:
                                for class_rankx in current_class_rankxs:
                                    # print(class_rankx)
                                    # print(class_rankx.is_actif)  
                                    class_rankx.is_actif = False
                                    class_rankx.modified_by = request.user.username
                                    class_rankx.save()
                                    class_ranking = ClassRanking.objects.create(
                                        term = cur_term,
                                        classroom = student.student_class,
                                        specialty = student.specialty,
                                        total_coeff = tt_coeff,
                                        total_marks = tot_testavg,
                                        total_avg = student_avg,
                                        observation = avg_observatn,
                                        student = student,
                                        added_by = request.user.username,
                                    )
                            else:
                                class_ranking = ClassRanking.objects.create(
                                    term = cur_term,
                                    classroom = student.student_class,
                                    specialty = student.specialty,
                                    total_coeff = tt_coeff,
                                    total_marks = tot_testavg,
                                    total_avg = student_avg,
                                    observation = avg_observatn,
                                    student = student,
                                    added_by = request.user.username,
                                )
        messages.success(request, f'{get_classrooms} Class Ranking Calculated Successfully')
        return redirect("classranking_class")

    

        # # for classroom in classrooms:
        # #     #get students
        # #     for student in students:
        # #         if student.student_class.id == classroom.id:
        #             print(classroom.class_name)
        #             print(student.specialty.name)
        # #             #subjects marks
        # #             for subject_marks in totalmarks_subject:
        # #                 if subject_marks.is_actif == True:
        # #                     # print(subject_marks.term)
        # #                     #loop through subjects
        # #                     for subject in subjects:
        # #                         if subject_marks.subject_id == subject.id:
        #                             print(subject.title)

        # # count = 0
            
        # if students:
            # print("in in")
        #     # loop thro students
        #     for student in students:
        #         get_coef = 0.0
        #         for classroom in classrooms:
        #             # print(classroom)

        #             #loop through subjects
        #             # for subject in subjects:
        #                 # print(f"{student.name}--{subject.title}--{subject_marks.specialty}--{subject_marks.test_avg}--{subject.coef}")
        #                 #
        #             # get_coef = subject.coef
        #             # print(f"{student.name}--")
        #             get_testa_subj = TestMoySpecialtySubjClass.objects.filter(classroom_id=classroom.id,student_id=student.id,is_actif = True)
        #             # print(f"{get_testa_subj}--{get_testa_subj}")
        #             # for get_tt in get_testa_subj:
                    #     print(f"{get_tt.subject.title}--{get_tt.subj_coef}")
                    # print("get_testa_subj")
                    # print(get_testa_subj)
        #             if get_testa_subj:
                        # print("get_testa_subj")
                        # print(get_testa_subj)
        #                 #total marks
        #                 # total_test = get_testa_subj.aggregate(s=Sum("test_avg"))["s"]
        #                 # # print(total_test)
        #                 # #total coef
        #                 # total_coef = get_testa_subj.aggregate(s=Sum("subj_coef"))["s"]
        #                 # # print(total_coef)
        #                 # # print(get_testa_subj[0].specialty.name)
        #                 # # print(get_testa_subj[0].term)
        #                 # # print(get_testa_subj[0].classroom.class_name)
        #                 # total_moy = '{:0.2f}'.format(total_test / total_coef) 
        #                 # # print(total_moy)
        #                 # print(student.name)
        #                 # current_class_rankxs = get_class_rankxs.filter(term=get_testa_subj[0].term, classroom =student.student_class, specialty=get_testa_subj[0].specialty, student=student, is_actif=True)
        #                 # if current_class_rankxs:
        #                 #     for class_rankx in current_class_rankxs:
                        #         print(class_rankx)
                        #         print(class_rankx.is_actif)  
        #                 #         class_rankx.is_actif = False
        #                 #         class_rankx.modified_by = request.user.username
        #                 #         class_rankx.save()
                        
        #                 # class_ranking = ClassRanking.objects.create(
        #                 #     term = get_testa_subj[0].term,
        #                 #     classroom = student.student_class,
        #                 #     specialty = get_testa_subj[0].specialty,
        #                 #     total_coeff = total_coef,
        #                 #     total_marks = total_test,
        #                 #     total_avg = total_moy,
        #                 #     student = student,
        #                 #     added_by = request.user.username,
        #                 # )
                


        # # for subject_marks in totalmarks_subject:
        # #     if subject_marks.is_actif == True:
        # #         # print(subject_marks.term)
        # #         #array of student and coef
        # #         arr_stud_coef = []
        # #         # loop thro students
        # #         for student in students:
        # #             get_coef = 0.0
        # #             if student.id == subject_marks.student_id:

        # #                 #loop through subjects
        # #                 for subject in subjects:
        # #                     if subject_marks.subject_id == subject.id:
        #                         print(f"{student.name}--{subject.title}--{subject_marks.specialty}--{subject_marks.test_avg}--{subject.coef}")
        # #                         #
        # #                         get_coef = subject.coef
        #                 # print(get_coef)
        
        # #NB
        # # Of course you can do it in one SQL query. Generating this query using django ORM is also easily achievable.
        # # top_scores = (myModel.objects
        # #                     .order_by('-score')
        # #                     .values_list('score', flat=True)
        # #                     .distinct())
        # # top_records = (myModel.objects
        # #                     .order_by('-score')
        # #                     .filter(score__in=top_scores[:10]))



        # #- before column name mean "descending order", while without - mean "ascending".
        # #order be decending order
        # get_class_rankings = ClassRanking.objects.filter(is_actif=True).order_by('-total_avg')
        # # ranking(get_class_rankings)
        # # rankings = ClassRanking.objects.filter(is_actif=True).annotate(
        # #         rank=Window(
        # #             expression=Rank(),
        # #             order_by=F('total_avg').desc()
        # #         ),
        # #     )
        # # print(rankings)
        # # rank = 1
        # # previous = None
        # # entries = list(get_class_rankings)
        # # previous = entries[0]
        # # previous.rank = 1
        # # for i, entry in enumerate(entries[1:]):
        # #     if entry.total_avg != previous.total_avg:
        # #         rank = i + 2
        # #         entry.rank = str(rank)
        # #     else:
        # #         entry.rank = "%s=" % rank
        # #         previous.rank = entry.rank
        # #     previous = entry
        #     print(rank)
    
                    
    context = {
        'classrooms':classrooms,
    }
    return render(request, "eval/add_classrankx.html", context=context)



@login_required
def rankx_all(request):
    # print("inn")
    rankings = SchoolClasRanking.objects.filter(is_actif=True)
    context = {
        'rankings':rankings,
    }
    return render(request, "eval/all_rankx.html", context=context)




@login_required
def rankx_add(request):
    # print("inn")
    rankings = SchoolClasRanking.objects.filter(is_actif=True)
    classrooms = ClassRoom.objects.filter(is_actif=True)
    current_academic_year = "2024/2025"
    context = {
        'rankings':rankings,
        'classrooms':classrooms,
    }
    # .objects.values('parameter_id').annotate(max_time_stamp=Max('time_stamp'))
    if request.method == "POST":
        # print('in post')
        term = request.POST.get('cur_term')
        get_classrooms = request.POST.get('get_classrooms')
        # get all specialties
        all_specialties = Specialty.objects.filter(is_actif=True)
        if get_classrooms:
            selected_class = ClassRoom.objects.get(id=get_classrooms)
            # print(selected_class)
            if term:
                if term == "first":
                    # print("first")
                    max_spec = ClassRanking.objects.aggregate(Max('total_avg'))
                    # print(max_spec)
                    # loop thro specialties
                    for specialt in all_specialties:
                        # print("get_classrooms")
                        # print(get_classrooms)
                        # print("specialt")
                        # print(specialt)
                        avg_spec = ClassRanking.objects.filter(classroom_id=get_classrooms,specialty=specialt, is_actif=True, academic_year=current_academic_year).order_by('-total_avg')
                        # print("avg_spec")
                        # print(avg_spec)
                        if avg_spec:
                            forcounter = 0
                            for avg_rank in avg_spec:
                                forcounter = forcounter + 1
                                # if forcounter == 1:
                                    # print(f"first is {avg_rank}")
                                # if forcounter == 2:
                                    # print(f"second is {avg_rank}")
                                # check if spec class rank exits already
                                chec_rank = SchoolClasRanking.objects.filter(academic_year=current_academic_year,spec_rank=forcounter,classroom=selected_class,specialty=specialt, is_actif=True).first()
                                if chec_rank:
                                    
                                    # print("record exits")
                                    chec_rank.is_actif = False
                                    chec_rank.modified_by = request.user.username
                                    chec_rank.save()
                                    spec_class_rank = SchoolClasRanking.objects.create(
                                        term = term,
                                        student_avg = avg_rank.total_avg,
                                        observation = avg_rank.observation,
                                        academic_year=current_academic_year,
                                        spec_rank=forcounter,
                                        added_by = request.user.username,
                                        classroom=selected_class,
                                        specialty=specialt,
                                        student = avg_rank.student,
                                    )
                                else:
                                    # print("record don't exit")
                                # spec_class_rank =
                                    spec_class_rank = SchoolClasRanking.objects.create(
                                        term = term,
                                        student_avg = avg_rank.total_avg,
                                        observation = avg_rank.observation,
                                        academic_year=current_academic_year,
                                        spec_rank=forcounter,
                                        added_by = request.user.username,
                                        classroom=selected_class,
                                        specialty=specialt,
                                        student = avg_rank.student,
                                    )

                                    
                if term == "second":
                    # print("second")
                    max_spec = ClassRanking.objects.aggregate(Max('total_avg'))
                    # print(max_spec)
                    # loop thro specialties
                    for specialt in all_specialties:
                        avg_spec = ClassRanking.objects.filter(classroom_id=get_classrooms,specialty=specialt, is_actif=True, academic_year=current_academic_year).order_by('-total_avg')
                        # 
                        if avg_spec:
                            forcounter = 0
                            for avg_rank in avg_spec:
                                forcounter = forcounter + 1
                                # check if spec class rank exits already
                                chec_rank = SchoolClasRanking.objects.filter(academic_year=current_academic_year,spec_rank=forcounter,classroom=selected_class,specialty=specialt, is_actif=True).first()
                                if chec_rank:
                                    # print("record exits")
                                    chec_rank.is_actif = False
                                    chec_rank.modified_by = request.user.username
                                    chec_rank.save()
                                    spec_class_rank = SchoolClasRanking.objects.create(
                                        term = term,
                                        student_avg = avg_rank.total_avg,
                                        observation = avg_rank.observation,
                                        academic_year=current_academic_year,
                                        spec_rank=forcounter,
                                        added_by = request.user.username,
                                        classroom=selected_class,
                                        specialty=specialt,
                                        student = avg_rank.student,
                                    )
                                else:
                                    # print("record don't exit")
                                    # spec_class_rank =
                                    spec_class_rank = SchoolClasRanking.objects.create(
                                        term = term,
                                        student_avg = avg_rank.total_avg,
                                        observation = avg_rank.observation,
                                        academic_year=current_academic_year,
                                        spec_rank=forcounter,
                                        added_by = request.user.username,
                                        classroom=selected_class,
                                        specialty=specialt,
                                        student = avg_rank.student,
                                    )
                if term == "third":
                    # print("third")
                    # max_spec = ClassRanking.objects.aggregate(Max('total_avg'))
                    # print(max_spec)
                    # loop thro specialties
                    for specialt in all_specialties:
                        avg_spec = ClassRanking.objects.filter(classroom_id=get_classrooms,specialty=specialt, is_actif=True, academic_year=current_academic_year).order_by('-total_avg')
                        # 
                        if avg_spec:
                            forcounter = 0
                            for avg_rank in avg_spec:
                                forcounter = forcounter + 1
                                # check if spec class rank exits already
                                chec_rank = SchoolClasRanking.objects.filter(academic_year=current_academic_year,spec_rank=forcounter,classroom=selected_class,specialty=specialt, is_actif=True).first()
                                if chec_rank:
                                    # print("record exits")
                                    chec_rank.is_actif = False
                                    chec_rank.modified_by = request.user.username
                                    chec_rank.save()
                                    spec_class_rank = SchoolClasRanking.objects.create(
                                        term = term,
                                        student_avg = avg_rank.total_avg,
                                        observation = avg_rank.observation,
                                        academic_year=current_academic_year,
                                        spec_rank=forcounter,
                                        added_by = request.user.username,
                                        classroom=selected_class,
                                        specialty=specialt,
                                        student = avg_rank.student,
                                    )
                                else:
                                    # print("record don't exit")
                                    # spec_class_rank =
                                    spec_class_rank = SchoolClasRanking.objects.create(
                                        term = term,
                                        student_avg = avg_rank.total_avg,
                                        observation = avg_rank.observation,
                                        academic_year=current_academic_year,
                                        spec_rank=forcounter,
                                        added_by = request.user.username,
                                        classroom=selected_class,
                                        specialty=specialt,
                                        student = avg_rank.student,
                                    )
        #
                messages.success(request, f'{get_classrooms} Ranking DONE per Specialty Class')
                return redirect("all_ranking")
        
            messages.error(request, f'Term Not found')
            return redirect("add_ranking")
            
        messages.error(request, f'Classroom Not found')
        return redirect("add_ranking")

    return render(request, "eval/add_rankx.html", context=context)




@login_required
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
                # print("not results")
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
                                    # print(term)

                            testa_value = 0.0
                            testb_value = 0.0
                            testb_coef = 0.0
                            testa_coef = 0.0
                            if(term == 'second'):
                                obj_eval_first = Eval.objects.filter(title='Test3',student_id=student, academic_year=academic_yr).first()
                                # print(obj_eval_first)
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
                                    # print(f'{subject}___{evals_record}___{evals_record.value}___{evals_record.subject_id}')
                                    testa_value =  decimal.Decimal(testa_value) + evals_record.value
                                    testa_coef = decimal.Decimal(testa_coef) + evals_record.coef

                                if evals_record.title == 'Test4':
                                    # print(f'{subject}___{evals_record}___{evals_record.value}___{evals_record.subject_id}')
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
                            # print(total_eval)


                                # print(testa)
                                # print(testb)
                                # if testa:
                                #     for test1 in testa:
                                #         if(test1.subject_id == subject.id):
                                #             testa_value = test1.value
                                #             testa_coef = test1.coef
                                #             # print(subject.title)
                                            # print(f'{testa}_______{testa_value}_____{testa_coef}')
                                # print(student)

                                # if testb:
                                #     for test2 in testb:
                                #         if(test2.subject_id == subject.id):
                                #             testb_value = test2.value
                                #             testb_coef = test2.coef
                                #             # print(subject.title)
                                # if(subject.category == 'General'):
                                    # print(f"General {subject.coef} {subject.title}")
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
            # print("not results")
            # print(results)
        # else:
        #     for subjj_cl in results:
                # print(subjj_cl.id)
                # print(subjj_cl.coef)
        #         if subjj_cl.coef is None:
                    # print('no subjj coef')
        #         else:
        #             if(subjj_cl.category == 'General'):
                        # print(f"General {subjj_cl.coef}")
        #                 total_gen_coeff = total_gen_coeff + decimal.Decimal(subjj_cl.coef)
        #                 # total_gen_tot = total_gen_tot + decimal.Decimal(subjj_cl.coef)
        #             #)
        #             if(subjj_cl.category == 'Professional'):
                        # print(f"Professional {subjj_cl.coef}")
        #                 total_prof_coeff = total_prof_coeff + decimal.Decimal(subjj_cl.coef)
        #             #
        #             if(term == 'first'):
        #                 testa = obj_eval_class.filter(title='Test1',subject_id=subjj_cl.id)
        #                 testb = obj_eval_class.filter(title='Test2',subject_id=subjj_cl.id)
        #                 # print('first')
        #                 if not testa:
                            # print("no vale a")
        #                     testa_value = 0.0
        #                 else:
        #                     for test1 in testa:
        #                         if(test1.subject_id == subjj_cl.id):
        #                             testa_value = test1.value
        #                 if not testb:
                            # print("no vale b")
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
                        # print(subj_moy_tot)
        #                 # print(testb)
        #                 if(subjj_cl.category == 'General'):
        #                     total_gen_tot = total_gen_tot + total_tot

        #             if(term == 'second'):
        #                 testa = obj_eval_class.filter(title='Test3').filter(subject_id=subjj_cl.id)
        #                 testb = obj_eval_class.filter(title='Test4',subject_id=subjj_cl.id)
        #                 # print('test3')
        #                 # print(testa.filter(subject_id=subjj_cl.id))
        #                 if not testa:
                            # print("no vale a")
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
                            # print("no vale b")
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
                        # print(subj_moy)

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
                        # print(subj_moy_tot)

        #                 # print('test4')
        #                 # print(testb)
        #                 if(subjj_cl.category == 'General'):
        #                     total_gen_tot = total_gen_tot + total_tot

        #             if(term == 'third'):
        #                 testa = obj_eval_class.filter(title='Test5')
        #                 testb = obj_eval_class.filter(title='Test6')
        #                 # print('first')
        #                 if not testa:
                            # print("no vale a")
        #                     testa_value = 0.0
        #                 else:
        #                     for test1 in testa:
        #                         if(test1.subject_id == subjj_cl.id):
        #                             testa_value = test1.value
        #                 if not testb:
                            # print("no vale b")
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
                        # print(subj_moy_tot)
        #                 # print(testb)
        #                 if(subjj_cl.category == 'General'):
        #                     total_gen_tot = total_gen_tot + total_tot
        #     #

        #     #total
            # print(total_coeff)
            # print(total_tot)
            # print("general")
            # print(total_gen_coeff)
            # print(f"General tot: {total_gen_tot}")
            # print("prof")
            # print(total_prof_coeff)
        

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



# fxn to get ranks
def getstudent_rank(student):
    rank = SchoolClasRanking.objects.filter(student=student, is_actif=True).first()
    # print(rank)
    if rank:
        return rank.spec_rank
    else:
        return 0



# get class worst avg
def get_classworstavg(class_room, term, speclty, sch_year="2024/2025"):
    # print(class_room)
    # get max avg of class
    max_spec = ClassRanking.objects.filter(classroom = class_room, term=term, specialty=speclty, academic_year=sch_year, is_actif=True).aggregate(Min('total_avg'))
    # print(max_spec)
    return max_spec

# get class best avg
def get_classbestavg(class_room, speclty, term, sch_year="2024/2025"):
    # print(class_room)
    # get max avg of class
    max_spec = ClassRanking.objects.filter(classroom = class_room, term=term, specialty=speclty, academic_year=sch_year, is_actif=True).aggregate(Max('total_avg'))
    # print(max_spec)
    return max_spec


# get class avg
def get_classavg(class_room, speclty, term, sch_year="2024/2025"):
    # print(class_room)
    # get max avg of class
    max_spec = ClassRanking.objects.filter(classroom = class_room, term=term, specialty=speclty, academic_year=sch_year, is_actif=True).aggregate(Avg('total_avg'))
    # print(max_spec)
    return max_spec


#total number of student per specialty per class
def count_stud_classspec(classroom_info, specialty_info):
    # print(f"classroom_info is {classroom_info}, specialty_info is {specialty_info}")
    count_stud =  Student.objects.filter(student_class=classroom_info, specialty=specialty_info, is_actif=True).count()
    # print(count_stud)
    return count_stud


# get diff term avg
def get_termavg(student, term, year="2024/2025"):
    # print(f"{student}---{term}---{year}")
    term_avg = ClassRanking.objects.filter(student = student, specialty=student.specialty,  term=term, academic_year=year, is_actif=True).aggregate(Max('total_avg'))
    # print(term_avg)
    return term_avg

# get subject passed per term
def get_subj_passedterm(student, term, year="2024/2025"):
    # print(f"subject passed")
    count_subjpass = 0
    title = "first"
    if term == "first":
        title = "Test1"
    if term == "second":
        title = "Test3"
    if term == "third":
        title = "Test5"

    call_subjpass = Eval.objects.filter(student = student, title=title, academic_year=year, is_actif=True)
    if call_subjpass:
        for subjpass in call_subjpass:
            if ((subjpass.value + subjpass.sec_value) / 2) >= 10:
                count_subjpass = count_subjpass + 1
    # print(count_subjpass)
    return count_subjpass


@login_required
def addReportCard(request):
    student = Student.objects.all()
    context = {
        'student':student,
    }
    #add reportcard
    
    
    if request.method == "POST":
        # student = request.POST.get('student')
        student_info = request.POST.get('selected_stud')
        # student_info = request.POST.get('student')
        term = request.POST.get('term')
        academic_yr = request.POST.get('academic_year')
        # print("academic_yr")
        # print(academic_yr)
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
            if student_info == "All":
                obj_student_class_all = Student.objects.filter(is_actif=True)
                # messages.error(request, 
                # generate all report card at once
                # messages.error(request, 'Please Select a student - Something went wrong, please try again!')
                # return redirect('report_cards')
                # for student in  obj_student_class:
                #     print(student)
                #     # loop thro each student
                #     obj_eval_cl_type = Eval.objects.filter(student_id=student, academic_year=academic_yr, is_actif=True)
                #     if obj_eval_cl_type:
                #         if(term == 'first'):
                #             print(f"term---{term}")
                #         if(term == 'second'):
                #             print(f"term---{term}")
                            
            else:
                #get student class
                # obj_student_class = Student.objects.get(id=student_info)
                obj_student_class = Student.objects.filter(name=student_info, is_actif=True).first()
                # print(f"{obj_student_class}---obj_student_class")

                classroomId = obj_student_class.student_class
                # print(f"{classroomId} --- classroomId")
                # classroom =  ClassRoom.objects.get(id=classroomId)
                classroom =  classroomId
                # print(f"{classroom}---classroom")
            
                subjects = Subject.objects.filter(classroom=classroomId)
                # print(subjects)
                # obj_eval_class = Eval.objects.filter(student_id=student_info, academic_year=academic_yr)
                # obj_eval_cl_type = Eval.objects.filter(student_id=student_info, academic_year=academic_yr, is_actif=True)
                obj_eval_cl_type = Eval.objects.filter(student=obj_student_class, academic_year=academic_yr, is_actif=True)
                # print(obj_eval_cl_type)
            # pass
        except:
            messages.error(request, 'Something went wrong')
            return redirect('report_cards')
        
        
        if student_info == "All":
            print("for all")
            if obj_student_class_all:
                for obj_student_class in obj_student_class_all:
                    student = obj_student_class
                    print(student)
                    classroomId = obj_student_class.student_class_id
                    classroom =  ClassRoom.objects.get(id=classroomId)
                    # loop thro each student
                    # obj_eval_cl_type = Eval.objects.filter(student_id=student, academic_year=academic_yr, is_actif=True)
                    obj_eval_cl_type = Eval.objects.filter(student_id=student, academic_year=academic_yr, is_actif=True)
                    if obj_eval_cl_type:
                        # if(term == 'first'):
                        #     print(f"term---{term}")
                        # if(term == 'second'):
                        #     print(f"term---{term}")
                        if(term == 'first'):
                            firstterm_reslts = Eval.objects.filter(student_id=student.id, academic_year= academic_yr, title="Test1", is_actif =True)
                            if firstterm_reslts:
                                for subject_tests in firstterm_reslts:
                                    moyentt = (subject_tests.value + subject_tests.sec_value) / 2
                                    moy_tot = round((moyentt * subject_tests.coef), ndigits=2)
                                    total_coeff = total_coeff + decimal.Decimal(subject_tests.coef)
                                    total_tot = total_tot + decimal.Decimal(moy_tot)
                                    if subject_tests.subject.category == "General":
                                        # print(subject_tests.subject.category)
                                        total_gen_tot = total_gen_tot + total_tot
                                        subject_gen_tot = subject_gen_tot + float(moy_tot)
                                        total_gen_coeff = total_gen_coeff + decimal.Decimal(subject_tests.coef)
                                    if subject_tests.subject.category == "Professional":
                                        # print(subject_tests.subject.category)
                                        total_prof_tot = total_prof_tot + moy_tot
                                        subject_prof_tot = subject_prof_tot + float(moy_tot)
                                        total_prof_coeff = total_prof_coeff + decimal.Decimal(subject_tests.coef)
                                    
                                    # 
                                    subject_value_cat.append([subject_tests.subject.title,subject_tests.value,subject_tests.sec_value, moyentt, subject_tests.coef, moy_tot, subject_tests.observation, subject_tests.subject.category, subject_tests.teacher])
                        
                        if(term == 'second'):
                            print("sec")
                            secondterm_reslts = Eval.objects.filter(student_id=student.id, academic_year= academic_yr, title="Test3", is_actif =True)
                            if secondterm_reslts:
                                for subject_tests in secondterm_reslts:
                                    # print(f"subject_tests --- {subject_tests}")
                                    moyentt = (subject_tests.value + subject_tests.sec_value) / 2
                                    moy_tot = round((moyentt * subject_tests.coef), ndigits=2)
                                    total_coeff = total_coeff + decimal.Decimal(subject_tests.coef)
                                    total_tot = total_tot + decimal.Decimal(moy_tot)
                                    if subject_tests.subject.category == "General":
                                        # print(subject_tests.subject.category)
                                        total_gen_tot = total_gen_tot + total_tot
                                        subject_gen_tot = subject_gen_tot + float(moy_tot)
                                        total_gen_coeff = total_gen_coeff + decimal.Decimal(subject_tests.coef)
                                    if subject_tests.subject.category == "Professional":
                                        # print(subject_tests.subject.category)
                                        total_prof_tot = total_prof_tot + moy_tot
                                        subject_prof_tot = subject_prof_tot + float(moy_tot)
                                        total_prof_coeff = total_prof_coeff + decimal.Decimal(subject_tests.coef)
                                    
                                    # 
                                    subject_value_cat.append([subject_tests.subject.title,subject_tests.value,subject_tests.sec_value, moyentt, subject_tests.coef, moy_tot, subject_tests.observation, subject_tests.subject.category, subject_tests.teacher])
                        
                        if(term == 'third'):
                            thirdterm_reslts = Eval.objects.filter(student_id=student.id, academic_year= academic_yr, title="Test5", is_actif =True)
                            if thirdterm_reslts:
                                for subject_tests in thirdterm_reslts:
                                    # print(f"subject_tests --- {subject_tests}")
                                    moyentt = (subject_tests.value + subject_tests.sec_value) / 2
                                    moy_tot = round((moyentt * subject_tests.coef), ndigits=2)
                                    total_coeff = total_coeff + decimal.Decimal(subject_tests.coef)
                                    total_tot = total_tot + decimal.Decimal(moy_tot)
                                    if subject_tests.subject.category == "General":
                                        # print(subject_tests.subject.category)
                                        total_gen_tot = total_gen_tot + total_tot
                                        subject_gen_tot = subject_gen_tot + float(moy_tot)
                                        total_gen_coeff = total_gen_coeff + decimal.Decimal(subject_tests.coef)
                                    if subject_tests.subject.category == "Professional":
                                        # print(subject_tests.subject.category)
                                        total_prof_tot = total_prof_tot + moy_tot
                                        subject_prof_tot = subject_prof_tot + float(moy_tot)
                                        total_prof_coeff = total_prof_coeff + decimal.Decimal(subject_tests.coef)
                                    
                                    # 
                                    subject_value_cat.append([subject_tests.subject.title,subject_tests.value,subject_tests.sec_value, moyentt, subject_tests.coef, moy_tot, subject_tests.observation, subject_tests.subject.category, subject_tests.teacher])
                        
                    
                    # 
                    # 
                        if total_gen_coeff != 0 or total_prof_coeff != 0:
                            total_coeff = decimal.Decimal(total_gen_coeff) + decimal.Decimal(total_prof_coeff)
                        else:
                            total_coeff = 0.00

                        if subject_gen_tot != 0 or total_gen_coeff != 0:
                            gen_sub_moy = decimal.Decimal(subject_gen_tot ) / decimal.Decimal(total_gen_coeff)
                        else:
                            gen_sub_moy = 0.00
                            
                        if subject_prof_tot != 0 or total_prof_coeff != 0:
                            prof_sub_moy = decimal.Decimal(subject_prof_tot ) / decimal.Decimal(total_prof_coeff)
                        else:
                            prof_sub_moy = 0.00
                            
                        if total_tot != 0 or total_coeff != 0:
                            prof_gen_tot_moy = decimal.Decimal(total_tot ) / decimal.Decimal(total_coeff)
                        else:
                            prof_gen_tot_moy = 0.00

                        # get rank
                        my_rank = getstudent_rank(obj_student_class)


                        # get classavg
                        print(f"for my classabg {classroom}-- {term}--- {obj_student_class.specialty}")
                        my_classavg = get_classavg(classroom,  obj_student_class.specialty, term)
                        print(f"classavg is {my_classavg}")

                        # get classavg
                        my_countstud = count_stud_classspec( classroom, obj_student_class.specialty)
                        print(f"count stud in specialty is {my_countstud}")
                        print(my_countstud)
                        print(type(my_countstud))

                        # get best classavg
                        my_beststud = get_classbestavg( classroom, obj_student_class.specialty,term)
                        print(f"best class avg is {my_beststud}")
                        print(my_beststud)
                        print(type(my_beststud))

                        # get worst classavg
                        my_worststud = get_classworstavg( classroom, term, obj_student_class.specialty)
                        print(f"worst class avg is {my_worststud}")
                        print(my_worststud)
                        print(type(my_worststud))

                        # get first term avg get_termavg(student, term, year="2024/2025")
                        firt_term_avg = get_termavg(obj_student_class, "first", academic_yr)
                        if firt_term_avg:
                            print(f"first term avg is {firt_term_avg}")
                        else: 
                            firt_term_avg = 0.00

                        # get second term avg get_termavg(student, term, year="2024/2025")
                        scnd_term_avg = get_termavg(obj_student_class, "second", academic_yr)
                        if scnd_term_avg:
                            print(f"second term avg is {scnd_term_avg}")
                        else: 
                            scnd_term_avg = 0.00
                        
                        # get third term avg get_termavg(student, term, year="2024/2025")
                        third_term_avg = get_termavg(obj_student_class, "third", academic_yr)
                        if third_term_avg:
                            print(f"third term avg is {third_term_avg}")
                        else: 
                            third_term_avg = 0.00

                        
                        # get_subj_passedterm 
                        # passed subject count per term
                        passed_subj_first = get_subj_passedterm(obj_student_class, "first", academic_yr)
                        
                        if passed_subj_first:
                            print(f"first term subj count is {passed_subj_first}")
                        else: 
                            passed_subj_first = 0

                        passed_subj_second = get_subj_passedterm(obj_student_class, "second", academic_yr)
                        
                        if passed_subj_second:
                            print(f"second term subj count is {passed_subj_second}")
                        else: 
                            passed_subj_second = 0

                        passed_subj_third = get_subj_passedterm(obj_student_class, "third", academic_yr)
                        
                        if passed_subj_third:
                            print(f"third term subj count is {passed_subj_third}")
                        else: 
                            passed_subj_third = 0


                        context = {}
                        context['firstterm_subjpass'] = passed_subj_first
                        context['second_term_subjpass'] = passed_subj_second
                        context['third_avg_subjpass'] = passed_subj_third
                        context['first_avg_term'] = firt_term_avg
                        context['second_term_avg'] = scnd_term_avg
                        context['third_avg_term'] = third_term_avg
                        context['mi_rank'] = my_rank
                        context['mi_class_avg'] = my_classavg
                        context['spec_class_count_stud'] = my_countstud
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

                        # print(context)

                        # using now() to get current time
                        current_time = datetime.datetime.now()
                        # 
                        # check is report card exits
                        chec_card = ReportCard.objects.filter(term = term,student= obj_student_class,academic_year= academic_yr,is_actif=True).first()
                        if chec_card:
                            chec_card.is_actif = False
                            chec_card.modified_by = added_by
                            chec_card.save()
                            report_card = ReportCard.objects.create(
                                student           = obj_student_class ,
                                term              = term,
                                student_rank      = my_rank,
                                gen_coeff         = total_gen_coeff,
                                prof_coeff        = total_prof_coeff,
                                gen_total         = subject_gen_tot,
                                prof_total        = total_prof_tot,
                                general_subjs_avr = gen_sub_moy,
                                prof_subjs_avr    = prof_sub_moy,
                                total_avr         = prof_gen_tot_moy,
                                class_moy_avr     =  my_classavg['total_avg__avg'],
                                best_avr          = my_beststud['total_avg__max'],
                                worst_avr         = my_worststud['total_avg__min'],
                                academic_year     = academic_yr,
                                resumption        = resumptn,
                                added_by          = added_by,
                            )
                        else:
                            #

                            report_card = ReportCard.objects.create(
                                student           = obj_student_class ,
                                term              = term,
                                student_rank      = my_rank,
                                gen_coeff         = total_gen_coeff,
                                prof_coeff        = total_prof_coeff,
                                gen_total         = subject_gen_tot,
                                prof_total        = total_prof_tot,
                                general_subjs_avr = gen_sub_moy,
                                prof_subjs_avr    = prof_sub_moy,
                                total_avr           = prof_gen_tot_moy,
                                class_moy_avr     =  my_classavg['total_avg__avg'],
                                best_avr          = my_beststud['total_avg__max'],
                                worst_avr         = my_worststud['total_avg__min'],
                                academic_year     = academic_yr,
                                resumption        = resumptn,
                                # teacher = teacher,
                                added_by          = added_by,
                            )
                            
                        # 
                    
                        if term == "first":
                            report_card.firstterm_avr = prof_gen_tot_moy
                            
                            if passed_subj_first:
                                report_card.first_subj_passed = passed_subj_first
                            report_card.modified_by = added_by
                            report_card.save()
                        if term == "second":
                            if firt_term_avg["total_avg__max"]:
                                #
                                report_card.firstterm_avr = firt_term_avg["total_avg__max"]
                            if passed_subj_first:
                                report_card.first_subj_passed = passed_subj_first
                            if passed_subj_second:
                                report_card.second_subj_passed = passed_subj_second
                            report_card.secondterm_avr    =  prof_gen_tot_moy
                            report_card.modified_by = added_by
                            report_card.save()
                            
                        if term == "third":
                            if firt_term_avg["total_avg__max"]:
                                #
                                report_card.firstterm_avr = firt_term_avg["total_avg__max"]
                            if scnd_term_avg["total_avg__max"]:
                                #
                                report_card.secondterm_avr = scnd_term_avg["total_avg__max"]
                            if passed_subj_first:
                                report_card.first_subj_passed = passed_subj_first
                            if passed_subj_second:
                                report_card.second_subj_passed = passed_subj_second
                            if passed_subj_third:
                                report_card.third_subj_passed = passed_subj_third
                            report_card.thirdterm_avr    =  prof_gen_tot_moy
                            report_card.modified_by = added_by
                            report_card.save()
                        
                    


                messages.success(request, f'All Record Card added Successfully')
                return redirect("report_cards")
                        
            else:
                messages.error(request, 'No Students Found - Something went wrong, please try again!')
                return redirect('report_cards')

        else:
            # 
            print("for on")
            if obj_student_class:
                # print("stud exits")
                #
                # get reportcard details
                if obj_eval_cl_type:
                    student = obj_student_class 
                    # print(f"obj_eval_cl_type ---{obj_eval_cl_type}")
                    if(term == 'first'):
                        # print(f"term---{term}")
                        firstterm_reslts = Eval.objects.filter(student_id=student.id, academic_year= academic_yr, title="Test1", is_actif =True)
                        if firstterm_reslts:
                            for subject_tests in firstterm_reslts:
                                # print(f"subject_tests --- {subject_tests}")
                                moyentt = (subject_tests.value + subject_tests.sec_value) / 2
                                moy_tot = round((moyentt * subject_tests.coef), ndigits=2)
                                total_coeff = total_coeff + decimal.Decimal(subject_tests.coef)
                                total_tot = total_tot + decimal.Decimal(moy_tot)
                                if subject_tests.subject.category == "General":
                                    # print(subject_tests.subject.category)
                                    total_gen_tot = total_gen_tot + total_tot
                                    subject_gen_tot = subject_gen_tot + float(moy_tot)
                                    total_gen_coeff = total_gen_coeff + decimal.Decimal(subject_tests.coef)
                                if subject_tests.subject.category == "Professional":
                                    # print(subject_tests.subject.category)
                                    total_prof_tot = total_prof_tot + moy_tot
                                    subject_prof_tot = subject_prof_tot + float(moy_tot)
                                    total_prof_coeff = total_prof_coeff + decimal.Decimal(subject_tests.coef)
                                
                                # 
                                subject_value_cat.append([subject_tests.subject.title,subject_tests.value,subject_tests.sec_value, moyentt, subject_tests.coef, moy_tot, subject_tests.observation, subject_tests.subject.category, subject_tests.teacher])
                    
                    if(term == 'second'):
                        # print(f"term---{term}")
                        secondterm_reslts = Eval.objects.filter(student_id=student.id, academic_year= academic_yr, title="Test3", is_actif =True)
                        if secondterm_reslts:
                            for subject_tests in secondterm_reslts:
                                # print(f"subject_tests --- {subject_tests}")
                                moyentt = (subject_tests.value + subject_tests.sec_value) / 2
                                moy_tot = round((moyentt * subject_tests.coef), ndigits=2)
                                total_coeff = total_coeff + decimal.Decimal(subject_tests.coef)
                                total_tot = total_tot + decimal.Decimal(moy_tot)
                                if subject_tests.subject.category == "General":
                                    # print(subject_tests.subject.category)
                                    total_gen_tot = total_gen_tot + total_tot
                                    subject_gen_tot = subject_gen_tot + float(moy_tot)
                                    total_gen_coeff = total_gen_coeff + decimal.Decimal(subject_tests.coef)
                                if subject_tests.subject.category == "Professional":
                                    # print(subject_tests.subject.category)
                                    total_prof_tot = total_prof_tot + moy_tot
                                    subject_prof_tot = subject_prof_tot + float(moy_tot)
                                    total_prof_coeff = total_prof_coeff + decimal.Decimal(subject_tests.coef)
                                
                                # 
                                subject_value_cat.append([subject_tests.subject.title,subject_tests.value,subject_tests.sec_value, moyentt, subject_tests.coef, moy_tot, subject_tests.observation, subject_tests.subject.category, subject_tests.teacher])
                    
                    if(term == 'third'):
                        # print(f"term---{term}")
                        thirdterm_reslts = Eval.objects.filter(student_id=student.id, academic_year= academic_yr, title="Test5", is_actif =True)
                        if thirdterm_reslts:
                            for subject_tests in thirdterm_reslts:
                                # print(f"subject_tests --- {subject_tests}")
                                moyentt = (subject_tests.value + subject_tests.sec_value) / 2
                                moy_tot = round((moyentt * subject_tests.coef), ndigits=2)
                                total_coeff = total_coeff + decimal.Decimal(subject_tests.coef)
                                total_tot = total_tot + decimal.Decimal(moy_tot)
                                if subject_tests.subject.category == "General":
                                    # print(subject_tests.subject.category)
                                    total_gen_tot = total_gen_tot + total_tot
                                    subject_gen_tot = subject_gen_tot + float(moy_tot)
                                    total_gen_coeff = total_gen_coeff + decimal.Decimal(subject_tests.coef)
                                if subject_tests.subject.category == "Professional":
                                    # print(subject_tests.subject.category)
                                    total_prof_tot = total_prof_tot + moy_tot
                                    subject_prof_tot = subject_prof_tot + float(moy_tot)
                                    total_prof_coeff = total_prof_coeff + decimal.Decimal(subject_tests.coef)
                                
                                # 
                                subject_value_cat.append([subject_tests.subject.title,subject_tests.value,subject_tests.sec_value, moyentt, subject_tests.coef, moy_tot, subject_tests.observation, subject_tests.subject.category, subject_tests.teacher])
                    
                
                # 
                # 
                if total_gen_coeff != 0 or total_prof_coeff != 0:
                    total_coeff = decimal.Decimal(total_gen_coeff) + decimal.Decimal(total_prof_coeff)
                else:
                    total_coeff = 0.00

                if subject_gen_tot != 0 or total_gen_coeff != 0:
                    gen_sub_moy = decimal.Decimal(subject_gen_tot ) / decimal.Decimal(total_gen_coeff)
                else:
                    gen_sub_moy = 0.00
                    
                if subject_prof_tot != 0 or total_prof_coeff != 0:
                    prof_sub_moy = decimal.Decimal(subject_prof_tot ) / decimal.Decimal(total_prof_coeff)
                else:
                    prof_sub_moy = 0.00
                    
                if total_tot != 0 or total_coeff != 0:
                    prof_gen_tot_moy = decimal.Decimal(total_tot ) / decimal.Decimal(total_coeff)
                else:
                    prof_gen_tot_moy = 0.00

                # total_coeff = decimal.Decimal(total_gen_coeff) + decimal.Decimal(total_prof_coeff)                           
                # gen_sub_moy = decimal.Decimal(subject_gen_tot ) / decimal.Decimal(total_gen_coeff)
                # prof_sub_moy = decimal.Decimal(subject_prof_tot ) / decimal.Decimal(total_prof_coeff)
                # prof_gen_tot_moy = decimal.Decimal(total_tot ) / decimal.Decimal(total_coeff)

                # get rank
                my_rank = getstudent_rank(obj_student_class)
                # print(f"rank is {my_rank}")

                # # get classavg
                # my_classavg = get_classavg(classroom, obj_student_class.specialty)
                # # print(f"classavg is {my_classavg}")

                # # get classavg
                # my_countstud = count_stud_classspec( classroom, obj_student_class.specialty)
                # # print(f"count stud in specialty is {my_countstud}")


                # get classavg
                my_classavg = get_classavg(classroom, obj_student_class.specialty, term)
                print(f"classavg is {my_classavg}")

                # get classavg
                my_countstud = count_stud_classspec( classroom, obj_student_class.specialty)
                print(f"count stud in specialty is {my_countstud}")
                print(my_countstud)
                print(type(my_countstud))

                # get best classavg
                my_beststud = get_classbestavg( classroom, obj_student_class.specialty, term)
                print(f"best class avg is {my_beststud}")
                print(my_beststud)
                print(type(my_beststud))

                # get worst classavg
                my_worststud = get_classworstavg( classroom, term, obj_student_class.specialty)
                print(f"worst class avg is {my_worststud}")
                print(my_worststud)
                print(type(my_worststud))

                # get first term avg get_termavg(student, term, year="2024/2025")
                firt_term_avg = get_termavg(obj_student_class, "first", academic_yr)
                if firt_term_avg:
                    print(f"first term avg is {firt_term_avg}")
                else: 
                    firt_term_avg = 0.00

                # get second term avg get_termavg(student, term, year="2024/2025")
                scnd_term_avg = get_termavg(obj_student_class, "second", academic_yr)
                if scnd_term_avg:
                    print(f"second term avg is {scnd_term_avg}")
                else: 
                    scnd_term_avg = 0.00
                
                # get third term avg get_termavg(student, term, year="2024/2025")
                third_term_avg = get_termavg(obj_student_class, "third", academic_yr)
                if third_term_avg:
                    print(f"third term avg is {third_term_avg}")
                else: 
                    third_term_avg = 0.00

                
                # get_subj_passedterm 
                # passed subject count per term
                passed_subj_first = get_subj_passedterm(obj_student_class, "first", academic_yr)
                
                if passed_subj_first:
                    print(f"first term subj count is {passed_subj_first}")
                else: 
                    passed_subj_first = 0

                passed_subj_second = get_subj_passedterm(obj_student_class, "second", academic_yr)
                
                if passed_subj_second:
                    print(f"second term subj count is {passed_subj_second}")
                else: 
                    passed_subj_second = 0

                passed_subj_third = get_subj_passedterm(obj_student_class, "third", academic_yr)
                
                if passed_subj_third:
                    print(f"third term subj count is {passed_subj_third}")
                else: 
                    passed_subj_third = 0


                context = {}
                context['firstterm_subjpass'] = passed_subj_first
                context['second_term_subjpass'] = passed_subj_second
                context['third_avg_subjpass'] = passed_subj_third
                context['first_avg_term'] = firt_term_avg
                context['second_term_avg'] = scnd_term_avg
                context['third_avg_term'] = third_term_avg
                context['mi_rank'] = my_rank
                context['mi_class_avg'] = my_classavg
                context['spec_class_count_stud'] = my_countstud
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

                # print(context)

                # using now() to get current time
                current_time = datetime.datetime.now()
                # 
                # check is report card exits
                chec_card = ReportCard.objects.filter(term = term,student= obj_student_class,academic_year= academic_yr,is_actif=True).first()
                if chec_card:
                    chec_card.is_actif = False
                    chec_card.modified_by = added_by
                    chec_card.save()
                    report_card = ReportCard.objects.create(
                        student           = obj_student_class ,
                        term              = term,
                        student_rank      = my_rank,
                        gen_coeff         = total_gen_coeff,
                        prof_coeff        = total_prof_coeff,
                        gen_total         = subject_gen_tot,
                        prof_total        = total_prof_tot,
                        general_subjs_avr = gen_sub_moy,
                        prof_subjs_avr    = prof_sub_moy,
                        total_avr         = prof_gen_tot_moy,
                        class_moy_avr     =  my_classavg['total_avg__avg'],
                        best_avr          = my_beststud['total_avg__max'],
                        worst_avr         = my_worststud['total_avg__min'],
                        # firstterm_avr     = firt_term_avg["total_avg__max"],
                        # secondterm_avr  = scnd_term_avg,
                        # third_subj_passed     = third_term_avg,
                        # first_subj_passed =  passed_subj_first,
                        # second_subj_passed = passed_subj_second,
                        # academic_year = '2023/2024',
                        academic_year     = academic_yr,
                        resumption        = resumptn,
                        # teacher = teacher,
                        added_by          = added_by,
                    )
                else:
                    #

                    report_card = ReportCard.objects.create(
                        student           = obj_student_class ,
                        term              = term,
                        student_rank      = my_rank,
                        gen_coeff         = total_gen_coeff,
                        prof_coeff        = total_prof_coeff,
                        gen_total         = subject_gen_tot,
                        prof_total        = total_prof_tot,
                        general_subjs_avr = gen_sub_moy,
                        prof_subjs_avr    = prof_sub_moy,
                        total_avr           = prof_gen_tot_moy,
                        class_moy_avr     =  my_classavg['total_avg__avg'],
                        best_avr          = my_beststud['total_avg__max'],
                        worst_avr         = my_worststud['total_avg__min'],
                        # firstterm_avr       = firt_term_avg["total_avg__max"],
                        # secondterm_avr  = scnd_term_avg,
                        # third_subj_passed     = third_term_avg,
                        # first_subj_passed =  passed_subj_first,
                        # second_subj_passed = passed_subj_second,
                        # # third_subj_passed =  passed_subj_third,
                        # academic_year = '2023/2024',
                        academic_year     = academic_yr,
                        resumption        = resumptn,
                        # teacher = teacher,
                        added_by          = added_by,
                    )
                    
                # 
                
                # print(f"firt_term_avg ----{firt_term_avg}")
                # print(firt_term_avg["total_avg__max"])
                # print(f"scnd_term_avg ----{scnd_term_avg}")
                # print(scnd_term_avg["total_avg__max"])
            
                if term == "first":
                    report_card.firstterm_avr = prof_gen_tot_moy
                    
                    if passed_subj_first:
                        report_card.first_subj_passed = passed_subj_first
                    report_card.modified_by = added_by
                    report_card.save()
                if term == "second":
                    if firt_term_avg["total_avg__max"]:
                        #
                        report_card.firstterm_avr = firt_term_avg["total_avg__max"]
                    if passed_subj_first:
                        report_card.first_subj_passed = passed_subj_first
                    if passed_subj_second:
                        report_card.second_subj_passed = passed_subj_second
                    report_card.secondterm_avr    =  prof_gen_tot_moy
                    report_card.modified_by = added_by
                    report_card.save()
                    
                if term == "third":
                    if firt_term_avg["total_avg__max"]:
                        #
                        report_card.firstterm_avr = firt_term_avg["total_avg__max"]
                    if scnd_term_avg["total_avg__max"]:
                        #
                        report_card.secondterm_avr = scnd_term_avg["total_avg__max"]
                    if passed_subj_first:
                        report_card.first_subj_passed = passed_subj_first
                    if passed_subj_second:
                        report_card.second_subj_passed = passed_subj_second
                    if passed_subj_third:
                        report_card.third_subj_passed = passed_subj_third
                    report_card.thirdterm_avr    =  prof_gen_tot_moy
                    report_card.modified_by = added_by
                    report_card.save()
                    
                


                messages.success(request, f'{obj_student_class.name} Record Card added Successfully')
                return redirect("report_cards")
                        
            else:
                messages.error(request, 'No Students Found - Something went wrong, please try again!')
                return redirect('report_cards')
        

        # 
        # 


        # #Calculate the Avg Total
        # if obj_student_class:
        #     # print("stud exits")
        #     # for student in  obj_student_class:
        #         #
        #         # get reportcard details
        #     if obj_eval_cl_type:
        #         student = obj_student_class 
        #         # print(f"obj_eval_cl_type ---{obj_eval_cl_type}")
        #         if(term == 'first'):
        #             # print(f"term---{term}")
        #             firstterm_reslts = Eval.objects.filter(student_id=student.id, academic_year= academic_yr, title="Test1", is_actif =True)
        #             if firstterm_reslts:
        #                 for subject_tests in firstterm_reslts:
        #                     # print(f"subject_tests --- {subject_tests}")
        #                     moyentt = (subject_tests.value + subject_tests.sec_value) / 2
        #                     moy_tot = round((moyentt * subject_tests.coef), ndigits=2)
        #                     total_coeff = total_coeff + decimal.Decimal(subject_tests.coef)
        #                     total_tot = total_tot + decimal.Decimal(moy_tot)
        #                     if subject_tests.subject.category == "General":
        #                         # print(subject_tests.subject.category)
        #                         total_gen_tot = total_gen_tot + total_tot
        #                         subject_gen_tot = subject_gen_tot + float(moy_tot)
        #                         total_gen_coeff = total_gen_coeff + decimal.Decimal(subject_tests.coef)
        #                     if subject_tests.subject.category == "Professional":
        #                         # print(subject_tests.subject.category)
        #                         total_prof_tot = total_prof_tot + moy_tot
        #                         subject_prof_tot = subject_prof_tot + float(moy_tot)
        #                         total_prof_coeff = total_prof_coeff + decimal.Decimal(subject_tests.coef)
                            
        #                     # 
        #                     subject_value_cat.append([subject_tests.subject.title,subject_tests.value,subject_tests.sec_value, moyentt, subject_tests.coef, moy_tot, subject_tests.observation, subject_tests.subject.category, subject_tests.teacher])
                
        #         if(term == 'second'):
        #             # print(f"term---{term}")
        #             secondterm_reslts = Eval.objects.filter(student_id=student.id, academic_year= academic_yr, title="Test3", is_actif =True)
        #             if secondterm_reslts:
        #                 for subject_tests in secondterm_reslts:
        #                     # print(f"subject_tests --- {subject_tests}")
        #                     moyentt = (subject_tests.value + subject_tests.sec_value) / 2
        #                     moy_tot = round((moyentt * subject_tests.coef), ndigits=2)
        #                     total_coeff = total_coeff + decimal.Decimal(subject_tests.coef)
        #                     total_tot = total_tot + decimal.Decimal(moy_tot)
        #                     if subject_tests.subject.category == "General":
        #                         # print(subject_tests.subject.category)
        #                         total_gen_tot = total_gen_tot + total_tot
        #                         subject_gen_tot = subject_gen_tot + float(moy_tot)
        #                         total_gen_coeff = total_gen_coeff + decimal.Decimal(subject_tests.coef)
        #                     if subject_tests.subject.category == "Professional":
        #                         # print(subject_tests.subject.category)
        #                         total_prof_tot = total_prof_tot + moy_tot
        #                         subject_prof_tot = subject_prof_tot + float(moy_tot)
        #                         total_prof_coeff = total_prof_coeff + decimal.Decimal(subject_tests.coef)
                            
        #                     # 
        #                     subject_value_cat.append([subject_tests.subject.title,subject_tests.value,subject_tests.sec_value, moyentt, subject_tests.coef, moy_tot, subject_tests.observation, subject_tests.subject.category, subject_tests.teacher])
                
        #         if(term == 'third'):
        #             # print(f"term---{term}")
        #             thirdterm_reslts = Eval.objects.filter(student_id=student.id, academic_year= academic_yr, title="Test5", is_actif =True)
        #             if thirdterm_reslts:
        #                 for subject_tests in thirdterm_reslts:
        #                     # print(f"subject_tests --- {subject_tests}")
        #                     moyentt = (subject_tests.value + subject_tests.sec_value) / 2
        #                     moy_tot = round((moyentt * subject_tests.coef), ndigits=2)
        #                     total_coeff = total_coeff + decimal.Decimal(subject_tests.coef)
        #                     total_tot = total_tot + decimal.Decimal(moy_tot)
        #                     if subject_tests.subject.category == "General":
        #                         # print(subject_tests.subject.category)
        #                         total_gen_tot = total_gen_tot + total_tot
        #                         subject_gen_tot = subject_gen_tot + float(moy_tot)
        #                         total_gen_coeff = total_gen_coeff + decimal.Decimal(subject_tests.coef)
        #                     if subject_tests.subject.category == "Professional":
        #                         # print(subject_tests.subject.category)
        #                         total_prof_tot = total_prof_tot + moy_tot
        #                         subject_prof_tot = subject_prof_tot + float(moy_tot)
        #                         total_prof_coeff = total_prof_coeff + decimal.Decimal(subject_tests.coef)
                            
        #                     # 
        #                     subject_value_cat.append([subject_tests.subject.title,subject_tests.value,subject_tests.sec_value, moyentt, subject_tests.coef, moy_tot, subject_tests.observation, subject_tests.subject.category, subject_tests.teacher])
                
            
        #     # 
        #     # 
        #     if total_gen_coeff != 0 or total_prof_coeff != 0:
        #         total_coeff = decimal.Decimal(total_gen_coeff) + decimal.Decimal(total_prof_coeff)
        #     else:
        #         total_coeff = 0.00

        #     if subject_gen_tot != 0 or total_gen_coeff != 0:
        #         gen_sub_moy = decimal.Decimal(subject_gen_tot ) / decimal.Decimal(total_gen_coeff)
        #     else:
        #         gen_sub_moy = 0.00
                
        #     if subject_prof_tot != 0 or total_prof_coeff != 0:
        #        prof_sub_moy = decimal.Decimal(subject_prof_tot ) / decimal.Decimal(total_prof_coeff)
        #     else:
        #         prof_sub_moy = 0.00
                
        #     if total_tot != 0 or total_coeff != 0:
        #       prof_gen_tot_moy = decimal.Decimal(total_tot ) / decimal.Decimal(total_coeff)
        #     else:
        #         prof_gen_tot_moy = 0.00

        #     # total_coeff = decimal.Decimal(total_gen_coeff) + decimal.Decimal(total_prof_coeff)                           
        #     # gen_sub_moy = decimal.Decimal(subject_gen_tot ) / decimal.Decimal(total_gen_coeff)
        #     # prof_sub_moy = decimal.Decimal(subject_prof_tot ) / decimal.Decimal(total_prof_coeff)
        #     # prof_gen_tot_moy = decimal.Decimal(total_tot ) / decimal.Decimal(total_coeff)

        #     # get rank
        #     my_rank = getstudent_rank(obj_student_class)
        #     # print(f"rank is {my_rank}")

        #     # # get classavg
        #     # my_classavg = get_classavg(classroom, obj_student_class.specialty)
        #     # # print(f"classavg is {my_classavg}")

        #     # # get classavg
        #     # my_countstud = count_stud_classspec( classroom, obj_student_class.specialty)
        #     # # print(f"count stud in specialty is {my_countstud}")


        #     # get classavg
        #     my_classavg = get_classavg(classroom, obj_student_class.specialty)
        #     print(f"classavg is {my_classavg}")

        #     # get classavg
        #     my_countstud = count_stud_classspec( classroom, obj_student_class.specialty)
        #     print(f"count stud in specialty is {my_countstud}")
        #     print(my_countstud)
        #     print(type(my_countstud))

        #     # get best classavg
        #     my_beststud = get_classbestavg( classroom, obj_student_class.specialty)
        #     print(f"best class avg is {my_beststud}")
        #     print(my_beststud)
        #     print(type(my_beststud))

        #     # get worst classavg
        #     my_worststud = get_classworstavg( classroom, obj_student_class.specialty)
        #     print(f"worst class avg is {my_worststud}")
        #     print(my_worststud)
        #     print(type(my_worststud))

        #     # get first term avg get_termavg(student, term, year="2024/2025")
        #     firt_term_avg = get_termavg(obj_student_class, "first", academic_yr)
        #     if firt_term_avg:
        #         print(f"first term avg is {firt_term_avg}")
        #     else: 
        #         firt_term_avg = 0.00

        #     # get second term avg get_termavg(student, term, year="2024/2025")
        #     scnd_term_avg = get_termavg(obj_student_class, "second", academic_yr)
        #     if scnd_term_avg:
        #         print(f"second term avg is {scnd_term_avg}")
        #     else: 
        #         scnd_term_avg = 0.00
            
        #     # get third term avg get_termavg(student, term, year="2024/2025")
        #     third_term_avg = get_termavg(obj_student_class, "third", academic_yr)
        #     if third_term_avg:
        #         print(f"third term avg is {third_term_avg}")
        #     else: 
        #         third_term_avg = 0.00

            
        #     # get_subj_passedterm 
        #     # passed subject count per term
        #     passed_subj_first = get_subj_passedterm(obj_student_class, "first", academic_yr)
            
        #     if passed_subj_first:
        #         print(f"first term subj count is {passed_subj_first}")
        #     else: 
        #         passed_subj_first = 0

        #     passed_subj_second = get_subj_passedterm(obj_student_class, "second", academic_yr)
            
        #     if passed_subj_second:
        #         print(f"second term subj count is {passed_subj_second}")
        #     else: 
        #         passed_subj_second = 0

        #     passed_subj_third = get_subj_passedterm(obj_student_class, "third", academic_yr)
            
        #     if passed_subj_third:
        #         print(f"third term subj count is {passed_subj_third}")
        #     else: 
        #         passed_subj_third = 0


        #     context = {}
        #     context['firstterm_subjpass'] = passed_subj_first
        #     context['second_term_subjpass'] = passed_subj_second
        #     context['third_avg_subjpass'] = passed_subj_third
        #     context['first_avg_term'] = firt_term_avg
        #     context['second_term_avg'] = scnd_term_avg
        #     context['third_avg_term'] = third_term_avg
        #     context['mi_rank'] = my_rank
        #     context['mi_class_avg'] = my_classavg
        #     context['spec_class_count_stud'] = my_countstud
        #     context['prof_sub_moy'] = round(prof_sub_moy, ndigits=2)
        #     context['prof_gen_tot_moy'] = round(prof_gen_tot_moy, ndigits=2)
        #     context['subject_line'] = subject_value_cat
        #     context['p_settings'] = p_settings
        #     context['student'] = obj_student_class
        #     context['classroom'] = classroom
        #     context['total_coeff'] = total_coeff
        #     context['total_tot'] = total_tot
        #     context['total_gen_coeff'] = total_gen_coeff
        #     context['total_prof_coeff'] = total_prof_coeff
        #     context['gen_tot'] = total_gen_tot
        #     context['subject_gen_tot'] = subject_gen_tot #gen total subj
        #     context['gen_sub_moy'] = round(gen_sub_moy, ndigits=2)
        #     context['subj_cat'] = subj_cat
        #     context['total_prof_tot'] = total_prof_tot
        #     # context['avgTotal'] = "{:.2f}".format(invoiceTotal)

        #     # print(context)

        #     # using now() to get current time
        #     current_time = datetime.datetime.now()
        #     # 
        #     # check is report card exits
        #     chec_card = ReportCard.objects.filter(term = term,student= obj_student_class,academic_year= academic_yr,is_actif=True).first()
        #     if chec_card:
        #         chec_card.is_actif = False
        #         chec_card.modified_by = added_by
        #         chec_card.save()
        #         report_card = ReportCard.objects.create(
        #             student           = obj_student_class ,
        #             term              = term,
        #             student_rank      = my_rank,
        #             gen_coeff         = total_gen_coeff,
        #             prof_coeff        = total_prof_coeff,
        #             gen_total         = subject_gen_tot,
        #             prof_total        = total_prof_tot,
        #             general_subjs_avr = gen_sub_moy,
        #             prof_subjs_avr    = prof_sub_moy,
        #             total_avr         = prof_gen_tot_moy,
        #             class_moy_avr     =  my_classavg['total_avg__avg'],
        #             best_avr          = my_beststud['total_avg__max'],
        #             worst_avr         = my_worststud['total_avg__min'],
        #             # firstterm_avr     = firt_term_avg["total_avg__max"],
        #             # secondterm_avr  = scnd_term_avg,
        #             # third_subj_passed     = third_term_avg,
        #             # first_subj_passed =  passed_subj_first,
        #             # second_subj_passed = passed_subj_second,
        #             # academic_year = '2023/2024',
        #             academic_year     = academic_yr,
        #             resumption        = resumptn,
        #             # teacher = teacher,
        #             added_by          = added_by,
        #         )
        #     else:
        #         #

        #         report_card = ReportCard.objects.create(
        #             student           = obj_student_class ,
        #             term              = term,
        #             student_rank      = my_rank,
        #             gen_coeff         = total_gen_coeff,
        #             prof_coeff        = total_prof_coeff,
        #             gen_total         = subject_gen_tot,
        #             prof_total        = total_prof_tot,
        #             general_subjs_avr = gen_sub_moy,
        #             prof_subjs_avr    = prof_sub_moy,
        #             total_avr           = prof_gen_tot_moy,
        #             class_moy_avr     =  my_classavg['total_avg__avg'],
        #             best_avr          = my_beststud['total_avg__max'],
        #             worst_avr         = my_worststud['total_avg__min'],
        #             # firstterm_avr       = firt_term_avg["total_avg__max"],
        #             # secondterm_avr  = scnd_term_avg,
        #             # third_subj_passed     = third_term_avg,
        #             # first_subj_passed =  passed_subj_first,
        #             # second_subj_passed = passed_subj_second,
        #             # # third_subj_passed =  passed_subj_third,
        #             # academic_year = '2023/2024',
        #             academic_year     = academic_yr,
        #             resumption        = resumptn,
        #             # teacher = teacher,
        #             added_by          = added_by,
        #         )
                
        #     # 
            
        #     # print(f"firt_term_avg ----{firt_term_avg}")
        #     # print(firt_term_avg["total_avg__max"])
        #     # print(f"scnd_term_avg ----{scnd_term_avg}")
        #     # print(scnd_term_avg["total_avg__max"])
           
        #     if term == "first":
        #         report_card.firstterm_avr = prof_gen_tot_moy
                
        #         if passed_subj_first:
        #             report_card.first_subj_passed = passed_subj_first
        #         report_card.modified_by = added_by
        #         report_card.save()
        #     if term == "second":
        #         if firt_term_avg["total_avg__max"]:
        #             #
        #             report_card.firstterm_avr = firt_term_avg["total_avg__max"]
        #         if passed_subj_first:
        #             report_card.first_subj_passed = passed_subj_first
        #         if passed_subj_second:
        #             report_card.second_subj_passed = passed_subj_second
        #         report_card.secondterm_avr    =  prof_gen_tot_moy
        #         report_card.modified_by = added_by
        #         report_card.save()
                
        #     if term == "third":
        #         if firt_term_avg["total_avg__max"]:
        #             #
        #             report_card.firstterm_avr = firt_term_avg["total_avg__max"]
        #         if scnd_term_avg["total_avg__max"]:
        #             #
        #             report_card.secondterm_avr = scnd_term_avg["total_avg__max"]
        #         if passed_subj_first:
        #             report_card.first_subj_passed = passed_subj_first
        #         if passed_subj_second:
        #             report_card.second_subj_passed = passed_subj_second
        #         if passed_subj_third:
        #             report_card.third_subj_passed = passed_subj_third
        #         report_card.thirdterm_avr    =  prof_gen_tot_moy
        #         report_card.modified_by = added_by
        #         report_card.save()
                
            


        #     messages.success(request, f'{obj_student_class.name} Record Card added Successfully')
        #     return redirect("report_cards")
                    
        # else:
        #     messages.error(request, 'No Students Found - Something went wrong, please try again!')
        #     return redirect('report_cards')
        # 
        # 
        # 

            #     for subject in subjects:
                    # print(subject)
            #         if subject.coef is None:
            #             # print('no subjj coef')
            #             messages.error(request, 'No Coef found')
            #             return redirect('report_cards')
            #         else:
            #             if obj_eval_cl_type:
                            # print("obj_eval_cl_type:")
            #                 for evals in obj_eval_cl_type:
            #                     if evals.subject_id == subject.id:
            #                         if(term == 'first'):
            #                             # print("term")
            #                             # print(term)
            #                             # print(evals)
            #                             # testa = obj_eval_class.filter(title='Test1',subject_id=subject.id, student=student)
            #                             # testb = obj_eval_class.filter(title='Test2',subject_id=subject.id, student=student)
            #                             obj_eval = Eval.objects.filter(student_id=student, title="Test1", academic_year=academic_yr, is_actif=True).first()
            #                             test_reslt = obj_eval
            #                             # print("test_reslt")
            #                             # print(test_reslt)
            #                             # print('first')
            #                             if not test_reslt:
            #                                 # print("no vale a")
            #                                 testa_value = 0.0
            #                                 messages.error(request, 'No Test Results Found')
            #                                 return redirect('report_cards')
            #                             else:
                                            # print("in")
                                            # print(print(test_reslt))
            #                                 if subject.category == 'General':
            #                                     # testa_value = testa.value
            #                                     testa_value = test_reslt.value
            #                                     testb_value = test_reslt.sec_value
            #                                         #
                                        
            #                                     total_eval = testa_value + testb_value
            #                                     moyentt = total_eval / 2
            #                                     # print(moyentt)

            #                                     subj_moy = f"{subject.id}_{moyentt}_{subject.title}"
            #                                     total_gen_coeff = total_gen_coeff + decimal.Decimal(evals.coef)
            #                                     # total
            #                                     moy_tot = moyentt  * int(evals.coef)
            #                                     total_tot = total_tot + decimal.Decimal(moy_tot)
            #                                     subj_moy_tot = f"{subject.title}_{subject.id}_{evals.coef}_{moyentt}_{moy_tot}"
            #                                     total_gen_tot = total_gen_tot + moy_tot
            #                                     subject_gen_tot = decimal.Decimal(subject_gen_tot) + moy_tot
            #                                     total_gen_tot = total_gen_tot + total_tot
                                                
            #                                 # print(subj_moy_tot)
            #                                 # print(testb)
            #                                 if subject.category == 'Professional':
            #                                     testa_value = test_reslt.value
            #                                     testb_value = test_reslt.sec_value
            #                                         #
                                        
            #                                     total_eval = testa_value + testb_value
            #                                     moyentt = total_eval / 2
            #                                     # print(moyentt)

            #                                     subj_moy = f"{subject.id}_{moyentt}_{subject.title}"
            #                                     total_prof_coeff = total_prof_coeff + decimal.Decimal(evals.coef)
            #                                     # total
            #                                     moy_tot = moyentt  * int(evals.coef)
            #                                     total_tot = total_tot + decimal.Decimal(moy_tot)
            #                                     subj_moy_tot = f"{subject.title}_{subject.id}_{evals.coef}_{moyentt}_{moy_tot}"
            #                                     total_gen_tot = total_gen_tot + moy_tot
            #                                     subject_prof_tot = decimal.Decimal(subject_prof_tot) + moy_tot
            #                                     total_prof_tot = total_prof_tot + moy_tot

            #                                 # if(subject.category == 'General'):
            #                                 #     total_gen_tot = total_gen_tot + total_tot
            #                                 #     #
            #                                 # if(subject.category == 'Professional'):
            #                                 #     total_prof_tot = total_prof_tot + moy_tot
            #                                 #
            #                                 # subject_value_cat.append([test1.subject.title,testa_value,testb_value, moyentt, moy_tot,evals.coef, test2.observation, subject.category, test1.teacher])
            #                                 subject_value_cat.append([test_reslt.subject.title,testa_value,testb_value, moyentt, moy_tot,evals.coef, test_reslt.observation, subject.category, test_reslt.teacher])
                                    

            #                         # 
                                    
            #                         if(term == 'second'):
            #                             obj_eval = Eval.objects.filter(student_id=student, title="Test3", academic_year=academic_yr, is_actif=True).first()
            #                             test_reslt = obj_eval
            #                             # print('first')
            #                             if not test_reslt:
            #                                 # print("no vale a")
            #                                 testa_value = 0.0
            #                                 messages.error(request, 'No Test Results Found')
            #                                 return redirect('report_cards')
            #                             else:
            #                                 # print("in")
            #                                 # print(print(test_reslt))
            #                                 if subject.category == 'General':
            #                                     # testa_value = testa.value
            #                                     testa_value = test_reslt.value
            #                                     testb_value = test_reslt.sec_value
            #                                         #
                                        
            #                                     total_eval = testa_value + testb_value
            #                                     moyentt = total_eval / 2
            #                                     # print(moyentt)

            #                                     subj_moy = f"{subject.id}_{moyentt}_{subject.title}"
            #                                     total_gen_coeff = total_gen_coeff + decimal.Decimal(evals.coef)
            #                                     # total
            #                                     moy_tot = moyentt  * int(evals.coef)
            #                                     total_tot = total_tot + decimal.Decimal(moy_tot)
            #                                     subj_moy_tot = f"{subject.title}_{subject.id}_{evals.coef}_{moyentt}_{moy_tot}"
            #                                     total_gen_tot = total_gen_tot + moy_tot
            #                                     subject_gen_tot = decimal.Decimal(subject_gen_tot) + moy_tot
            #                                     total_gen_tot = total_gen_tot + total_tot
                                                
            #                                 # print(subj_moy_tot)
            #                                 # print(testb)
            #                                 if subject.category == 'Professional':
            #                                     testa_value = test_reslt.value
            #                                     testb_value = test_reslt.sec_value
            #                                         #
                                        
            #                                     total_eval = testa_value + testb_value
            #                                     moyentt = total_eval / 2
            #                                     # print(moyentt)

            #                                     subj_moy = f"{subject.id}_{moyentt}_{subject.title}"
            #                                     total_prof_coeff = total_prof_coeff + decimal.Decimal(evals.coef)
            #                                     # total
            #                                     moy_tot = moyentt  * int(evals.coef)
            #                                     total_tot = total_tot + decimal.Decimal(moy_tot)
            #                                     subj_moy_tot = f"{subject.title}_{subject.id}_{evals.coef}_{moyentt}_{moy_tot}"
            #                                     total_gen_tot = total_gen_tot + moy_tot
            #                                     subject_prof_tot = decimal.Decimal(subject_prof_tot) + moy_tot
            #                                     total_prof_tot = total_prof_tot + moy_tot
            #                                     # 
            #                                 subject_value_cat.append([test_reslt.subject.title,testa_value,testb_value, moyentt, moy_tot,evals.coef, test_reslt.observation, subject.category, test_reslt.teacher])
                                    

            #                         # 
                                    
                                    
            #                         if(term == 'third'):
            #                             obj_eval = Eval.objects.filter(student_id=student, title="Test5", academic_year=academic_yr, is_actif=True).first()
            #                             test_reslt = obj_eval
            #                             # print('first')
            #                             if not test_reslt:
            #                                 # print("no vale a")
            #                                 testa_value = 0.0
            #                                 messages.error(request, 'No Test Results Found')
            #                                 return redirect('report_cards')
            #                             else:
            #                                 # print("in")
            #                                 # print(print(test_reslt))
            #                                 if subject.category == 'General':
            #                                     # testa_value = testa.value
            #                                     testa_value = test_reslt.value
            #                                     testb_value = test_reslt.sec_value
            #                                         #
                                        
            #                                     total_eval = testa_value + testb_value
            #                                     moyentt = total_eval / 2
            #                                     # print(moyentt)

            #                                     subj_moy = f"{subject.id}_{moyentt}_{subject.title}"
            #                                     total_gen_coeff = total_gen_coeff + decimal.Decimal(evals.coef)
            #                                     # total
            #                                     moy_tot = moyentt  * int(evals.coef)
            #                                     total_tot = total_tot + decimal.Decimal(moy_tot)
            #                                     subj_moy_tot = f"{subject.title}_{subject.id}_{evals.coef}_{moyentt}_{moy_tot}"
            #                                     total_gen_tot = total_gen_tot + moy_tot
            #                                     subject_gen_tot = decimal.Decimal(subject_gen_tot) + moy_tot
            #                                     total_gen_tot = total_gen_tot + total_tot
                                                
            #                                 # print(subj_moy_tot)
            #                                 # print(testb)
            #                                 if subject.category == 'Professional':
            #                                     testa_value = test_reslt.value
            #                                     testb_value = test_reslt.sec_value
            #                                         #
                                        
            #                                     total_eval = testa_value + testb_value
            #                                     moyentt = total_eval / 2
            #                                     # print(moyentt)

            #                                     subj_moy = f"{subject.id}_{moyentt}_{subject.title}"
            #                                     total_prof_coeff = total_prof_coeff + decimal.Decimal(evals.coef)
            #                                     # total
            #                                     moy_tot = moyentt  * int(evals.coef)
            #                                     total_tot = total_tot + decimal.Decimal(moy_tot)
            #                                     subj_moy_tot = f"{subject.title}_{subject.id}_{evals.coef}_{moyentt}_{moy_tot}"
            #                                     total_gen_tot = total_gen_tot + moy_tot
            #                                     subject_prof_tot = decimal.Decimal(subject_prof_tot) + moy_tot
            #                                     total_prof_tot = total_prof_tot + moy_tot
            #                                     # 
            #                                 subject_value_cat.append([test_reslt.subject.title,testa_value,testb_value, moyentt, moy_tot,evals.coef, test_reslt.observation, subject.category, test_reslt.teacher])

            #                         #     # print(subject_value_cat)
            #                         #     # print("total_prof_coeff")
            #                         #     # print(total_prof_coeff)
            #                         #     # print("total_gen_coeff")
            #                         #     # print(total_gen_coeff)
            #                         #     # print('subj_moy_tot')
            #                         #     # print(subj_moy_tot)
                                                       

            #                         #     # print("subject_value_cat")            
            #                         #     # print(subject_value_cat)
            #                         #     # print("subject_gen_tot")
            #                         #     # print(subject_gen_tot)
            #                         #     # print("subject_prof_tot")
            #                         #     # print(subject_prof_tot)
            #                         #     # print("total_tot ")
            #                         #     # print(total_tot )

            #                         #     # total_coeff = decimal.Decimal(total_gen_coeff) + decimal.Decimal(total_prof_coeff)
                                        
                                        
            #                         #     # gen_sub_moy = decimal.Decimal(subject_gen_tot ) / decimal.Decimal(total_gen_coeff)
            #                         #     # prof_sub_moy = decimal.Decimal(subject_prof_tot ) / decimal.Decimal(total_prof_coeff)
            #                         #     # prof_gen_tot_moy = decimal.Decimal(total_tot ) / decimal.Decimal(total_coeff)

            #                         #     # # get rank
            #                         #     # my_rank = getstudent_rank(obj_student_class)
            #                         #     # print(f"rank is {my_rank}")

            #                         #     # # get classavg
            #                         #     # my_classavg = get_classavg(classroom)
            #                         #     # print(f"classavg is {my_classavg}")

            #                         #     # # get classavg
            #                         #     # my_countstud = count_stud_classspec( classroom, obj_student_class.specialty)
            #                         #     # print(f"count stud in specialty is {my_countstud}")



            #                         #     # # get first term avg get_termavg(student, term, year="2024/2025")
            #                         #     # firt_term_avg = get_termavg(obj_student_class, "first", academic_yr)
            #                         #     # if firt_term_avg:
                                    #     #     print(f"first term avg is {firt_term_avg}")
            #                         #     # else: 
            #                         #     #     firt_term_avg = 0.00

            #                         #     # # get second term avg get_termavg(student, term, year="2024/2025")
            #                         #     # scnd_term_avg = get_termavg(obj_student_class, "second", academic_yr)
            #                         #     # if scnd_term_avg:
                                    #     #     print(f"second term avg is {scnd_term_avg}")
            #                         #     # else: 
            #                         #     #     scnd_term_avg = 0.00
                                        
            #                         #     # # get third term avg get_termavg(student, term, year="2024/2025")
            #                         #     # third_term_avg = get_termavg(obj_student_class, "third", academic_yr)
            #                         #     # if third_term_avg:
                                    #     #     print(f"third term avg is {third_term_avg}")
            #                         #     # else: 
            #                         #     #     third_term_avg = 0.00


            #                         #     # context = {}
            #                         #     # context['first_avg_term'] = firt_term_avg
            #                         #     # context['second_term_avg'] = scnd_term_avg
            #                         #     # context['third_avg_term'] = third_term_avg
            #                         #     # context['mi_rank'] = my_rank
            #                         #     # context['mi_class_avg'] = my_classavg
            #                         #     # context['spec_class_count_stud'] = my_countstud
            #                         #     # context['prof_sub_moy'] = round(prof_sub_moy, ndigits=2)
            #                         #     # context['prof_gen_tot_moy'] = round(prof_gen_tot_moy, ndigits=2)
            #                         #     # context['subject_line'] = subject_value_cat
            #                         #     # context['p_settings'] = p_settings
            #                         #     # context['student'] = obj_student_class
            #                         #     # context['classroom'] = classroom
            #                         #     # context['total_coeff'] = total_coeff
            #                         #     # context['total_tot'] = total_tot
            #                         #     # context['total_gen_coeff'] = total_gen_coeff
            #                         #     # context['total_prof_coeff'] = total_prof_coeff
            #                         #     # context['gen_tot'] = total_gen_tot
            #                         #     # context['subject_gen_tot'] = subject_gen_tot #gen total subj
            #                         #     # context['gen_sub_moy'] = round(gen_sub_moy, ndigits=2)
            #                         #     # context['subj_cat'] = subj_cat
            #                         #     # context['total_prof_tot'] = total_prof_tot
            #                         #     # # context['avgTotal'] = "{:.2f}".format(invoiceTotal)

            #                         #     # print(context)

            #                         #     # # using now() to get current time
            #                         #     # current_time = datetime.datetime.now()

            #                         #     # report_card = ReportCard.objects.create(
            #                         #     #     student           = obj_student_class ,
            #                         #     #     term              = term,
            #                         #     #     student_rank      = my_rank,
            #                         #     #     gen_coeff         = total_gen_coeff,
            #                         #     #     prof_coeff        = total_prof_coeff,
            #                         #     #     gen_total         = subject_gen_tot,
            #                         #     #     prof_total        = total_prof_tot,
            #                         #     #     general_subjs_avr = round(gen_sub_moy, ndigits=2),
            #                         #     #     prof_subjs_avr    = round(prof_sub_moy, ndigits=2),
            #                         #     #     total_avr         = round(prof_gen_tot_moy, ndigits=2),
            #                         #     #     best_avr          = round(prof_gen_tot_moy, ndigits=2),
            #                         #     #     worst_avr         = round(prof_gen_tot_moy, ndigits=2),
            #                         #     #     firstterm_avr     = round(prof_gen_tot_moy, ndigits=2),
            #                         #     #     # academic_year = '2023/2024',
            #                         #     #     academic_year     = academic_yr,
            #                         #     #     resumption        = resumptn,
            #                         #     #     # teacher = teacher,
            #                         #     #     added_by          = added_by,
            #                         #     # )

            #                         #     # messages.success(request, f'{obj_student_class.name} Record Card added Successfully')
            #                         #     # return redirect("report_cards")
            #                         # if(term == 'second'):
            #                         #     # print("term")
            #                         #     # print('second')
            #                         #     # print(evals)
            #                         #     # testa = obj_eval_class.filter(title='Test1',subject_id=subject.id, student=student)
            #                         #     # testb = obj_eval_class.filter(title='Test2',subject_id=subject.id, student=student)
            #                         #     test_reslt = evals
            #                         #     # print("test_reslt")
            #                         #     # print(test_reslt)
            #                         #     # print('first')
            #                         #     if not test_reslt:
            #                         #         # print("no vale a")
            #                         #         testa_value = 0.0
            #                         #         messages.error(request, 'No Test Results Found')
            #                         #         return redirect('report_cards')
            #                         #     else:
            #                         #         # print("in")
            #                         #         # print(print(test_reslt))
            #                         #         if subject.category == 'General':
            #                         #             # testa_value = testa.value
            #                         #             testa_value = test_reslt.value
            #                         #             testb_value = test_reslt.sec_value
            #                         #                 #
                                        
            #                         #             total_eval = testa_value + testb_value
            #                         #             moyentt = total_eval / 2
            #                         #             # print(moyentt)

            #                         #             subj_moy = f"{subject.id}_{moyentt}_{subject.title}"
            #                         #             total_gen_coeff = total_gen_coeff + decimal.Decimal(evals.coef)
            #                         #             # total
            #                         #             moy_tot = moyentt  * int(evals.coef)
            #                         #             total_tot = total_tot + decimal.Decimal(moy_tot)
            #                         #             subj_moy_tot = f"{subject.title}_{subject.id}_{moyentt}_{moy_tot}"
            #                         #             total_gen_tot = total_gen_tot + moy_tot
            #                         #             subject_gen_tot = decimal.Decimal( subject_gen_tot) + moy_tot
            #                         #             total_gen_tot = total_gen_tot + total_tot
            #                         #         # print(subj_moy_tot)
            #                         #         # print(testb)
            #                         #         if subject.category == 'Professional':
            #                         #             testa_value = test_reslt.value
            #                         #             testb_value = test_reslt.sec_value
            #                         #                 #
                                        
            #                         #             total_eval = testa_value + testb_value
            #                         #             moyentt = total_eval / 2
            #                         #             # print(moyentt)

            #                         #             subj_moy = f"{subject.id}_{moyentt}_{subject.title}"
            #                         #             total_prof_coeff = total_prof_coeff + decimal.Decimal(evals.coef)
            #                         #             # total
            #                         #             moy_tot = moyentt  * int(evals.coef)
            #                         #             total_tot = total_tot + decimal.Decimal(moy_tot)
            #                         #             subj_moy_tot = f"{subject.title}_{subject.id}_{moyentt}_{moy_tot}"
            #                         #             total_gen_tot = total_gen_tot + moy_tot
            #                         #             subject_prof_tot = decimal.Decimal(subject_prof_tot) + moy_tot
            #                         #             total_prof_tot = total_prof_tot + moy_tot

            #                         #         # if(subject.category == 'General'):
            #                         #         #     total_gen_tot = total_gen_tot + total_tot
            #                         #         #     #
            #                         #         # if(subject.category == 'Professional'):
            #                         #         #     total_prof_tot = total_prof_tot + moy_tot
            #                         #         #
            #                         #         # subject_value_cat.append([test1.subject.title,testa_value,testb_value, moyentt, moy_tot,evals.coef, test2.observation, subject.category, test1.teacher])
            #                         #         subject_value_cat.append([test_reslt.subject.title,testa_value,testb_value, moyentt, moy_tot,evals.coef, test_reslt.observation, subject.category, test_reslt.teacher])
                                    

            #                         #     # total_coeff = decimal.Decimal(total_gen_coeff) + decimal.Decimal(total_prof_coeff)
                                        
                                        
            #                         #     # gen_sub_moy = decimal.Decimal(subject_gen_tot ) / decimal.Decimal(total_gen_coeff)
            #                         #     # prof_sub_moy = decimal.Decimal(subject_prof_tot ) / decimal.Decimal(total_prof_coeff)
            #                         #     # prof_gen_tot_moy = decimal.Decimal(total_tot ) / decimal.Decimal(total_coeff)

            #                         #     # # get rank
            #                         #     # my_rank = getstudent_rank(obj_student_class)
            #                         #     # # print(f"rank is {my_rank}")

            #                         #     # # get classavg
            #                         #     # my_classavg = get_classavg(classroom)
            #                         #     # # print(f"classavg is {my_classavg}")

            #                         #     # # get classavg
            #                         #     # my_countstud = count_stud_classspec( classroom, obj_student_class.specialty)
            #                         #     # # print(f"count stud in specialty is {my_countstud}")

                                        

            #                         #     # # get first term avg get_termavg(student, term, year="2024/2025")
            #                         #     # firt_term_avg = get_termavg(obj_student_class, "first", academic_yr)
            #                         #     # if firt_term_avg:
                                    #     #     print(f"first term avg is {firt_term_avg}")
            #                         #     # else: 
            #                         #     #     firt_term_avg = 0.00

            #                         #     # # get second term avg get_termavg(student, term, year="2024/2025")
            #                         #     # scnd_term_avg = get_termavg(obj_student_class, "second", academic_yr)
            #                         #     # if scnd_term_avg:
                                    #     #     print(f"second term avg is {scnd_term_avg}")
            #                         #     # else: 
            #                         #     #     scnd_term_avg = 0.00
                                        
            #                         #     # # get third term avg get_termavg(student, term, year="2024/2025")
            #                         #     # third_term_avg = get_termavg(obj_student_class, "third", academic_yr)
            #                         #     # if third_term_avg:
                                    #     #     print(f"third term avg is {third_term_avg}")
            #                         #     # else: 
            #                         #     #     third_term_avg = 0.00


            #                         #     # context = {}
            #                         #     # context['first_avg_term'] = firt_term_avg
            #                         #     # context['second_term_avg'] = scnd_term_avg
            #                         #     # context['third_avg_term'] = third_term_avg
            #                         #     # context['mi_rank'] = my_rank
            #                         #     # context['mi_class_avg'] = my_classavg
            #                         #     # context['spec_class_count_stud'] = my_countstud
            #                         #     # context['prof_sub_moy'] = round(prof_sub_moy, ndigits=2)
            #                         #     # context['prof_gen_tot_moy'] = round(prof_gen_tot_moy, ndigits=2)
            #                         #     # context['subject_line'] = subject_value_cat
            #                         #     # context['p_settings'] = p_settings
            #                         #     # context['student'] = obj_student_class
            #                         #     # context['classroom'] = classroom
            #                         #     # context['total_coeff'] = total_coeff
            #                         #     # context['total_tot'] = total_tot
            #                         #     # context['total_gen_coeff'] = total_gen_coeff
            #                         #     # context['total_prof_coeff'] = total_prof_coeff
            #                         #     # context['gen_tot'] = total_gen_tot
            #                         #     # context['subject_gen_tot'] = subject_gen_tot #gen total subj
            #                         #     # context['gen_sub_moy'] = round(gen_sub_moy, ndigits=2)
            #                         #     # context['subj_cat'] = subj_cat
            #                         #     # context['total_prof_tot'] = total_prof_tot
            #                         #     # # context['avgTotal'] = "{:.2f}".format(invoiceTotal)

            #                         #     # # print(context)

            #                         #     # # using now() to get current time
            #                         #     # current_time = datetime.datetime.now()

            #                         #     # report_card = ReportCard.objects.create(
            #                         #     #     student           = obj_student_class ,
            #                         #     #     term              = term,
            #                         #     #     student_rank      = my_rank,
            #                         #     #     gen_coeff         = total_gen_coeff,
            #                         #     #     prof_coeff        = total_prof_coeff,
            #                         #     #     gen_total         = subject_gen_tot,
            #                         #     #     prof_total        = total_prof_tot,
            #                         #     #     general_subjs_avr = round(gen_sub_moy, ndigits=2),
            #                         #     #     prof_subjs_avr    = round(prof_sub_moy, ndigits=2),
            #                         #     #     total_avr         = round(prof_gen_tot_moy, ndigits=2),
            #                         #     #     best_avr          = round(prof_gen_tot_moy, ndigits=2),
            #                         #     #     worst_avr         = round(prof_gen_tot_moy, ndigits=2),
            #                         #     #     firstterm_avr     = round(firt_term_avg, ndigits=2),
            #                         #     #     secondterm_avr    = round(prof_gen_tot_moy, ndigits=2),
            #                         #     #     # academic_year = '2023/2024',
            #                         #     #     academic_year     = academic_yr,
            #                         #     #     resumption        = resumptn,
            #                         #     #     # teacher = teacher,
            #                         #     #     added_by          = added_by,
            #                         #     # )

            #                         #     # messages.success(request, f'{obj_student_class.name} Record Card added Successfully')
            #                         #     # return redirect("report_cards")
            #                         # if(term == 'third'):
                                    #     print("term")
                                    #     print(term)
                                    #     print(evals)
            #                         #     # testa = obj_eval_class.filter(title='Test1',subject_id=subject.id, student=student)
            #                         #     # testb = obj_eval_class.filter(title='Test2',subject_id=subject.id, student=student)
            #                         #     test_reslt = evals
                                    #     print("test_reslt")
                                    #     print(test_reslt)
            #                         #     # print('first')
            #                         #     if not test_reslt:
            #                         #         # print("no vale a")
            #                         #         testa_value = 0.0
            #                         #         messages.error(request, 'No Test Results Found')
            #                         #         return redirect('report_cards')
            #                         #     else:
                                    #         print("in")
                                    #         print(print(test_reslt))
            #                         #         if subject.category == 'General':
            #                         #             # testa_value = testa.value
            #                         #             testa_value = test_reslt.value
            #                         #             testb_value = test_reslt.sec_value
            #                         #                 #
                                        
            #                         #             total_eval = testa_value + testb_value
            #                         #             moyentt = total_eval / 2
            #                         #             # print(moyentt)

            #                         #             subj_moy = f"{subject.id}_{moyentt}_{subject.title}"
            #                         #             total_gen_coeff = total_gen_coeff + decimal.Decimal(evals.coef)
            #                         #             # total
            #                         #             moy_tot = moyentt  * int(evals.coef)
            #                         #             total_tot = total_tot + decimal.Decimal(moy_tot)
            #                         #             subj_moy_tot = f"{subject.title}_{subject.id}_{moyentt}_{moy_tot}"
            #                         #             total_gen_tot = total_gen_tot + moy_tot
            #                         #             subject_gen_tot = decimal.Decimal(subject_gen_tot) + moy_tot
            #                         #             total_gen_tot = total_gen_tot + total_tot
            #                         #         # print(subj_moy_tot)
            #                         #         # print(testb)
            #                         #         if subject.category == 'Professional':
            #                         #             testa_value = test_reslt.value
            #                         #             testb_value = test_reslt.sec_value
            #                         #                 #
                                        
            #                         #             total_eval = testa_value + testb_value
            #                         #             moyentt = total_eval / 2
            #                         #             # print(moyentt)

            #                         #             subj_moy = f"{subject.id}_{moyentt}_{subject.title}"
            #                         #             total_prof_coeff = total_prof_coeff + decimal.Decimal(evals.coef)
            #                         #             # total
            #                         #             moy_tot = moyentt  * int(evals.coef)
            #                         #             total_tot = total_tot + decimal.Decimal(moy_tot)
            #                         #             subj_moy_tot = f"{subject.title}_{subject.id}_{moyentt}_{moy_tot}"
            #                         #             total_gen_tot = total_gen_tot + moy_tot
            #                         #             subject_prof_tot = decimal.Decimal(subject_prof_tot) + moy_tot
            #                         #             total_prof_tot = total_prof_tot + moy_tot

            #                         #         # if(subject.category == 'General'):
            #                         #         #     total_gen_tot = total_gen_tot + total_tot
            #                         #         #     #
            #                         #         # if(subject.category == 'Professional'):
            #                         #         #     total_prof_tot = total_prof_tot + moy_tot
            #                         #         #
            #                         #         # subject_value_cat.append([test1.subject.title,testa_value,testb_value, moyentt, moy_tot,evals.coef, test2.observation, subject.category, test1.teacher])
            #                         #         subject_value_cat.append([test_reslt.subject.title,testa_value,testb_value, moyentt, moy_tot,evals.coef, test_reslt.observation, subject.category, test_reslt.teacher])
                                    
            #                         #     # print(subject_value_cat)
                                                       

            #                         #     # print("subject_value_cat")            
            #                         #     # print(subject_value_cat)
            #                         #     # print("subject_gen_tot")
            #                         #     # print(subject_gen_tot)
            #                         #     # print("subject_prof_tot")
            #                         #     # print(subject_prof_tot)
            #                         #     # print("total_tot ")
            #                         #     # print(total_tot )

            #                         #     # total_coeff = decimal.Decimal(total_gen_coeff) + decimal.Decimal(total_prof_coeff)
                                        
                                        
            #                         #     # gen_sub_moy = decimal.Decimal(subject_gen_tot ) / decimal.Decimal(total_gen_coeff)
            #                         #     # prof_sub_moy = decimal.Decimal(subject_prof_tot ) / decimal.Decimal(total_prof_coeff)
            #                         #     # prof_gen_tot_moy = decimal.Decimal(total_tot ) / decimal.Decimal(total_coeff)

            #                         #     # # get rank
            #                         #     # my_rank = getstudent_rank(obj_student_class)
            #                         #     # print(f"rank is {my_rank}")

            #                         #     # # get classavg
            #                         #     # my_classavg = get_classavg(classroom)
            #                         #     # print(f"classavg is {my_classavg}")

            #                         #     # # get classavg
            #                         #     # my_countstud = count_stud_classspec( classroom, obj_student_class.specialty)
            #                         #     # print(f"count stud in specialty is {my_countstud}")

            #                         #     # # get first term avg get_termavg(student, term, year="2024/2025")
            #                         #     # firt_term_avg = get_termavg(obj_student_class, "first", academic_yr)
            #                         #     # if firt_term_avg:
                                    #     #     print(f"first term avg is {firt_term_avg}")
            #                         #     # else: 
            #                         #     #     firt_term_avg = 0.00

            #                         #     # # get second term avg get_termavg(student, term, year="2024/2025")
            #                         #     # scnd_term_avg = get_termavg(obj_student_class, "second", academic_yr)
            #                         #     # if scnd_term_avg:
                                    #     #     print(f"second term avg is {scnd_term_avg}")
            #                         #     # else: 
            #                         #     #     scnd_term_avg = 0.00
                                        
            #                         #     # # get third term avg get_termavg(student, term, year="2024/2025")
            #                         #     # third_term_avg = get_termavg(obj_student_class, "third", academic_yr)
            #                         #     # if third_term_avg:
                                    #     #     print(f"third term avg is {third_term_avg}")
            #                         #     # else: 
            #                         #     #     third_term_avg = 0.00


            #                         #     # context = {}
            #                         #     # context['first_avg_term'] = firt_term_avg
            #                         #     # context['second_term_avg'] = scnd_term_avg
            #                         #     # context['third_avg_term'] = third_term_avg
            #                         #     # context['mi_rank'] = my_rank
            #                         #     # context['mi_class_avg'] = my_classavg
            #                         #     # context['spec_class_count_stud'] = my_countstud
            #                         #     # context['prof_sub_moy'] = round(prof_sub_moy, ndigits=2)
            #                         #     # context['prof_gen_tot_moy'] = round(prof_gen_tot_moy, ndigits=2)
            #                         #     # context['subject_line'] = subject_value_cat
            #                         #     # context['p_settings'] = p_settings
            #                         #     # context['student'] = obj_student_class
            #                         #     # context['classroom'] = classroom
            #                         #     # context['total_coeff'] = total_coeff
            #                         #     # context['total_tot'] = total_tot
            #                         #     # context['total_gen_coeff'] = total_gen_coeff
            #                         #     # context['total_prof_coeff'] = total_prof_coeff
            #                         #     # context['gen_tot'] = total_gen_tot
            #                         #     # context['subject_gen_tot'] = subject_gen_tot #gen total subj
            #                         #     # context['gen_sub_moy'] = round(gen_sub_moy, ndigits=2)
            #                         #     # context['subj_cat'] = subj_cat
            #                         #     # context['total_prof_tot'] = total_prof_tot
            #                         #     # # context['avgTotal'] = "{:.2f}".format(invoiceTotal)

            #                         #     # print(context)

            #                         #     # # using now() to get current time
            #                         #     # current_time = datetime.datetime.now()

            #                         #     # report_card = ReportCard.objects.create(
            #                         #     #     student           = obj_student_class ,
            #                         #     #     term              = term,
            #                         #     #     student_rank      = my_rank,
            #                         #     #     gen_coeff         = total_gen_coeff,
            #                         #     #     prof_coeff        = total_prof_coeff,
            #                         #     #     gen_total         = subject_gen_tot,
            #                         #     #     prof_total        = total_prof_tot,
            #                         #     #     general_subjs_avr = round(gen_sub_moy, ndigits=2),
            #                         #     #     prof_subjs_avr    = round(prof_sub_moy, ndigits=2),
            #                         #     #     total_avr         = round(prof_gen_tot_moy, ndigits=2),
            #                         #     #     best_avr          = round(prof_gen_tot_moy, ndigits=2),
            #                         #     #     worst_avr         = round(prof_gen_tot_moy, ndigits=2),
            #                         #     #     firstterm_avr     = round(firt_term_avg, ndigits=2),
            #                         #     #     secondterm_avr    = round(scnd_term_avg, ndigits=2),
            #                         #     #     thirdterm_avr    = round(prof_gen_tot_moy, ndigits=2),
            #                         #     #     # academic_year = '2023/2024',
            #                         #     #     academic_year     = academic_yr,
            #                         #     #     resumption        = resumptn,
            #                         #     #     # teacher = teacher,
            #                         #     #     added_by          = added_by,
            #                         #     # )

            #                         #     # messages.success(request, f'{obj_student_class.name} Record Card added Successfully')
            #                         #     # return redirect("report_cards")
        
        
            # #                             #
            #             else:
            #                 messages.error(request, 'No Tests Record')
            #                 return redirect('report_cards')
                        
            #
            #
                            
            # total_coeff = decimal.Decimal(total_gen_coeff) + decimal.Decimal(total_prof_coeff)
                                            
                                            
            # gen_sub_moy = decimal.Decimal(subject_gen_tot ) / decimal.Decimal(total_gen_coeff)
            # prof_sub_moy = decimal.Decimal(subject_prof_tot ) / decimal.Decimal(total_prof_coeff)
            # prof_gen_tot_moy = decimal.Decimal(total_tot ) / decimal.Decimal(total_coeff)

            # # get rank
            # my_rank = getstudent_rank(obj_student_class)
            # print(f"rank is {my_rank}")

            # # get classavg
            # my_classavg = get_classavg(classroom)
            # print(f"classavg is {my_classavg}")

            # # get classavg
            # my_countstud = count_stud_classspec( classroom, obj_student_class.specialty)
            # print(f"count stud in specialty is {my_countstud}")



            # # get first term avg get_termavg(student, term, year="2024/2025")
            # firt_term_avg = get_termavg(obj_student_class, "first", academic_yr)
            # if firt_term_avg:
                # print(f"first term avg is {firt_term_avg}")
            # else: 
            #     firt_term_avg = 0.00

            # # get second term avg get_termavg(student, term, year="2024/2025")
            # scnd_term_avg = get_termavg(obj_student_class, "second", academic_yr)
            # if scnd_term_avg:
                # print(f"second term avg is {scnd_term_avg}")
            # else: 
            #     scnd_term_avg = 0.00
            
            # # get third term avg get_termavg(student, term, year="2024/2025")
            # third_term_avg = get_termavg(obj_student_class, "third", academic_yr)
            # if third_term_avg:
                # print(f"third term avg is {third_term_avg}")
            # else: 
            #     third_term_avg = 0.00

            
            # # get_subj_passedterm 
            # # passed subject count per term
            # passed_subj_first = get_subj_passedterm(obj_student_class, "first", academic_yr)
            
            # if passed_subj_first:
                # print(f"first term subj count is {passed_subj_first}")
            # else: 
            #     passed_subj_first = 0

            # passed_subj_second = get_subj_passedterm(obj_student_class, "second", academic_yr)
            
            # if passed_subj_second:
                # print(f"second term subj count is {passed_subj_second}")
            # else: 
            #     passed_subj_second = 0

            # passed_subj_third = get_subj_passedterm(obj_student_class, "third", academic_yr)
            
            # if passed_subj_third:
                # print(f"third term subj count is {passed_subj_third}")
            # else: 
            #     passed_subj_third = 0


            # context = {}
            # context['firstterm_subjpass'] = passed_subj_first
            # context['second_term_subjpass'] = passed_subj_second
            # context['third_avg_subjpass'] = passed_subj_third
            # context['first_avg_term'] = firt_term_avg
            # context['second_term_avg'] = scnd_term_avg
            # context['third_avg_term'] = third_term_avg
            # context['mi_rank'] = my_rank
            # context['mi_class_avg'] = my_classavg
            # context['spec_class_count_stud'] = my_countstud
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
            # # 
            # # check is report card exits
            # chec_card = ReportCard.objects.filter(term = term,student= obj_student_class,academic_year= academic_yr,is_actif=True).first()
            # if chec_card:
            #     chec_card.is_actif = False
            #     chec_card.modified_by = added_by
            #     chec_card.save()
            #     report_card = ReportCard.objects.create(
            #         student           = obj_student_class ,
            #         term              = term,
            #         student_rank      = my_rank,
            #         gen_coeff         = total_gen_coeff,
            #         prof_coeff        = total_prof_coeff,
            #         gen_total         = subject_gen_tot,
            #         prof_total        = total_prof_tot,
            #         general_subjs_avr = gen_sub_moy,
            #         prof_subjs_avr    = prof_sub_moy,
            #         total_avr         = prof_gen_tot_moy,
            #         best_avr          = my_beststud,
            #         worst_avr         = prof_gen_tot_moy,
            #         # firstterm_avr     = firt_term_avg["total_avg__max"],
            #         # secondterm_avr  = scnd_term_avg,
            #         # third_subj_passed     = third_term_avg,
            #         # first_subj_passed =  passed_subj_first,
            #         # second_subj_passed = passed_subj_second,
            #         # academic_year = '2023/2024',
            #         academic_year     = academic_yr,
            #         resumption        = resumptn,
            #         # teacher = teacher,
            #         added_by          = added_by,
            #     )
            # else:
            #     #

            #     report_card = ReportCard.objects.create(
            #         student           = obj_student_class ,
            #         term              = term,
            #         student_rank      = my_rank,
            #         gen_coeff         = total_gen_coeff,
            #         prof_coeff        = total_prof_coeff,
            #         gen_total         = subject_gen_tot,
            #         prof_total        = total_prof_tot,
            #         general_subjs_avr = gen_sub_moy,
            #         prof_subjs_avr    = prof_sub_moy,
            #         total_avr           = prof_gen_tot_moy,
            #         best_avr            = prof_gen_tot_moy,
            #         worst_avr           = prof_gen_tot_moy,
            #         # firstterm_avr       = firt_term_avg["total_avg__max"],
            #         # secondterm_avr  = scnd_term_avg,
            #         # third_subj_passed     = third_term_avg,
            #         # first_subj_passed =  passed_subj_first,
            #         # second_subj_passed = passed_subj_second,
            #         # # third_subj_passed =  passed_subj_third,
            #         # academic_year = '2023/2024',
            #         academic_year     = academic_yr,
            #         resumption        = resumptn,
            #         # teacher = teacher,
            #         added_by          = added_by,
            #     )
                
            # # 
            
            # print(f"firt_term_avg ----{firt_term_avg}")
            # print(firt_term_avg["total_avg__max"])
            # print(f"scnd_term_avg ----{scnd_term_avg}")
            # print(scnd_term_avg["total_avg__max"])
           
            # if term == "first":
            #     report_card.firstterm_avr = prof_gen_tot_moy
                
            #     if passed_subj_first:
            #         report_card.first_subj_passed = passed_subj_first
            #     report_card.modified_by = added_by
            #     report_card.save()
            # if term == "second":
            #     if firt_term_avg["total_avg__max"]:
            #         #
            #         report_card.firstterm_avr = firt_term_avg["total_avg__max"]
            #     if passed_subj_first:
            #         report_card.first_subj_passed = passed_subj_first
            #     if passed_subj_second:
            #         report_card.second_subj_passed = passed_subj_second
            #     report_card.secondterm_avr    =  prof_gen_tot_moy
            #     report_card.modified_by = added_by
            #     report_card.save()
                
            # if term == "third":
            #     if firt_term_avg["total_avg__max"]:
            #         #
            #         report_card.firstterm_avr = firt_term_avg["total_avg__max"]
            #     if scnd_term_avg["total_avg__max"]:
            #         #
            #         report_card.secondterm_avr = scnd_term_avg["total_avg__max"]
            #     if passed_subj_first:
            #         report_card.first_subj_passed = passed_subj_first
            #     if passed_subj_second:
            #         report_card.second_subj_passed = passed_subj_second
            #     if passed_subj_third:
            #         report_card.third_subj_passed = passed_subj_third
            #     report_card.thirdterm_avr    =  prof_gen_tot_moy
            #     report_card.modified_by = added_by
            #     report_card.save()
                
            


            # messages.success(request, f'{obj_student_class.name} Record Card added Successfully')
            # return redirect("report_cards")
    

        # else:
        #     messages.error(request, 'No Student Record')
        #     return redirect('report_cards')
    

        # print("subject_value_cat")            
        # print(subject_value_cat)
        # print("subject_gen_tot")
        # print(subject_gen_tot)
        # print("subject_prof_tot")
        # print(subject_prof_tot)
        # print("total_tot ")
        # print(total_tot )

        # total_coeff = decimal.Decimal(total_gen_coeff) + decimal.Decimal(total_prof_coeff)

        # # if subject_gen_tot == 0:
        # #     gen_sub_moy = 0
        
        # # else:
        # #     gen_sub_moy = subject_gen_tot / decimal.Decimal(total_gen_coeff)
        # # if subject_prof_tot == 0:
        # #     prof_sub_moy = 0
        # # else:
        # #     prof_sub_moy = subject_prof_tot / decimal.Decimal(total_prof_coeff)
        # # if total_tot == 0:
        # #     prof_gen_tot_moy = 0
        # # else:
        # #     prof_gen_tot_moy = total_tot / decimal.Decimal(total_coeff)
        
        
        # gen_sub_moy = decimal.Decimal(subject_gen_tot ) / decimal.Decimal(total_gen_coeff)
        # prof_sub_moy = decimal.Decimal(subject_prof_tot ) / decimal.Decimal(total_prof_coeff)
        # prof_gen_tot_moy = decimal.Decimal(total_tot ) / decimal.Decimal(total_coeff)
        
        
        # # gen_sub_moy = decimal.Decimal(subject_gen_tot ) / total_gen_coeff
        # # prof_sub_moy = decimal.Decimal(subject_prof_tot ) / total_prof_coeff
        # # prof_gen_tot_moy = decimal.Decimal(total_tot ) / total_coeff

        

        # # print(subject_value_cat)

        # # get rank
        # my_rank = getstudent_rank(obj_student_class)
        # print(f"rank is {my_rank}")

        # # get classavg
        # my_classavg = get_classavg(classroom)
        # print(f"classavg is {my_classavg}")

        # # get classavg
        # my_countstud = count_stud_classspec( classroom, obj_student_class.specialty)
        # print(f"count stud in specialty is {my_countstud}")



        # context = {}
        # context['mi_rank'] = my_rank
        # context['mi_class_avg'] = my_classavg
        # context['spec_class_count_stud'] = my_countstud
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
        #     student_rank      = my_rank,
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
                                        # print("term")
                                        # print(term)
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
                                        # print(term)
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
                                        # print(subj_moy)
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
                                        #     print(subject.category)
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


def viewDocumentInvoice(request, slug):
    #fetch that reportcard
    try:
        #get student class
        # print('student')
        obj_report_card = ReportCard.objects.get(id=slug)
        studentId = obj_report_card.student.id
        obj_student_class = Student.objects.get(id=studentId)
        # print(obj_student_class)
        # print(obj_student_class.specialty)
        current_academic_year = "2024/2025"

        classroomId = obj_student_class.student_class_id
        classroom =  ClassRoom.objects.get(id=classroomId)
        subjects = Subject.objects.filter(classroom=classroomId)
        # print(subjects)
        obj_eval_cl_type = TestMoySpecialtySubjClass.objects.filter(student_id=studentId, academic_year= current_academic_year, is_actif =True)
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

    # Create an empty of subjects and grade marks
    subject_grade_val = []

    # Create an empty of subjects and marks
    subj_cat = []

    # Create an empty of gen et prof
    subject_gen_tot = 0.0
    subject_prof_tot = 0.0

    subjt_rang = "1"

    # get reportcard details
    if obj_eval_cl_type:
        # print(f"obj_eval_cl_type ---{obj_eval_cl_type}")
        if(term == 'first'):
            # print(f"term---{term}")
            firstterm_reslts = Eval.objects.filter(student_id=studentId, academic_year= current_academic_year, titre="Eval1", is_actif =True)
            if firstterm_reslts:
                print(firstterm_reslts)
                for subject_tests in firstterm_reslts:
                    # print(f"subject_tests --- {subject_tests}")
                    moyentt = (subject_tests.value + subject_tests.sec_value) / 2
                    moy_tot = round((moyentt * subject_tests.coef), ndigits=2)
                    total_coeff = total_coeff + decimal.Decimal(subject_tests.coef)
                    total_tot = total_tot + decimal.Decimal(moy_tot)
                    if subject_tests.subject.category == "General":
                        # print(subject_tests.subject.category)
                        total_gen_tot = total_gen_tot + total_tot
                        subject_gen_tot = subject_gen_tot + float(moy_tot)
                        total_gen_coeff = total_gen_coeff + decimal.Decimal(subject_tests.coef)
                    if subject_tests.subject.category == "Professional":
                        # print(subject_tests.subject.category)
                        total_prof_tot = total_prof_tot + moy_tot
                        subject_prof_tot = subject_prof_tot + float(moy_tot)
                        total_prof_coeff = total_prof_coeff + decimal.Decimal(subject_tests.coef)
                    
                    # 
                    subject_value_cat.append([subject_tests.subject.title,subject_tests.value,subject_tests.sec_value, moyentt, subject_tests.coef, moy_tot, subject_tests.observation, subject_tests.subject.category, subject_tests.teacher])
        # 
        if(term == 'second'):
            # print(f"term---{term}")
            secondterm_reslts = Eval.objects.filter(student_id=studentId, academic_year= current_academic_year, title="Test3", is_actif =True)
            if secondterm_reslts:
                for subject_tests in secondterm_reslts:
                    # print(f"subject_tests --- {subject_tests}")
                    moyentt = (subject_tests.value + subject_tests.sec_value) / 2
                    grad_moyentt = grade_marks(moyentt)
                    # print(f"grad_moyentt --- {grad_moyentt}")
                    moy_tot = round((moyentt * subject_tests.coef), ndigits=2)
                    total_coeff = total_coeff + decimal.Decimal(subject_tests.coef)
                    total_tot = total_tot + decimal.Decimal(moy_tot)
                    if subject_tests.subject.category == "General":
                        # print(subject_tests.subject.category)
                        total_gen_tot = total_gen_tot + total_tot
                        subject_gen_tot = subject_gen_tot + float(moy_tot)
                        total_gen_coeff = total_gen_coeff + decimal.Decimal(subject_tests.coef)
                    if subject_tests.subject.category == "Professional":
                        # print(subject_tests.subject.category)
                        total_prof_tot = total_prof_tot + moy_tot
                        subject_prof_tot = subject_prof_tot + float(moy_tot)
                        total_prof_coeff = total_prof_coeff + decimal.Decimal(subject_tests.coef)
                    
                    # 
                    subject_value_cat.append([subject_tests.subject.title,subject_tests.value,subject_tests.sec_value, moyentt, subject_tests.coef, moy_tot, subject_tests.observation, subject_tests.subject.category, subject_tests.teacher])
                    subject_grade_val.append([subject_tests.subject.title,grad_moyentt])
        # 
        if(term == 'third'):
            # print(f"term---{term}")
            thirdterm_reslts = Eval.objects.filter(student_id=studentId, academic_year= current_academic_year, title="Test5", is_actif =True)
            if thirdterm_reslts:
                for subject_tests in thirdterm_reslts:
                    # print(f"subject_tests --- {subject_tests}")
                    moyentt = (subject_tests.value + subject_tests.sec_value) / 2
                    moy_tot = round((moyentt * subject_tests.coef), ndigits=2)
                    total_coeff = total_coeff + decimal.Decimal(subject_tests.coef)
                    total_tot = total_tot + decimal.Decimal(moy_tot)
                    if subject_tests.subject.category == "General":
                        # print(subject_tests.subject.category)
                        total_gen_tot = total_gen_tot + total_tot
                        subject_gen_tot = subject_gen_tot + float(moy_tot)
                        total_gen_coeff = total_gen_coeff + decimal.Decimal(subject_tests.coef)
                    if subject_tests.subject.category == "Professional":
                        # print(subject_tests.subject.category)
                        total_prof_tot = total_prof_tot + moy_tot
                        subject_prof_tot = subject_prof_tot + float(moy_tot)
                        total_prof_coeff = total_prof_coeff + decimal.Decimal(subject_tests.coef)
                    
                    # 
                    subject_value_cat.append([subject_tests.subject.title,subject_tests.value,subject_tests.sec_value, moyentt, subject_tests.coef, moy_tot, subject_tests.observation, subject_tests.subject.category, subject_tests.teacher])
        # 
        # print(subject_value_cat)
        # print(f"subject_gen_tot ----{subject_gen_tot}")
        # print(f"total_gen_coeff ----{total_gen_coeff}")

        if subject_gen_tot == 0 or total_gen_coeff == 0:
            gen_sub_moy = 0
        else:
            gen_sub_moy = decimal.Decimal(subject_gen_tot, ) / total_gen_coeff
        # prof_sub_moy = decimal.Decimal(subject_prof_tot, ) / total_prof_coeff

        if subject_prof_tot == 0 or total_prof_coeff == 0:
            prof_sub_moy = 0
        else:
            prof_sub_moy = decimal.Decimal(subject_prof_tot, ) / total_prof_coeff

        if total_tot == 0 or total_coeff == 0:
            prof_gen_tot_moy = 0
        else:
            prof_gen_tot_moy = decimal.Decimal(total_tot, ) / total_coeff

        

        # print(subject_value_cat)
        # get student image obj_student_class
        def display_image( obj):
            if obj.stud_image:
                img_url = image_services.get_image_url_from_cloudflare(
                    obj.stud_image.cloudflare_id, variant="thumbnailSmall"
                    # obj.stud_image.cloudflare_id
                )
                # print("obj")
                return img_url
            return "https://imagedelivery.net/FGazjujafzdf38AXQFJ0qw/834941c7-4e47-4404-a47c-c27bd18a4e00/thumbnailSmall"
        myimage = display_image(obj_student_class)

        meimage = "https://imagedelivery.net/FGazjujafzdf38AXQFJ0qw/834941c7-4e47-4404-a47c-c27bd18a4e00/thumbnailSmall"


        # get rank
        my_rank = getstudent_rank(obj_student_class)
        # print(f"rank is {my_rank}")

        # get classavg
        my_classavg = get_classavg(classroom, obj_student_class.specialty, term)
        # print(f"classavg is {my_classavg}")

        # get classavg
        my_countstud = count_stud_classspec( classroom, obj_student_class.specialty)
        # print(f"count stud in specialty is {my_countstud}")



        # get first term avg get_termavg(student, term, year="2024/2025")
        firt_term_avg = get_termavg(obj_student_class, "first", current_academic_year)
        if firt_term_avg:
            # print(f"first term avg is {firt_term_avg}")
            pass
        else: 
            firt_term_avg = 0.00

        # get second term avg get_termavg(student, term, year="2024/2025")
        scnd_term_avg = get_termavg(obj_student_class, "second", current_academic_year)
        if scnd_term_avg:
            # print(f"second term avg is {scnd_term_avg}")
            pass
        else: 
            scnd_term_avg = 0.00
        
        # get third term avg get_termavg(student, term, year="2024/2025")
        third_term_avg = get_termavg(obj_student_class, "third", current_academic_year)
        if third_term_avg:
            # print(f"third term avg is {third_term_avg}")
            pass
        else: 
            third_term_avg = 0.00


        context = {}
        context['first_avg_term'] = firt_term_avg
        context['second_term_avg'] = scnd_term_avg
        context['third_avg_term'] = third_term_avg
        context['mi_rank'] = my_rank
        context['mi_class_avg'] = my_classavg
        context['spec_class_count_stud'] = my_countstud
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
        context['academ_yr'] = obj_report_card.academic_year
        context['acad_resumption'] = obj_report_card.resumption
        context['total_prof_tot'] = total_prof_tot
        context['subject_grade'] = subject_grade_val
        # context['avgTotal'] = "{:.2f}".format(invoiceTotal)

        # print(f"academic_year {obj_report_card.academic_year}")
        # print(f"resumption {obj_report_card.resumption}")


        # test
        # print(context)

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
        # print(new_header)

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
    else:
        messages.error(request, 'No test result found')
        return redirect('report_cards')

   


# @login_required
def NOTGOODviewDocumentInvoice(request, slug):
    #fetch that reportcard
    try:
        #get student class
        # print('student')
        obj_report_card = ReportCard.objects.get(id=slug)
        studentId = obj_report_card.student.id
        obj_student_class = Student.objects.get(id=studentId)
        # print(obj_student_class)
        # print(obj_student_class.specialty)
        current_academic_year = "2024/2025"

        classroomId = obj_student_class.student_class_id
        classroom =  ClassRoom.objects.get(id=classroomId)
        subjects = Subject.objects.filter(classroom=classroomId)
        # print(subjects)
        obj_eval_class = Eval.objects.filter(student_id=studentId)
        obj_eval_cl_type = Eval.objects.filter(student_id=studentId, academic_year= current_academic_year)
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
            if subject is None:
                # print('no subjj coef')
                messages.error(request, 'Something went wrong')
                return redirect('report_cards')
            else:
                if obj_student_class:
                    if obj_eval_cl_type:
                        for evals in obj_eval_cl_type:
                                if evals.subject_id == subject.id:
                                    if(term == 'first'):
                                        subjt_rang = "1"
                                        # testa = obj_eval_class.filter(title='Test1',subject_id=subject.id)
                                        # testb = obj_eval_class.filter(title='Test2',subject_id=subject.id)
                                        get_testa = Eval.objects.filter(title="Test1",student_id=obj_student_class.id,subject_id = subject.id, academic_year=current_academic_year).first()
                                        # print('first')
                                        get_testa.value + get_testa.sec_value
                                        if not get_testa.value:
                                            # print("no vale a")
                                            testa_value = 0.0
                                        else:
                                            testa_value = get_testa.value
                                            # for test1 in testa:
                                            #     if(test1.subject_id == subject.id):
                                            #         testa_value = test1.value
                                                    #
                                        if not get_testa.sec_value:
                                            # print("no vale b")
                                            testb_value = 0.0
                                        else:
                                            testb_value = get_testa.sec_value
                                            # for test2 in testb:
                                            #     if(test2.subject_id == subject.id):
                                            #         testb_value = test2.value
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
                                        # print(term)
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
                                            print(subject.category)
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
    
        # print(f"subject_gen_tot ----{subject_gen_tot}")
        # print(f"total_gen_coeff ----{total_gen_coeff}")
        
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
                # print("obj")
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
        # print(new_header)

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
    
    else:
            messages.error(request, 'No Subject found Record')
            return redirect('report_cards')





# @login_required
def viewDocumentInvoiceERRUR(request, slug):
    #fetch that reportcard
    try:
        #get student class
        # print('student')
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
                    # print(term)
                    # print(testa.teacher)
                    # print(testb)
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
                    # print(subj_moy)
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
                        print(subject.category)
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
        # print('student')
        obj_student_class = Student.objects.get(id=student)

        classroomId = obj_student_class.student_class_id
        classroom =  ClassRoom.objects.get(id=classroomId)

        #get test
        # print('test')
        obj_eval_class = Eval.objects.filter(student_id=student)
        # print(obj_eval_class)

        #get subject
        # print('subject')
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
            # print(results)
        else:
            for subjj_cl in results:
                # print(subjj_cl.id)
                # print(subjj_cl.coef)
                if subjj_cl.coef is None:
                    print('no subjj coef')
                else:
                    if(subjj_cl.category == 'General'):
                        # print(f"General {subjj_cl.coef}")
                        total_gen_coeff = total_gen_coeff + decimal.Decimal(subjj_cl.coef)
                        # total_gen_tot = total_gen_tot + decimal.Decimal(subjj_cl.coef)
                    #)
                    if(subjj_cl.category == 'Professional'):
                        # print(f"Professional {subjj_cl.coef}")
                        total_prof_coeff = total_prof_coeff + decimal.Decimal(subjj_cl.coef)
                    #
                    if(term == 'first'):
                        testa = obj_eval_class.filter(title='Test1',subject_id=subjj_cl.id)
                        testb = obj_eval_class.filter(title='Test2',subject_id=subjj_cl.id)
                        # print('first')
                        if not testa:
                            # print("no vale a")
                            testa_value = 0.0
                        else:
                            for test1 in testa:
                                if(test1.subject_id == subjj_cl.id):
                                    testa_value = test1.value
                        if not testb:
                            # print("no vale b")
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
                        # print(subj_moy_tot)
                        # print(testb)
                        if(subjj_cl.category == 'General'):
                            total_gen_tot = total_gen_tot + total_tot

                    if(term == 'second'):
                        testa = obj_eval_class.filter(title='Test3').filter(subject_id=subjj_cl.id)
                        testb = obj_eval_class.filter(title='Test4',subject_id=subjj_cl.id)
                        # print('test3')
                        # print(testa.filter(subject_id=subjj_cl.id))
                        if not testa:
                            # print("no vale a")
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
                            # print("no vale b")
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
                        # print(subj_moy)

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
                        # print(subj_moy_tot)

                        # print('test4')
                        # print(testb)
                        if(subjj_cl.category == 'General'):
                            total_gen_tot = total_gen_tot + total_tot

                    if(term == 'third'):
                        testa = obj_eval_class.filter(title='Test5')
                        testb = obj_eval_class.filter(title='Test6')
                        # print('first')
                        if not testa:
                            # print("no vale a")
                            testa_value = 0.0
                        else:
                            for test1 in testa:
                                if(test1.subject_id == subjj_cl.id):
                                    testa_value = test1.value
                        if not testb:
                            # print("no vale b")
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
                        # print(subj_moy_tot)
                        # print(testb)
                        if(subjj_cl.category == 'General'):
                            total_gen_tot = total_gen_tot + total_tot
            #

            #total
            # print(total_coeff)
            # print(total_tot)
            # print("general")
            # print(total_gen_coeff)
            # print(f"General tot: {total_gen_tot}")
            # print("prof")
            # print(total_prof_coeff)
        

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
        # print('student')
        obj_student_class = Student.objects.get(id=student)

        classroomId = obj_student_class.student_class_id
        classroom =  ClassRoom.objects.get(id=classroomId)

        #get test
        # print('test')
        obj_eval_class = Eval.objects.filter(student_id=student)
        # print(obj_eval_class)

        #get subject
        # print('subject')
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
            # print(results)
        else:
            for subjj_cl in results:
                # print(subjj_cl.id)
                # print(subjj_cl.coef)
                if subjj_cl.coef is None:
                    print('no subjj coef')
                else:
                    if(subjj_cl.category == 'General'):
                        # print(f"General {subjj_cl.coef}")
                        total_gen_coeff = total_gen_coeff + decimal.Decimal(subjj_cl.coef)
                        # total_gen_tot = total_gen_tot + decimal.Decimal(subjj_cl.coef)
                    #)
                    if(subjj_cl.category == 'Professional'):
                        # print(f"Professional {subjj_cl.coef}")
                        total_prof_coeff = total_prof_coeff + decimal.Decimal(subjj_cl.coef)
                    #
                    if(term == 'first'):
                        testa = obj_eval_class.filter(title='Test1',subject_id=subjj_cl.id)
                        testb = obj_eval_class.filter(title='Test2',subject_id=subjj_cl.id)
                        # print('first')
                        if not testa:
                            # print("no vale a")
                            testa_value = 0.0
                        else:
                            for test1 in testa:
                                if(test1.subject_id == subjj_cl.id):
                                    testa_value = test1.value
                        if not testb:
                            # print("no vale b")
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
                        # print(subj_moy_tot)
                        # print(testb)
                        if(subjj_cl.category == 'General'):
                            total_gen_tot = total_gen_tot + total_tot

                    if(term == 'second'):
                        testa = obj_eval_class.filter(title='Test3').filter(subject_id=subjj_cl.id)
                        testb = obj_eval_class.filter(title='Test4',subject_id=subjj_cl.id)
                        # print('test3')
                        # print(testa.filter(subject_id=subjj_cl.id))
                        if not testa:
                            # print("no vale a")
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
                            # print("no vale b")
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
                        # print(subj_moy)

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
                        # print(subj_moy_tot)

                        # print('test4')
                        # print(testb)
                        if(subjj_cl.category == 'General'):
                            total_gen_tot = total_gen_tot + total_tot

                    if(term == 'third'):
                        testa = obj_eval_class.filter(title='Test5')
                        testb = obj_eval_class.filter(title='Test6')
                        # print('first')
                        if not testa:
                            # print("no vale a")
                            testa_value = 0.0
                        else:
                            for test1 in testa:
                                if(test1.subject_id == subjj_cl.id):
                                    testa_value = test1.value
                        if not testb:
                            # print("no vale b")
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
                        # print(subj_moy_tot)
                        # print(testb)
                        if(subjj_cl.category == 'General'):
                            total_gen_tot = total_gen_tot + total_tot
            #

            #total
            # print(total_coeff)
            # print(total_tot)
            # print("general")
            # print(total_gen_coeff)
            # print(f"General tot: {total_gen_tot}")
            # print("prof")
            # print(total_prof_coeff)
        

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



def has_stud_pass(avg):
    #check is avg is a pass mark
    if avg > 10.00:
        return True
    else:
        return False



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
        # print(f"num of girls in form 1 is {count_girl_form1}")

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
            # print(term)
        # elif term == "second":
            # print(term)
        #     #get the test relatives too students
        # elif term == "third":
            # print(term)
        
        # if type == "consolidation":
            # print(type)
        #     # pdf_heading = ""
        # elif type == "non_consolidation":
            # print(type)
        
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
        # print(data_non_consolidation)

        # print("num_specialties")
        num_specialties = num_specialties + 2
        # print(num_specialties)



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




