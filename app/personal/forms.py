from django import forms
from models import *

class TemperaturaForma(forms.ModelForm):
    class Meta :
        model = Temperatura
        fields = ['temperatura', 'data' ]

#depois fazer restantes