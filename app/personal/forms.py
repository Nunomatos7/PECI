from django import forms
from models import *

class DesovaForm(forms.ModelForm):
    class Meta :
        model = Desova
        fields = ['femeas', 'data', 'embrionados', 'desovados' ]

#depois fazer restantes