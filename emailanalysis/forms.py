from django.forms import forms
from dropzone.forms import DropzoneInput


class ExampleForm(forms.Form):
    emails = forms.FileField(
        widget=DropzoneInput(dropzone_config={
            # "autoProcessQueue": False,
            # todo: add a reasonable max file size
            "maxFilesize": 100,
            "maxFiles": 1,
            "url": '/email/import/parse/',
            # "uploadMultiple": True,
            "addRemoveLinks": True
        })
    )
