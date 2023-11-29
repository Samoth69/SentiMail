import django.forms as forms
from base.models import UploadFile

class EmailForm(forms.ModelForm):
    class Meta:
        model = UploadFile
        fields = ( 'file', )