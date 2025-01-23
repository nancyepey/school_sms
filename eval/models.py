from django.db import models
#
# from teacher.models import Teacher
from student.models import Student
from subject.models import Subject


# Create your models here.
class Eval(models.Model):
    title              = models.CharField(max_length=100, unique=True)
    titre              = models.CharField(max_length=100, null=True, blank=True)
    value                = models.DecimalField(max_digits=10, decimal_places=2) #
    coef                = models.DecimalField(max_digits=10, decimal_places=0) #
    subject_code        = models.CharField(max_length=100, unique=True,null=True, blank=True)
    # Define a foreign key relationship with eval
    # Multiple eval can be assigned to one subject
    subject             = models.ForeignKey(Subject, on_delete=models.CASCADE)
    observation         = models.TextField( null=True, blank=True)

    # Define a foreign key relationship with eval
    # Multiple eval can be assigned to one student
    student              = models.ForeignKey(Student, on_delete=models.CASCADE)

    teacher             = models.CharField(max_length=100)
    added_by            = models.CharField(max_length=100, null=True)
    modified_by         = models.CharField(max_length=100, null=True, blank=True)
    is_actif            = models.BooleanField(default=True)
    created_on          = models.DateTimeField(auto_now_add=True)
    updated_on          = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"{self.title} "

