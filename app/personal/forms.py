from django import forms
from .models import *

class DataForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = ['data']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data'].error_messages = {'unique': 'Data já existente, dado atualizado.'}


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


class TemperaturaArrayForm(forms.Form):
    temperatura_array = forms.CharField(label='Temperaturas')

class DesovasLineForm(forms.Form):
    desovasLines = forms.CharField(label='Desovas')

class SetupJaulaForm(forms.ModelForm):
    class Meta:
        model = Jaula
        fields = ['id','massa_volumica','volume']

class VacinadosForm(forms.ModelForm):
    class Meta:
        model = Vacina
        fields = ['id_jaula','num','PM']
    

class AlimentacaoForm(forms.ModelForm):
    class Meta:
        model = Alimentacao
        fields = ['valor','peso_inicio','peso_fim','temp','id_jaula']

class DadosJaulaForm(forms.ModelForm):
    class Meta:
        model = Dados
        fields = ['data','id_jaula','num_peixes','PM','Biom','percentagem_alimentacao','peso',
                  'sacos_racao','FC','PM_teorica_alim_real','alimentacao_real','PM_teorico',
                  'PM_real','percentagem_mortalidade_teorica','num_mortos_teorico',
                  'percentagem_mortalidade_real','num_mortos_real','peso_medio','FC_real']
        
class TransicoesJaulaForm(forms.ModelForm):
    class Meta:
        model = Movimento
        fields = ['num','jaula_inicio','jaula_fim']