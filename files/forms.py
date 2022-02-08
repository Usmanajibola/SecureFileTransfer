from django import forms
from files.models import File, Link 


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'file']

class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['name', 'link']
        labels = {'name':'Name', 'link':'Link'}

class PasswordForm(forms.Form):
    password = forms.CharField(max_length=100)