from django.db import models
##
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from uuid import uuid4

class ClassRoom(models.Model):
    class_name              = models.CharField(max_length=250, unique=True,)
    class_code              = models.CharField(max_length=250, unique=True,)
    class_department        = models.CharField(max_length=250, null=True, blank=True)
    other                   = models.CharField(max_length=250, null=True, blank=True)
    added_by                = models.CharField(max_length=100, null=True)
    modified_by             = models.CharField(max_length=100, null=True, blank=True)
    slug                    = models.SlugField(max_length=255, unique=True, blank=True)
    is_actif                = models.BooleanField(default=True)
    created_on              = models.DateTimeField(auto_now_add=True)
    updated_on              = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.class_name}-{self.class_code}")
        super(ClassRoom, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.class_name} ({self.class_code})"


class Specialty(models.Model):
    name              = models.CharField(max_length=250, unique=True,)
    code              = models.CharField(max_length=250, unique=True,)
    # classroom      = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, null=True, blank=True)
    department        = models.CharField(max_length=250, null=True, blank=True)
    other                   = models.CharField(max_length=250, null=True, blank=True)
    added_by                = models.CharField(max_length=100, null=True)
    modified_by             = models.CharField(max_length=100, null=True, blank=True)
    slug                    = models.SlugField(max_length=255, unique=True, blank=True)
    is_actif                = models.BooleanField(default=True)
    created_on              = models.DateTimeField(auto_now_add=True)
    updated_on              = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.code}")
        super(Specialty, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Settings(models.Model):

    # PROVINCES = [
    # ('Gauteng', 'Gauteng'),
    # ('Free State', 'Free State'),
    # ('Limpopo', 'Limpopo'),
    # ]

    #Basic Fields
    clientName = models.CharField(null=True, blank=True, max_length=200)
    clientLogo = models.ImageField(default='default_logo.jpg', upload_to='school/img/')
    addressLine1 = models.CharField(null=True, blank=True, max_length=200)
    exact_address = models.CharField(max_length=200, null=True, blank=True)
    # province = models.CharField(choices=PROVINCES, blank=True, max_length=100)
    postalCode = models.CharField(null=True, blank=True, max_length=10)
    phoneNumber = models.CharField(null=True, blank=True, max_length=100)
    emailAddress = models.CharField(null=True, blank=True, max_length=100)
    taxNumber = models.CharField(null=True, blank=True, max_length=100)
    other                   = models.CharField(max_length=250, null=True, blank=True)
    added_by                = models.CharField(max_length=100, null=True)
    modified_by             = models.CharField(max_length=100, null=True, blank=True)
    is_actif                = models.BooleanField(default=True)


    #Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return f'{self.clientName}_{self.uniqueId}'


    def get_absolute_url(self):
        return reverse('settings-detail', kwargs={'slug': self.slug})


    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify(f'{self.clientName}_{self.uniqueId}')

        self.slug = slugify(f'{self.clientName}_{self.uniqueId}')
        self.last_updated = timezone.localtime(timezone.now())

        super(Settings, self).save(*args, **kwargs)