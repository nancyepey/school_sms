from django.db import models
#
from django.utils.text import slugify

from school.models import ClassRoom, Specialty

# Create your models here.


class Department(models.Model):
    name                = models.TextField( null=True, blank=True)
    department_code      = models.CharField(max_length=100, unique=True,null=True, blank=True)
    # To define a many-to-many relationship, use ManyToManyField.
    # In this example, an Article can be published in multiple Publication objects, and a Publication has multiple Article objects
    # depart_class        = models.ManyToManyField(ClassRoom)
    specialties        = models.ManyToManyField(Specialty, blank=True, related_name='depart_specialty')
    slug                = models.SlugField(max_length=255, unique=True, blank=True)
    added_by            = models.CharField(max_length=100, null=True)
    modified_by         = models.CharField(max_length=100, null=True, blank=True)
    is_actif            = models.BooleanField(default=True)
    created_on          = models.DateTimeField(auto_now_add=True)
    updated_on          = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.department_code}_{self.specialties}")
        super(Department, self).save(*args, **kwargs)
    

    def __str__(self):
        return f"{self.name} "


