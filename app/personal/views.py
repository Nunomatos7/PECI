# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
#from .forms import *
from .models import *

# Create your views here.

def home(request):
    return render(request, "base.html", {})

@login_required
def dashboard_view(request):
    return render(request, "dashboard.html", {})

@login_required
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



