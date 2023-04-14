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
from datetime import datetime, timedelta

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
            messages.success(request,('Dados Temperatura eliminado!'))
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
            messages.success(request,('Dados Desova eliminado!'))
            return render(request, 'delete_temp.html', {'form': form})
        else:
            messages.success(request,('Erro!'))
            return render(request, 'delete_temp.html', {'form': form})
    else:
        return render(request, 'delete_desova.html', {'form': form})
    
@login_required
def ins_excel_temp(request):
    if request.method == 'POST':
        temp_form = TemperaturaArrayForm(request.POST)
        data_form = DataForm(request.POST, prefix="inicial")
        data_final_form = DataForm(request.POST, prefix="final")
        if temp_form.is_valid():
            try:
                if data_form.is_valid():
                    print("valid")
                data_i = datetime.strptime(data_form.data["inicial-data"], "%Y-%m-%d")
                data_f = datetime.strptime(data_form.data["final-data"], "%Y-%m-%d")
                delta = data_f - data_i
                num_days = delta.days + 1 # include end date in count
                temp_array = (temp_form.data['temperatura_array']).split(';')
                if num_days != len(temp_array):
                    messages.success(request, 'Erro!')
                else:   
                    for t,d in zip(temp_array,range(num_days)):
                        current_date = data_i + timedelta(days=d)
                        date = Data(data=current_date)
                        if not Data.objects.filter(data=current_date).exists():
                            date.save()
                        temp = Temperatura(temperatura=t,data=date)
                        temp.save()
                    messages.success(request, 'Dados Temperatura adicionado!')
            except Exception as e:
                print(e)
                print("not Valid")
        #         data_data = data_form.data['data']
        #         data = Data.objects.get(data=data_data)
        #         temp = temp_form.save(commit=False)
        #         temp.data = data
        #         temp.save()
        #         messages.success(request, 'Dados Temperatura adicionado!')
        # else:
        #     messages.success(request, 'Erro!')
    else:
        temp_form = TemperaturaArrayForm()
        data_form = DataForm(request.POST, prefix="inicial")
        data_final_form = DataForm(request.POST, prefix="final")
    return render(request, 'ins_excel_temp.html', {'temp_form': temp_form, 'data_form': data_form, 'data_final_form': data_final_form})
    
@login_required
def ins_excel_desovas(request):
    if request.method == 'POST':
        desova_form = DesovasLineForm(request.POST)

        if desova_form.is_valid():
            print(desova_form)
            print(desova_form.data['desovasLines'])
            desova_data = (desova_form.data['desovasLines']).split(';')
            print(desova_data)
            desova_fieds = []
            for i in range(0, len(desova_data), 4):
                desova_fieds.append(desova_data[i:i+4])

            print(desova_fieds)
            for d in desova_fieds:
                desova = Desova()
                data = datetime.strptime(d[0],"%d/%m/%Y")
                data_mod = Data(data=data)
                if not Data.objects.filter(data=data).exists():  
                    data_mod.save()
                desova.data = data_mod
                desova.femeas = d[1].replace(",", "")
                desova.desovados = d[2].replace(",", "")
                desova.embrionados = d[3].replace(",", "")
                desova.save()
                messages.success(request, 'Dados Desova adicionado!')
            # try:
            #     #case there is no data
            #     if data_form.is_valid():
            #         data = data_form.save()

            #     desova = desova_form.save(commit=False)
            #     desova.data = data
            #     desova.save()
            #     messages.success(request, 'Dados Desova adicionado!')
            # except:
            #     #case already exists data
            #     # data_data = data_form.data['data']
            #     # data = Data.objects.get(data=data_data)
            #     # desova = desova_form.save(commit=False)
            #     # desova.data = data
            #     # desova.save()
            #     # messages.success(request, 'Dados Desova adicionado!')

        else:
            messages.success(request,('Erro!'))
    else:
        desova_form = DesovasLineForm()
    return render(request, 'ins_excel_desovas.html', {'desova_form': desova_form})

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

@login_required
def transicoes(request):
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
    return render(request, 'transicoes.html', {'temp_form': temp_form, 'data_form': data_form})


@login_required
def amostragens(request):
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
    return render(request, 'amostragens.html', {'temp_form': temp_form, 'data_form': data_form})

@login_required
def venda(request):
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
    return render(request, 'venda.html', {'temp_form': temp_form, 'data_form': data_form})

@login_required
def comida(request):
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
    return render(request, 'comida.html', {'temp_form': temp_form, 'data_form': data_form})

@login_required
def setup_jaula(request):
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
    return render(request, 'setup_jaula.html', {'temp_form': temp_form, 'data_form': data_form})
