# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
#from .forms import *
from .models import *

# Create your views here.

def home(request):
    return render(request, "base.html", {})

def dashboard_view(request):
    return render(request, "dashboard.html", {})

def insert_view(request):
    if request.method == "POST":
        form = DesovaForm(request.POST or None)
        #verificar se form é valido
        form.save()
        return render(request, "insert.html", {})
    else:
        return render(request, "insert.html", {})

def contacts_view(request):
    return render(request, "contacts.html", {})



