# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Temperatura (models.Model):
    data = models.DateField(primary_key=True)
    temperatura = models.FloatField(default=None)

class Desova (models.Model):
    data = models.DateField(primary_key=True,default=None)
    femeas = models.IntegerField(default=None)
    desovados = models.IntegerField(default=None)
    embrionados = models.IntegerField(default=None)

class Jaula (models.Model):
    id = models.PositiveSmallIntegerField(default=None)
    num_peixes = models.PositiveIntegerField(default=None)
    data = models.DateField(primary_key=True)
    PM = models.FloatField(default=None)
    Biom = models.FloatField(default=None)
    percentagem_alimentacao = models.FloatField(default=None)
    peso = models.FloatField(default=None)
    sacos_racao = models.FloatField(default=None)
    FC = models.FloatField(default=None)
    peso_medio = models.FloatField(default=None)
    PM_teorica_alim_real = models.FloatField(default=None)
    alimentacao_real = models.FloatField(default=None)
    PM_teorico = models.FloatField(default=None)
    PM_real = models.FloatField(default=None)
    percentagem_mortalidade_teorica = models.FloatField(default=None)
    num_mortos_teorico = models.FloatField(default=None)
    percentagem_mortalidade_real = models.FloatField(default=None)
    num_mortos_real = models.FloatField(default=None)
    retirados = models.PositiveSmallIntegerField(default=None)
    colocados = models.PositiveSmallIntegerField(default=None)
    FC_real = models.FloatField(default=None)
    volume = models.FloatField(default=None)

