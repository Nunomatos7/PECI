# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Temperatura (models.Model):
    data = models.DateField
    temperatura = models.FloatField

class Desova (models.Model):
    data = models.DateField
    femeas = models.IntegerField
    desovados = models.IntegerField
    embrionados = models.IntegerField

class Jaula (models.Model):
    id = models.PositiveSmallIntegerField
    num_peixes = models.PositiveIntegerField
    data = models.DateField
    PM = models.FloatField
    Blom = models.FloatField
    percentagem_alimentacao = models.FloatField
    peso = models.FloatField
    sacos_racao = models.FloatField
    FC = models.FloatField
    peso_medio = models.FloatField
    alimentacao_teorica = models.FloatField
    alimentacao_real = models.FloatField
    PM_teorico = models.FloatField
    PM_real = models.FloatField
    percentagem_mortalidade_teorica = models.FloatField
    num_mortos_teorico = models.FloatField
    percentagem_mortalidade_real = models.FloatField
    num_mortos_real = models.FloatField
    retirados = models.PositiveSmallIntegerField
    colocados = models.PositiveSmallIntegerField
    FC_real = models.FloatField

