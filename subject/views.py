import csv
import datetime
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render


from subject.admin import SubjectResource
from school.models import ClassRoom, Specialty
from subject.models import Subject
#search
from django.db.models import Q
# csv
import csv 
from django.utils.text import slugify
import os
from tablib import Dataset
from school.admin import SpecialtyResource
from subject.forms import CSVSubjectImportForm
from django.http import HttpResponse
import pandas as pd

#login required
from django.contrib.auth.decorators import login_required



# Create your views here.
@login_required
def subject_list(request):
    subject_list = Subject.objects.prefetch_related('classroom').all()
    
    form = CSVSubjectImportForm()

    # search
    if 'q' in request.GET:
        search=request.GET['q']
        subject_list =  Subject.objects.filter(Q(title__icontains = search) | Q(fr_title__icontains = search) | Q(subject_code__icontains = search) | Q(description__icontains = search)  )

    context = {
        'subject_list': subject_list,
        'csv_subject_import_form': form,
    }
    # import
    if request.method == 'POST':
        # print(request)
        form = CSVSubjectImportForm(request.POST, request.FILES)
        if form.is_valid():
            print("importttttttttt")
            csv_file = request.FILES['csv_file']
            csv_reader = pd.read_excel(csv_file, engine="openpyxl")
            # 

            file = request.FILES['csv_file']
            df = pd.read_excel(file)

            """Rename the headeers in the excel file
           to match Django models fields"""

            #Call the Subject Resource Model and make its instance
            subjects_resource = SubjectResource()

            # Load the pandas dataframe into a tablib dataset
            dataset = Dataset().load(csv_reader)
            # dataset = Dataset().load(df)

            # Call the import_data hook and pass the tablib dataset
            result = subjects_resource.import_data(dataset,\
             dry_run=True, raise_errors = True)
            
            if not result.has_errors():
                result = subjects_resource.import_data(dataset, dry_run=False)
                messages.success(request, "Subject Data imported successfully")
                # return Response({"status": "Subject Data Imported Successfully"})
                # return redirect('index')
                #
            
            else:
                messages.error(request, "Not Imported Subject Data")
            #

    return render(request, "subjects/subjects.html", context)


@login_required
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
        classroom = request.POST.get('subject_class')
        specialty = request.POST.get('specialty')
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

        #

        # count_class = 0
        # print("classroom")
        # print(classroom)
        # for classr in classroom:
        #     # print(classr)
        #     obj_class = ClassRoom.objects.get(id=classr)
        #     subject.classroom.add(obj_class)
        #     count_class += 1
        # # print(count_class)

        # count_specialty = 0
        # for specialt in specialty:
        #     # print(specialt)
        #     specialty_obj_class = Specialty.objects.get(id=specialt)
        #     subject.specialty.add(specialty_obj_class)
        #     count_specialty += 1


        # print(count_specialty)

        # count = 0
        # for e in classroom:
        #     obj_class = ClassRoom.objects.get(id=e)
        #     # subject.classroom.add(obj_class)
        #     subject.classroom.m2m.add(obj_class)
        #     count += 1

        obj_class = ClassRoom.objects.get(id=classroom)
        specialty_obj_class = Specialty.objects.get(id=specialty)

        subject.classroom.add(obj_class)
        subject.specialty.add(specialty_obj_class)

        subject.save()

        messages.success(request, f'{title} Subject added Successfully')
        return redirect("subject_list")
    
    return render(request, "subjects/add-subject.html", context)


@login_required
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
        subj_all = subject.classroom.all()
        print(subj_all)
        # subj_all.clear()
        print(subj_all)
        spec_all = subject.specialty.all()
        print(spec_all)
        # spec_all.clear()
        print(spec_all)
        title           = request.POST.get('subject_title')
        # title = request.POST.get('subject_title')
        fr_title        = request.POST.get('subject_title_fren')
        coef            = request.POST.get('coeff')
        subject_code    = request.POST.get('subject_code')
        classroom       = request.POST.getlist('subject_class')
        
        description     = request.POST.get('description')
        category = request.POST.get('category')
        specialty = request.POST.getlist('specialty')
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

        messages.success(request, f'{title} Subject updated Successfully')
        return redirect("subject_list")
    
    return render(request, "subjects/edit-subject.html", context)


@login_required
def view_subject(request, slug):
    subject = get_object_or_404(Subject, id = slug)
    context = {
        'subject': subject
    }
    return render(request, "subjects/subject-details.html", context)


@login_required
def delete_subject(request, slug):
    if request.method == "POST":
        #
        subject = get_object_or_404(Subject, id = slug)
        subject.delete()

        return redirect('subject_list')
    return HttpResponseForbidden()


@login_required
def subjects_generate_csv(request): 
    response = HttpResponse(content_type='text/csv') 
    formatted_datetime = datetime.datetime.now()
    file_name = f"subjects_{formatted_datetime}.csv"
    response['Content-Disposition'] = f'attachment; filename={file_name}'

    response.write(u'\ufeff'.encode('utf8'))
  
    writer = csv.writer(response) 
    writer.writerow(["title", "fr_title",  "coef", "subject_code", "description","category","slug","added_by" ]) 
    # writer.writerow(["title", "fr_title",  "coef", "subject_code", "description","category" ]) 
    # 

    subjects = Subject.objects.all() 
    for subjj in subjects: 
        # print("subjj_")
        # print(subjj)
            
        writer.writerow([ subjj.title, subjj.fr_title, subjj.coef,  subjj.subject_code, subjj.description, subjj.category, subjj.slug, subjj.added_by]) 
        # writer.writerow([ subjj.title, subjj.fr_title, subjj.coef, subjj.description, subjj.category]) 
        # 
  
    return response 


