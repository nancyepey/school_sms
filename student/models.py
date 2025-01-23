from django.db import models

#
from django.utils.text import slugify

from school.models import ClassRoom

# Create your models here.

class Parent(models.Model):
    father_name             = models.CharField(max_length=250, null=True, blank=True)
    father_occupation       = models.CharField(max_length=250, null=True, blank=True)
    father_mobile           = models.CharField(max_length=100, unique=True, null=True, blank=True)
    father_email            = models.EmailField(max_length=100,unique=True,  null=True, blank=True)
    mother_name             = models.CharField(max_length=250, null=True, blank=True)
    mother_occupation       = models.CharField(max_length=250, null=True, blank=True)
    mother_mobile           = models.CharField(max_length=100, unique=True, null=True, blank=True)
    mother_email            = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    carer_name              = models.CharField(max_length=250, null=True, blank=True)
    carer_occupation        = models.CharField(max_length=250, null=True, blank=True)
    carer_mobile            = models.CharField(max_length=100, unique=True, null=True, blank=True)
    carer_email             = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    present_address         = models.TextField( null=True, blank=True)
    permanent_address       = models.TextField( null=True)
    added_by                = models.CharField(max_length=100, null=True)
    modified_by             = models.CharField(max_length=100, null=True, blank=True)
    is_actif                = models.BooleanField(default=True)
    created_on              = models.DateTimeField(auto_now_add=True)
    updated_on              = models.DateTimeField(auto_now=True)

    def __str__(self) ->str:
        if self.father_name == "":
            return f"{self.carer_name}"
        if self.mother_name == "":
            return f"{self.carer_name}"
        return f"{self.father_name} & {self.mother_name}"


class Student(models.Model):
    name                = models.TextField( null=True, blank=True)
    student_uid         = models.CharField(max_length=100, unique=True,null=True, blank=True)
    gender              = models.CharField(max_length=100, choices=[('Male','Male'), ('Female', 'Female')])
    date_of_birth       = models.DateField()
    # Define a foreign key relationship with Student
    # Multiple Student can be assigned to one Classroom
    student_class       = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    # student_class       = models.CharField(max_length=100)
    religion            = models.CharField(max_length=100, null=True, blank=True)
    joining_date        = models.DateField()
    mobile_number       = models.CharField(max_length=15, null=True, blank=True)
    admission_number    = models.CharField(max_length=15)
    section             = models.CharField(max_length=100)
    student_image       = models.ImageField(upload_to='student/img/', blank=True)
    # parent              = models.OneToOneField(Parent, on_delete=models.CASCADE)
    # Define a foreign key relationship with Student
    # Multiple Student can be assigned to one Parent
    parent              = models.ForeignKey(Parent, on_delete=models.CASCADE)
    slug                = models.SlugField(max_length=255, unique=True, blank=True)
    added_by            = models.CharField(max_length=100, null=True)
    modified_by         = models.CharField(max_length=100, null=True, blank=True)
    is_actif            = models.BooleanField(default=True)
    created_on          = models.DateTimeField(auto_now_add=True)
    updated_on          = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-")
        super(Student, self).save(*args, **kwargs)
    

    def __str__(self):
        return f"{self.name} "


