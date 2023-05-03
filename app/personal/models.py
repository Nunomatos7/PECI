# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Data (models.Model):
    data = models.DateField(primary_key=True)
    
class Temperatura (models.Model):
    temperatura = models.FloatField(default=None)
    data = models.ForeignKey(Data,primary_key=True,on_delete=models.CASCADE)

class CalculosTemperatura(models.Model):
    mes =  models.IntegerField(default=None)
    ano =  models.IntegerField(default=None)
    media =  models.FloatField(default=None)
    minimo =  models.FloatField(default=None)
    maximo =  models.FloatField(default=None)
    soma =  models.FloatField(default=None)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['ano','mes'], name='CalculosTemperatura_pk')
        ]


class Desova (models.Model):
    data = models.ForeignKey(Data,primary_key=True,on_delete=models.CASCADE)
    femeas = models.IntegerField(default=None)
    desovados = models.IntegerField(default=None)
    embrionados = models.IntegerField(default=None)

class Jaula (models.Model):
    id = models.PositiveSmallIntegerField(default=None,primary_key=True)
    massa_volumica = models.FloatField(default=None)
    volume = models.FloatField(default=None)

class Dados (models.Model):
    data = models.ForeignKey(Data,primary_key=True,on_delete=models.CASCADE)
    id_jaula = models.ForeignKey(Jaula,on_delete=models.CASCADE)
    num_peixes = models.PositiveIntegerField(default=None)
    PM = models.FloatField(default=None)
    Biom = models.FloatField(default=None)
    percentagem_alimentacao = models.FloatField(default=None)
    peso = models.FloatField(default=None)
    sacos_racao = models.FloatField(default=None)
    FC = models.FloatField(default=None)
    PM_teorica_alim_real = models.FloatField(default=None)
    alimentacao_real = models.FloatField(default=None)
    PM_teorico = models.FloatField(default=None)
    PM_real = models.FloatField(default=None)
    percentagem_mortalidade_teorica = models.FloatField(default=None)
    num_mortos_teorico = models.FloatField(default=None)
    percentagem_mortalidade_real = models.FloatField(default=None)
    num_mortos_real = models.FloatField(default=None)
    peso_medio = models.FloatField(default=None)
    FC_real = models.FloatField(default=None)

    def get_previous_data(self, date):
        try:
            previous_data = self.objects.filter(data__lt=date).latest('data')
        except self.DoesNotExist:
            previous_data = None
        return previous_data

class Alimentacao(models.Model):
    valor = models.FloatField(default=None)
    peso_inicio = models.FloatField()
    peso_fim = models.FloatField()
    temp = models.FloatField()
    id_jaula = models.ForeignKey(Jaula, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['peso_inicio', 'peso_fim', 'temp', 'id_jaula'], name='alimentacao_pk')
        ]


class Vacina (models.Model):
    id_jaula = models.ForeignKey(Jaula,default=None,on_delete=models.CASCADE)
    data = models.ForeignKey(Data,primary_key=True,on_delete=models.CASCADE)
    num = models.IntegerField(default=None)
    PM = models.FloatField(default=None)

class Movimento(models.Model):
    num = models.IntegerField(default=None)   
    data = models.ForeignKey(Data,on_delete=models.CASCADE)
    jaula_inicio = models.ForeignKey(Jaula, default=None,related_name='movimentos_inicio',on_delete=models.CASCADE)
    jaula_fim = models.ForeignKey(Jaula,default=None,related_name='movimentos_fim',on_delete=models.CASCADE)
    venda = models.BooleanField(default=False)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['data', 'jaula_inicio', 'jaula_fim'], name='my_model_pk')
        ]