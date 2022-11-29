# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Desovas(models.Model):
    data = models.DateField()
    femeas = models.IntegerField()
    desovados = models.IntegerField()
    embrionados = models.IntegerField()
class Temperatures (models.Model):
    data = models.DateField()
    valor = models.FloatField()
    

