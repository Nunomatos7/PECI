from django import forms
from .models import *
"""
class DataForm(forms.ModelForm):
    data = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Data
        fields = ['data']
        
    def clean_data(self):
        data = self.cleaned_data['data']
        
        try:
            data_obj = Data.objects.get(data=data)
        except Data.DoesNotExist:
            return data
        
        return data_obj
"""
class DataForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = ['data']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'})
        }


class DesovaForm(forms.ModelForm):
    class Meta :
        model = Desova
        exclude = ['data']
        #fields = ['data', 'femeas', 'desovados', 'embrionados' ]
        

class TemperaturaForm(forms.ModelForm):
    class Meta:
        model = Temperatura
        exclude = ['data']
        widgets = {'temperatura': forms.NumberInput(attrs={'step': 0.1})}
