import json
import uuid

from django import forms
from django.template import loader


class DropzoneInput(forms.TextInput):
    template_name = 'dropzone/dropzone.html'

    class Media:
        js = ("js/dropzone/dropzone.js", "js/dropzone/django-dropzone.js",)
        css = {"all": ("css/dropzone/basic.css", "css/dropzone/dropzone.css", "css/dropzone/django-dropzone.css",)}

    def __init__(self, *args, **kwargs):
        self.dropzone_config = kwargs.pop("dropzone_config", {})
        self.uid = uuid.uuid4()
        super(DropzoneInput, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''

        c = {
            "dropzone_config_json": json.dumps(self.dropzone_config),
            "name": name,
            "value": value,
            "uid": self.uid
        }

        t = loader.get_template(self.template_name)

        return t.render(c)
