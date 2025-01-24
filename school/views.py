from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse

from core.models import CustomUser
from subject.models import Subject
from student.models import Student
# from .models import Notification
from .models import ClassRoom, Settings, Specialty

from .models import Settings
from django.http import HttpResponseForbidden
from django.contrib import messages



# Create your views here.
def index(request):
    return render(request, "authentication/login.html")
    # return render(request, "home/index.html")

def dashboard(request):
    company = Settings.objects.get(clientName='GILEAD TECHNICAL HIGH SCHOOL(Gilead Tech)')
    user_info = Student.objects.get(id=request.user.student_profile.id)
    class_info = ClassRoom.objects.get(id=user_info.student_class.id)
    class_subjects = Subject.objects.filter(classroom=class_info.id)
    num_subjects = Subject.objects.filter(classroom=class_info.id).count()
    print(num_subjects)
    #get number of subjects
    user_class = user_info.student_class.class_name
    print(user_info.student_image.url)
    context = {
        'user_info': user_info,
        "user_class" : user_class,
        'company': company,
        "class_info" : class_info,
        "class_subjects" : class_subjects,
        "num_subjects" : num_subjects,
    }
    # unread_notification = Notification.objects.filter(user=request.user, is_read=False)
    # unread_notification_count = unread_notification.count()
    return render(request, "dashboard/student-dashboard.html", context)


def admin_dashboard(request):
    company = Settings.objects.get(clientName='GILEAD TECHNICAL HIGH SCHOOL(Gilead Tech)')
    classroom = ClassRoom.objects.all()
    count_class = ClassRoom.objects.all().count()
    count_subjects = Subject.objects.all().count()
    context = {
        'company': company,
        "classroom" : classroom,
        "count_class" : count_class,
        "count_subjects" : count_subjects,
    }
    # unread_notification = Notification.objects.filter(user=request.user, is_read=False)
    # unread_notification_count = unread_notification.count()
    return render(request, "dashboard/admin-dashboard.html", context)



def teacher_dashboard(request):
    company = Settings.objects.get(clientName='GILEAD TECHNICAL HIGH SCHOOL(Gilead Tech)')
    user_info = Student.objects.get(id=request.user.student_profile.id)
    class_info = ClassRoom.objects.get(id=user_info.student_class.id)
    class_subjects = Subject.objects.filter(classroom=class_info.id)
    num_subjects = Subject.objects.filter(classroom=class_info.id).count()
    print(num_subjects)
    #get number of subjects
    user_class = user_info.student_class.class_name
    print(user_info.student_image.url)
    context = {
        'user_info': user_info,
        "user_class" : user_class,
        'company': company,
        "class_info" : class_info,
        "class_subjects" : class_subjects,
        "num_subjects" : num_subjects,
    }
    # unread_notification = Notification.objects.filter(user=request.user, is_read=False)
    # unread_notification_count = unread_notification.count()
    return render(request, "dashboard/student-dashboard.html", context)


def class_list(request):
    class_list = ClassRoom.objects.all()
    context = {
        'class_list': class_list,
    }
    return render(request, "class/classes.html", context)


def add_class(request):

    if request.method == "POST":
        name      = request.POST.get('name')
        code      = request.POST.get('code')
        dept       = request.POST.get('dept')
        added_by     = request.user.username,
        # added_by = "emnanlaptop"
        # obj_student_class = ClassRoom.objects.filter(classroom)

        classroom = ClassRoom.objects.create(
            class_name = name,
            class_code = code,
            class_department = dept,
            added_by = request.user.username,
        )
        classroom.save()

        messages.success(request, 'Class added Successfully')
        return redirect("class_list")
    return render(request, "class/add-class.html")




def edit_class(request, slug):
    # classroom = ClassRoom.objects.get(id=slug)
    # context = {
    #     'classroom': classroom,
    # }
    class_room = get_object_or_404(ClassRoom, id=slug)
    context = {
        'classroom':class_room,
    }

    if request.method == "POST":
        name      = request.POST.get('name')
        code      = request.POST.get('code')
        dept       = request.POST.get('dept')
        modified_by     = request.user.username,

        # 
        # obj_student_class = ClassRoom.objects.filter(classroom)

        
        class_room.class_name = name
        class_room.class_code = code
        class_room.class_department = dept
        # description = description,
        class_room.modified_by = modified_by

        # class_room.update()

        
        class_room.save()

        messages.success(request, 'Class updated Successfully')
        return redirect("class_list")
    return render(request, "class/edit-class.html", context) 


def del_class(request, slug):
    if request.method == "POST":
        #
        classroom = get_object_or_404(ClassRoom, id = slug)
        classroom.delete()

        return redirect('class_list')
    return HttpResponseForbidden()





def specialty_list(request):
    specialty_list = Specialty.objects.all()
    context = {
        'specialty_list': specialty_list,
    }
    return render(request, "specialty/specialty.html", context)


def add_specialty(request):

    if request.method == "POST":
        name      = request.POST.get('name')
        code      = request.POST.get('code')
        # classroom      = request.POST.get('classroom')
        dept       = request.POST.get('dept')
        # other       = request.POST.get('other')
        added_by     = request.user.username,
        # added_by = "emnanlaptop"
        # obj_student_class = ClassRoom.objects.filter(classroom)

        specialty = Specialty.objects.create(
            class_name = name,
            class_code = code,
            class_department = dept,
            added_by = added_by,
        )

        # obj_class = Specialty.objects.get(id=classroom)

        # specialty.classroom.add(obj_class)
        specialty.save()

        messages.success(request, 'specialty added Successfully')
        return redirect("specialty_list")
    return render(request, "specialty/add-specialty.html")




def edit_specialty(request, slug):
    # classroom = ClassRoom.objects.get(id=slug)
    # context = {
    #     'classroom': classroom,
    # }
    specialty = get_object_or_404(Specialty, id=slug)
    context = {
        'specialty':specialty,
    }

    if request.method == "POST":
        name      = request.POST.get('name')
        code      = request.POST.get('code')
        # classroom      = request.POST.get('classroom')
        dept       = request.POST.get('dept')
        modified_by     = request.user.username,

        # 
        # obj_student_class = ClassRoom.objects.filter(classroom)

        
        specialty.class_name = name
        specialty.class_code = code
        specialty.class_department = dept
        # description = description,
        specialty.modified_by = modified_by

        # specialty.update()

        # obj_class = Specialty.objects.get(id=classroom)

        # specialty.classroom.add(obj_class)

        
        specialty.save()

        messages.success(request, 'Specialty updated Successfully')
        return redirect("specialty_list")
    return render(request, "specialty/edit-specialty.html", context) 


def del_specialty(request, slug):
    if request.method == "POST":
        #
        specialty = get_object_or_404(Specialty, id = slug)
        specialty.delete()

        return redirect('specialty_list')
    return HttpResponseForbidden()




def companySettings(request):
    company = Settings.objects.get(clientName='GILEAD TECHNICAL HIGH SCHOOL(Gilead Tech)')
    context = {'company': company}
    return render(request, 'company/company-settings.html', context)




