from django import forms

from .models import Photo


class UploadPhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ["id", "slug", "is_active", "post"]

    def save(self, commit = True, parent = None):
        instance = super().save(commit=False)

        if parent: instance.post = parent
        if commit: instance.save()

        return instance