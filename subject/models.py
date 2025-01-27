from django.db import models
#
from django.utils.text import slugify

from school.models import ClassRoom, Specialty



# Create your models here.

class Subject(models.Model):
    title               = models.TextField( null=True, blank=True)
    fr_title            = models.TextField( null=True, blank=True)
    # coef                = models.DecimalField(max_digits=10, decimal_places=0) #
    coef                = models.CharField(max_length=100, null=True, blank=True)
    subject_code        = models.CharField(max_length=100, unique=True,null=True, blank=True)
    # To define a many-to-many relationship, use ManyToManyField.
    # In this example, an Article can be published in multiple Publication objects, and a Publication has multiple Article objects
    classroom           = models.ManyToManyField(ClassRoom)
    specialty           = models.ManyToManyField(Specialty)
    # specialty          = models.ForeignKey(Specialty, on_delete=models.CASCADE, default=None, null=True, blank=True)
    description         = models.TextField( null=True, blank=True)
    category            = models.CharField(max_length=100, null=True, blank=True)
    slug                = models.SlugField(max_length=255, unique=True, blank=True)
    added_by            = models.CharField(max_length=100, null=True)
    modified_by         = models.CharField(max_length=100, null=True, blank=True)
    is_actif            = models.BooleanField(default=True)
    created_on          = models.DateTimeField(auto_now_add=True)
    updated_on          = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.subject_code}")
        super(Subject, self).save(*args, **kwargs)
    

    def __str__(self):
        return f"{self.title} "

