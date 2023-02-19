from django import forms
from models import *

class DesovaForm(forms.ModelForm):
    class Meta :
        model = Desova
        fields = ['femeas', 'data', 'embrionados', 'desovados' ]

class TemperaturaForm(forms.ModelForm):
    class Meta :
        model = Temperatura
        fields = ['data', 'temperatura']
#depois fazer restantes