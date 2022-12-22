# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import *
# Create your views here.
temperaturas = Temperatura.objects.all
print(temperaturas)
def home_screen_view(request):
    return render(request, "base.html", {'temperaturas' : temperaturas})

def dashboard_view(request):
    return render(request, "dashboard.html", {})

def insert_view(request):
    return render(request, "insert.html", {})

def contacts_view(request):
    return render(request, "contacts.html", {})



