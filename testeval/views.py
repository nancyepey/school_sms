
import html
from django.conf import settings
from django.shortcuts import render
#
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
# from sympy import Sum
from django.db.models import Sum
import decimal
from school.models import ClassRoom, Settings

from .models import Eval, ReportCard
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
import os
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
    context = {
        'subject':subject,
        'student':student,
    }

    if request.method == "POST":
        title = request.POST.get('title')
        titre = request.POST.get('titre')
        student = request.POST.get('student')
        value = request.POST.get('value')
        coef = request.POST.get('coeff')
        subject = request.POST.get('subject')
        teacher = "teacher"
        remarks = request.POST.get('remarks')
        added_by = "emnanlaptop"

        #get student class
        print('student')
        obj_student_class = Student.objects.get(id=student)

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




def edit_test(request, slug):
    eval = get_object_or_404(Eval, id=slug)
    # student = get_object_or_404(Student, id=slug)
    student = Student.objects.all()
    subject = Subject.objects.all()
    # parent = student.parent if hasattr(student, 'parent') else None
    context = {'eval':eval, 'student':student, 'subject':subject}
    if request.method == "POST":
        # first_name = request.POST.get('first_name')
        title = request.POST.get('title')
        titre = request.POST.get('titre')
        student = request.POST.get('student')
        value = request.POST.get('value')
        coef = request.POST.get('coeff')
        subject = request.POST.get('subject')
        teacher = "teacher"
        remarks = request.POST.get('remarks')

        #get student class
        print('student')
        obj_student_class = Student.objects.get(id=student)

        #get subject class
        print('subject')
        obj_subject_class = Subject.objects.get(id=subject)

        
        eval.title = title
        eval.titre = titre
        eval.value = value
        eval.coef = coef
        eval.subject = obj_subject_class
        eval.observation = remarks
        eval.student = obj_student_class
        eval.teacher = teacher
        eval.modified_by = "emnanlaptop"
        eval.save()
        
        
        return redirect("test_list")
    return render(request, "eval/edit-eval.html", context )






def delete_test(request, slug):
    if request.method == "POST":
        #
        student = get_object_or_404(Student, id = slug)
        student.delete()

        return redirect('_test')
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


def create_report_card(request):
    # eval = Eval.objects.all()
    student = Student.objects.all()
    context = {
        'student':student,
    }

    if request.method == "POST":
        student = request.POST.get('student')
        term = request.POST.get('term')
        added_by = "emnanlaptop"

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
                        total_eval = testa_value + testb_value
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
                academic_year = '2023/2024',
                # teacher = teacher,
                added_by = added_by,
            )

        # messages.success(request, 'Eval added Successfully')
        # return redirect("test_list")
    

    return render(request, "reports/add-card.html", context=context)


def generate_pdf(request):
    response = FileResponse(generate_pdf_file(), 
                            as_attachment=True, 
                            filename='book_catalog.pdf')
    return response
 
 
def generate_pdf_file():
    from io import BytesIO
 
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
 
    # Create a PDF document
    reportCards = ReportCard.objects.all()
    p.drawString(100, 750, "ReportCard Catalog")
 
    y = 700
    for reportCard in reportCards:
        p.drawString(100, y, f"Title: {reportCard.student.name}")
        p.drawString(100, y - 20, f"Author: {reportCard.student_rank}")
        p.drawString(100, y - 40, f"Year: {reportCard.academic_year}")
        p.rect(0.2*inch,0.2*inch,1*inch,1.5*inch, fill=1)

        y -= 60

        #
 
    p.showPage()
    p.save()
 
    buffer.seek(0)
    return buffer




def viewDocumentInvoice(request, slug):
    #fetch that reportcard
    try:
        #get student class
        print('student')
        obj_report_card = ReportCard.objects.get(id=slug)
        studentId = obj_report_card.student.id
        obj_student_class = Student.objects.get(id=studentId)

        classroomId = obj_student_class.student_class_id
        classroom =  ClassRoom.objects.get(id=classroomId)
        subjects = Subject.objects.filter(classroom=classroomId)
        obj_eval_class = Eval.objects.filter(student_id=studentId)
        # print(results)
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
    p_settings = Settings.objects.get(clientName='GILEAD TECHNICAL HIGH SCHOOL(Gilead Tech)')

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
                print('no subjj coef')
                messages.error(request, 'Something went wrong')
                return redirect('report_cards')
            else:
                if(subject.category == 'General'):
                    print(f"General {subject.coef}")
                    total_gen_coeff = total_gen_coeff + decimal.Decimal(subject.coef)
                    subj_cat.append(subject.category)
                    # total_gen_tot = total_gen_tot + decimal.Decimal(subject.coef)
                #)
                if(subject.category == 'Professional'):
                    print(f"Professional {subject.coef}")
                    total_prof_coeff = total_prof_coeff + decimal.Decimal(subject.coef)
                    subj_cat.append(subject.category)
                #
                if(term == 'first'):
                    subjt_rang = "1"
                    testa = obj_eval_class.filter(title='Test1',subject_id=subject.id)
                    testb = obj_eval_class.filter(title='Test2',subject_id=subject.id)
                    # print('first')
                    if not testa:
                        print("no vale a")
                        testa_value = 0.0
                    else:
                        for test1 in testa:
                            if(test1.subject_id == subject.id):
                                testa_value = test1.value
                                #
                    if not testb:
                        print("no vale b")
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
                    print(subj_moy_tot)
                    # print(testb)
                    if(subject.category == 'General'):
                        total_gen_tot = total_gen_tot + total_tot
                        #
                    if(subject.category == 'Professional'):
                        total_prof_tot = total_prof_tot + moy_tot
                        #
                    subject_value_cat.append([test1.subject.title,testa_value,testb_value, moyentt, moy_tot,subject.coef, test2.observation, subject.category, test1.teacher])
                    #
                if(term == 'second'):
                    subjt_rang = "1"
                    testa = obj_eval_class.filter(title='Test3',subject_id=subject.id)
                    testb = obj_eval_class.filter(title='Test4',subject_id=subject.id)
                    # print('first')
                    if not testa:
                        print("no vale a")
                        testa_value = 0.0
                    else:
                        for test1 in testa:
                            if(test1.subject_id == subject.id):
                                testa_value = test1.value
                    if not testb:
                        print("no vale b")
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
                    print(subj_moy_tot)
                    # print(testb)
                    if(subject.category == 'General'):
                        total_gen_tot = total_gen_tot + total_tot
                        subject_gen_tot = subject_gen_tot + float(moy_tot)
                    if(subject.category == 'Professional'):
                        # total_gen_tot = total_gen_tot + total_tot
                        subject_prof_tot = subject_prof_tot + float(moy_tot)
                        total_prof_tot = total_prof_tot + moy_tot
                        #
                    if(test1.subject.title == "English Langauge"):
                        print(subject.category)
                        #
                    subject_value_cat.append([test1.subject.title,testa_value,testb_value, moyentt, subject.coef, moy_tot, test2.observation, subject.category, test1.teacher])
                    #
                if(term == 'third'):
                    subjt_rang = "1"
                    testa = obj_eval_class.filter(title='Test5',subject_id=subject.id)
                    testb = obj_eval_class.filter(title='Test6',subject_id=subject.id)
                    # print('first')
                    if not testa:
                        print("no vale a")
                        testa_value = 0.0
                    else:
                        for test1 in testa:
                            if(test1.subject_id == subject.id):
                                testa_value = test1.value
                    if not testb:
                        print("no vale b")
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
                    print(subj_moy_tot)
                    # print(testb)
                    if(subject.category == 'General'):
                        total_gen_tot = total_gen_tot + total_tot
                    if(subject.category == 'Professional'):
                        total_prof_tot = total_prof_tot + moy_tot
                        #
                    subject_value_cat.append([test1.subject.title,testa_value,testb_value, moyentt, moy_tot, subject.coef, test2.observation, subject.category,  test1.teacher])

            # y = float(x.quantity) * float(x.price)
            # invoiceTotal += y
    
    gen_sub_moy = decimal.Decimal(subject_gen_tot, ) / total_gen_coeff
    prof_sub_moy = decimal.Decimal(subject_prof_tot, ) / total_prof_coeff
    prof_gen_tot_moy = decimal.Decimal(total_tot, ) / total_coeff



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
    path_wkthmltopdf = b'C:\wkhtmltopdf\\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    # config = pdfkit.configuration(wkhtmltopdf='C:/wkhtmltopdf/bin/wkhtmltopdf')

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

