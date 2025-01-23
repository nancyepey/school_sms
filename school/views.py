from django.shortcuts import render
from django.http import HttpResponse

from core.models import CustomUser
from student.models import Student
# from .models import Notification
from .models import ClassRoom, Settings

from .models import Settings

# Create your views here.
def index(request):
    return render(request, "authentication/login.html")
    # return render(request, "home/index.html")

def dashboard(request):
    company = Settings.objects.get(clientName='GILEAD TECHNICAL HIGH SCHOOL(Gilead Tech)')
    user_info = Student.objects.get(id=request.user.student_profile.id)
    #get number of subjects
    user_class = user_info.student_class.class_name
    print(user_info.student_image.url)
    context = {
        'user_info': user_info,
        "user_class" : user_class,
        'company': company
    }
    # unread_notification = Notification.objects.filter(user=request.user, is_read=False)
    # unread_notification_count = unread_notification.count()
    return render(request, "dashboard/student-dashboard.html", context)



def class_list(request):
    return render(request, "class/classes.html")


def add_class(request):
    return render(request, "class/add-class.html")




def edit_class(request, slug):
    return render(request, "class/edit-class.html")


def companySettings(request):
    company = Settings.objects.get(clientName='GILEAD TECHNICAL HIGH SCHOOL(Gilead Tech)')
    context = {'company': company}
    return render(request, 'company/company-settings.html', context)




