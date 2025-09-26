from django import forms
from .models import UploadedFile

class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file', 'title']

    def clean_file(self):
        f = self.cleaned_data.get('file')
        # optional: validate size/type here
        return f
