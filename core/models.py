from django.db import models
#
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.conf import settings
import uuid
from django.utils.crypto import get_random_string
from django.utils import timezone

from teacher.models import Teacher
from student.models import Student

import uuid
import pathlib

#for image file handler
def image_file_upload_handler(instance, filepath):
    # instance_id = instance.id
    print("instance_id")
    # print(instance_id)
    print(instance.username)
    # if not instance.id:
    #     instance_id = 1
    instance_username = instance.username
    if not instance.username:
        instance_username = "uname"
    filepath = pathlib.Path(filepath).resolve()
    print("filepath")
    print(filepath)
    # print(instance, filepath)
    fuuid = str(uuid.uuid1())
    return f"userprof/{instance_username}/{fuuid}/{filepath.name}"


#
# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    # email = models.EmailField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, blank=True, null=True, db_index=True)
    student_profile      = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    teacher_profile      = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True)
    phone_code = models.CharField(max_length=30, blank=True)
    is_authorized = models.BooleanField(default=False)
    login_token = models.CharField(max_length=6, blank=True, null=True)
    name = models.CharField(max_length=30, blank=True)
    related_to = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_actif            = models.BooleanField(default=True)
    has_sub            = models.BooleanField(default=True)
    company = models.CharField(max_length=30, blank=True)
    freespace = models.CharField(max_length=30, blank=True)
    # photo       = models.ImageField(upload_to='core/img/', blank=True, default='default.png')
    photo       = models.ImageField(upload_to=image_file_upload_handler, blank=True, default='default.png')
    
       # Fields for user roles
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False) 
    is_top_management = models.BooleanField(default=False)


    created_on = models.DateTimeField(auto_now_add=True)
    updated_o = models.DateTimeField(auto_now=True)

    # Set related_name to None to prevent reverse relationship creation
    groups = models.ManyToManyField(
        'auth.Group',
        related_name=None,
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name=None,
        blank=True
    )

    # USERNAME_FIELD  = "username"
    # REQUIRED_FIELDS = ("username",)

    def __str__(self):
        return self.username


class PasswordResetRequest(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    email = models.EmailField()
    token = models.CharField(max_length=32, default=get_random_string(32), editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Define token validity period (e.g., 1 hour)
    TOKEN_VALIDITY_PERIOD = timezone.timedelta(hours=1)

    def is_valid(self):
        return timezone.now() <= self.created_at + self.TOKEN_VALIDITY_PERIOD

    def send_reset_email(self):
        reset_link = f"http://localhost:8000/authentication/reset-password/{self.token}/"
        send_mail(
            'Password Reset Request',
            f'Click the following link to reset your password: {reset_link}',
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
            fail_silently=False,
        )
