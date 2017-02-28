from django.forms import forms
from dropzone.forms import DropzoneInput


class ExampleForm(forms.Form):
    images = forms.FileField(
        widget=DropzoneInput(dropzone_config={
            "maxFilesize": 10,
            # "acceptedFiles": "image/*",
            "url": '/file_uploads/upload/',
            "addRemoveLinks": True
        })
    )