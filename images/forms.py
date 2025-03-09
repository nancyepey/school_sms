from django import forms

from .models import Image
from .services import upload_image_to_cloudflare


class ImageUploadForm(forms.ModelForm):
    image_file = forms.ImageField(required=False)

    class Meta:
        model = Image
        fields = ["title"]

    def save(self, commit=True):
        instance = super().save(commit=False)
        image_file = self.cleaned_data.get("image_file")
        if image_file:
            instance.cloudflare_id = upload_image_to_cloudflare(image_file)

        if commit:
            instance.save()
        return instance

