# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#import pymysql
from models import Desovas
from django.shortcuts import render

# Create your views here.

def home_screen_view(request):
    return render(request, "base.html", {})

def send(request):
    p = Desovas(request[0],request[1],request[2],request[3])
    p.save()