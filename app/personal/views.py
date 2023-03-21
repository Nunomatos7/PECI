# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .forms import *
from .models import *

# Create your views here.

def home(request):
    return render(request, "home.html", {})

@login_required
def dashboard_view(request):
    return render(request, "dashboard.html", {})

def contacts_view(request):
    return render(request, "contacts.html", {})

@login_required
def insert_desovas(request):
    if request.method == 'POST':
        desova_form = DesovaForm(request.POST)
        data_form = DataForm(request.POST)

        if desova_form.is_valid():
            try:
                #case there is no data
                if data_form.is_valid():
                    data = data_form.save()

                desova = desova_form.save(commit=False)
                desova.data = data
                desova.save()
                messages.success(request, 'Dados Desova adicionado!')
            except:
                #case already exists data
                data_data = data_form.data['data']
                data = Data.objects.get(data=data_data)
                desova = desova_form.save(commit=False)
                desova.data = data
                desova.save()
                messages.success(request, 'Dados Desova adicionado!')

        else:
            messages.success(request,('Erro!'))
    else:
        desova_form = DesovaForm()
        data_form = DataForm()
    return render(request, 'insert_desovas.html', {'desova_form': desova_form, 'data_form': data_form})

@login_required
def insert_temp(request):
    if request.method == 'POST':
        temp_form = TemperaturaForm(request.POST)
        data_form = DataForm(request.POST)

        if temp_form.is_valid():
            try:
                if data_form.is_valid():
                    data = data_form.save()
                
                temp = temp_form.save(commit=False)
                temp.data = data
                temp.save()
                messages.success(request, 'Dados Temperatura adicionado!')
            except:
                data_data = data_form.data['data']
                data = Data.objects.get(data=data_data)
                temp = temp_form.save(commit=False)
                temp.data = data
                temp.save()
                messages.success(request, 'Dados Temperatura adicionado!')
        else:
            messages.success(request, 'Erro!')
    else:
        temp_form = TemperaturaForm()
        data_form = DataForm()
    return render(request, 'insert_temp.html', {'temp_form': temp_form, 'data_form': data_form})


@login_required
def delete_temp(request):
    form = DataForm()
    if request.method == 'POST':
        data = request.POST.get('data')
        temperatura = Temperatura.objects.filter(data__data=data).first()
        if temperatura:
            temperatura.delete()
            messages.success(request,('Dados Temperatura eleminado!'))
            return render(request, 'delete_temp.html', {'form': form})
        else:
            messages.success(request,('Erro!'))
            return render(request, 'delete_temp.html', {'form': form})
    else:
        return render(request, 'delete_temp.html', {'form': form})
    
@login_required
def delete_desova(request):
    form = DataForm()
    if request.method == 'POST':
        data = request.POST.get('data')
        desova = Desova.objects.filter(data__data=data).first()
        if desova:
            desova.delete()
            messages.success(request,('Dados Desova eleminado!'))
            return render(request, 'delete_temp.html', {'form': form})
        else:
            messages.success(request,('Erro!'))
            return render(request, 'delete_temp.html', {'form': form})
    else:
        return render(request, 'delete_desova.html', {'form': form})
    
@login_required
def ins_excel_temp(request):
    return render(request, 'ins_excel_temp.html')
    
@login_required
def ins_excel_desovas(request):
    return render(request, 'ins_excel_desovas.html',)

@login_required
def teste(request):
    if request.method == 'POST':
        form = DesovaForm(request.POST or None)
        #verificar se form é valido
        if form.is_valid():
            form.save()
            messages.success(request,('Dados Desova adicionado!'))
            return redirect('teste')
        else:
            messages.success(request,('DADOS INCORRETOS!'))

    form = DesovaForm()
    Desovas = Desova.objects.all()
    """
    form = DesovaForm()
    Desovas = Desova.objects.all()
    
    IN HTML TO PRINT INFO: {{ Desovas }}
    PRINT ALL FROM DESOVAS:
        {% for x in Desovas %}
            {{ x }}
        {% endfor %}

    para apresentar especifico: x.data, x.femeas,...
    
    return render(request,'insert_desovas.html',{})
    """
    
    return render(request,'teste.html',{'form':form, 'Desovas':Desovas})
