
from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'id':'form-file'}))
    # file = forms.FileField()