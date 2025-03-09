from django.db import models

# Create your models here.

class Image(models.Model):
    title = models.CharField(max_length=200)
    cloudflare_id = models.CharField(max_length=200)
    added_by            = models.CharField(max_length=100, null=True)
    modified_by         = models.CharField(max_length=100, null=True, blank=True)
    is_actif            = models.BooleanField(default=True)
    created_on          = models.DateTimeField(auto_now_add=True)
    updated_on          = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
