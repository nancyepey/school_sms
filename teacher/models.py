from django.db import models
#
from school.models import ClassRoom
from subject.models import Subject
from django.utils.text import slugify
# Create your models here.



class Teacher(models.Model):
    name                = models.TextField( null=True, blank=True)
    teacher_uid         = models.CharField(max_length=100, unique=True,null=True, blank=True)
    gender              = models.CharField(max_length=100, choices=[('Male','Male'), ('Female', 'Female')])
    date_of_birth       = models.DateField()
    # Define a foreign key relationship with Teacher
    # Multiple Teacher can be assigned to one Subject
    # teacher_subj        = models.ForeignKey(Subject, on_delete=models.CASCADE)
    classrooms           = models.ManyToManyField(ClassRoom)
    t_subjects           = models.ManyToManyField(Subject)
    joining_date        = models.DateField()
    mobile_number       = models.CharField(max_length=15, null=True, blank=True)
    email               = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    section             = models.CharField(max_length=100)
    teacher_image       = models.ImageField(upload_to='teacher/img/', blank=True)
    permanent_address   = models.TextField( null=True)
    slug                = models.SlugField(max_length=255, unique=True, blank=True)
    added_by            = models.CharField(max_length=100, null=True)
    modified_by         = models.CharField(max_length=100, null=True, blank=True)
    is_actif            = models.BooleanField(default=True)
    created_on          = models.DateTimeField(auto_now_add=True)
    updated_on          = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-")
        super(Teacher, self).save(*args, **kwargs)
    

    def __str__(self):
        return f"{self.name} "




