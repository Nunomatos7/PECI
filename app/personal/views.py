# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from itertools import chain, product

from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .forms import *
from .models import *
from django.db.models import Max
from datetime import date, datetime, timedelta
from django.db.models import Q,F, functions


# Create your views here.

def home(request):
    return render(request, "home.html", {})

@login_required
def dashboard_view(request):
    return render(request, "dashboard.html", {})

@login_required
def contacts_login_view(request):
    return render(request, "contacts_login.html", {})

def contacts_logout_view(request):
    return render(request, "contacts_logout.html", {})

def month_to_number(month_name):
    month_name = month_name.lower()
    month_names = [
        "janeiro", "fevereiro", "março", "abril", "maio", "junho",
        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
    ]
    month_number = month_names.index(month_name) + 1
    return month_number

def mortalidade_mes (mes):
    if isinstance(mes,str):
        mes = month_to_number(mes)
    if mes == 1 or mes == 2 or mes == 3 or mes == 11 or mes == 12 :
        return 0.2
    if mes == 5 or mes == 4 or mes == 10:
        return 0.5
    if mes == 6:
        return 0.8
    if mes == 7:
        return 1
    if mes == 8:
        return 2
    if mes == 9:
        return 1.5

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
def insert_venda(request):
    first = None
    if request.method == 'POST':
        print("entered")
        vendasJaula_form = VendasJaulaForm(request.POST)
        data_form = DataForm(request.POST)
        param = dict(request.POST)
        ultimo_tuplo_inicio = get_most_recent_data(param['jaula_inicio'][0])
        if int(param['num'][0]) > ultimo_tuplo_inicio.num_peixes:
           param['num'][0] = str(ultimo_tuplo_inicio.num_peixes)
        data = None
        if vendasJaula_form.is_valid():
       
            try:
                #case there is no data
                print('aqui1')
                data = data_form.save()
            except:
                #case already exists data
                print("aqui")
                print(data_form.data['data'])
                data_data = data_form.data['data']
                data = Data.objects.get(data=data_data)

            jaula_fim = None
            try:
                ultimo_tuplo_fim = get_most_recent_data(0)
                jaula_fim = Jaula.objects.get(id=0)
            except:
                jaula_fim = Jaula(0,0,0) # criar jaula 0 caso ela não exista
                jaula_fim.save()
                dados = Dados(
                    data = data,
                    id_jaula = jaula_fim,
                    num_peixes = 0,
                    PM = 0,
                    Biom = 0,
                    percentagem_alimentacao = 0,
                    peso = 0,
                    sacos_racao = 0,
                    FC = 0,
                    PM_teorica_alim_real = 0,
                    alimentacao_real = 0,
                    PM_teorico = 0,
                    PM_real = 0,
                    percentagem_mortalidade_teorica = 0,
                    num_mortos_teorico = 0,
                    percentagem_mortalidade_real = 0,
                    num_mortos_real = 0,
                    peso_medio = 0,
                    FC_real = 0,
                    )
                dados.save()
                ultimo_tuplo_fim = get_most_recent_data(0)
            
            venda = vendasJaula_form.save(commit=False)
            venda.data = data
            venda.jaula_fim = jaula_fim
            venda.venda = True
            #print("teste4:",venda.num)
            #print("teste4:",venda.PM)
            #print("teste4:",venda.data)
            #print("teste4:",venda.jaula_inicio)
            #print("teste4:",venda.jaula_fim)
            #print("teste4:",venda.venda)
            venda.save()
                
            print("ultimo : ")
            print(ultimo_tuplo_fim)
            if ultimo_tuplo_fim != None:
                print("entrou")
                print("Num peixes:",param['num'])
                dadosjaula_form = { 'num_form' : param['num'],
                                    'PM_form'  : param['PM'],
                                    'id_jaula' : [ultimo_tuplo_fim.id_jaula],
                                    'PM' : [ultimo_tuplo_fim.PM],
                                    'alimentacao_real' : [ultimo_tuplo_fim.alimentacao_real],
                                    'FC_real' : [ultimo_tuplo_fim.FC_real],
                                    'PM_teorica_alim_real' : [ultimo_tuplo_fim.PM_teorica_alim_real],
                                    'num_mortos_real' : [ultimo_tuplo_fim.num_mortos_real],
                                    'PM_real' : [ultimo_tuplo_fim.PM_real],
                                    'percentagem_mortalidade_real' : [ultimo_tuplo_fim.percentagem_mortalidade_real]}
                first = calc_dados_v2(data,ultimo_tuplo_fim,dadosjaula_form,data.data.month,True)
                first.save()
                print("first:")
                print(first)
            if ultimo_tuplo_inicio != None :
                print("Num peixes 2:",param['num'])
                dadosjaula_form = { 'num_form' : param['num'],
                                    'PM_form'  : param['PM'],
                                    'id_jaula' : [ultimo_tuplo_inicio.id_jaula],
                                    'PM' : [ultimo_tuplo_inicio.PM],
                                    'alimentacao_real' : [ultimo_tuplo_inicio.alimentacao_real],
                                    'FC_real' : [ultimo_tuplo_inicio.FC_real],
                                    'PM_teorica_alim_real' : [ultimo_tuplo_inicio.PM_teorica_alim_real],
                                    'num_mortos_real' : [ultimo_tuplo_inicio.num_mortos_real],
                                    'PM_real' : [ultimo_tuplo_inicio.PM_real],
                                    'percentagem_mortalidade_real' : [ultimo_tuplo_inicio.percentagem_mortalidade_real]}
                sec = calc_dados_v2(data,ultimo_tuplo_inicio,dadosjaula_form,data.data.month,False)
                if first:
                    sec.id = first.id+1
                sec.save()
            messages.success(request, 'Venda registada com sucesso!')

        else:
            print(vendasJaula_form.errors)
            messages.success(request,('Erro!'))
    else:
        vendasJaula_form = VendasJaulaForm()
        data_form = DataForm()
    return render(request, 'insert_venda.html', {'TransicoesJaulaForm': vendasJaula_form, 'data_form': data_form})


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
            ## calculos com temperatura
            print(data.data)
            mes = data.data.month
            ano = data.data.year
            objects = Temperatura.objects.filter(data__data__month=mes,data__data__year = ano)
            temps = []
            print('aqui')
            print(objects)
            for k in objects:
                temps.append(k.temperatura)
            if temps:
                    calculos = CalculosTemperatura(mes=str(mes),ano = str(ano), media = sum(temps)/len(temps),
                                                minimo = min(temps),maximo = max(temps),soma = sum(temps))
                    CalculosTemperatura.objects.filter(mes=str(mes),ano = str(ano)).delete()
                    calculos.save()
        else:
            messages.success(request, 'Erro!')
    else:
        temp_form = TemperaturaForm()
        data_form = DataForm()
    return render(request, 'insert_temp.html', {'temp_form': temp_form, 'data_form': data_form})

def get_latest_tuple_below_date(given_date,id):
    latest_tuple = Dados.objects.filter(data__lt=given_date,id_jaula = id).aggregate(max_date=Max('data'))
    latest_date = latest_tuple['max_date']

    if latest_date:
        latest_tuple = Dados.objects.filter(data=latest_date,id_jaula = id).first()

    return latest_tuple

def get_most_recent_data(jaula):
    try:
        most_recent_data = Dados.objects.filter(id_jaula=jaula).latest('data')
    except Dados.DoesNotExist:
        return None
    
    return most_recent_data

@login_required
def transicoes(request):
    first = None
    if request.method == 'POST':
        transicoesJaula_form = TransicoesJaulaForm(request.POST)
        data_form = DataForm(request.POST)
        param = dict(request.POST)
        ultimo_tuplo_inicio = get_most_recent_data(param['jaula_inicio'][0])
        if int(param['num'][0]) > ultimo_tuplo_inicio.num_peixes:
           param['num'][0] = str(ultimo_tuplo_inicio.num_peixes)
        data = None
        if transicoesJaula_form.is_valid():
       
            try:
                #case there is no data
                print('aqui1')
                data = data_form.save()
            except:
                #case already exists data
                print("aqui")
                print(data_form.data['data'])
                data_data = data_form.data['data']
                data = Data.objects.get(data=data_data)

            transicao = transicoesJaula_form.save(commit=False)
            transicao.data = data
            transicao.save()
            print(data)
            ultimo_tuplo_fim = get_most_recent_data(param['jaula_fim'][0])
            print("ultimo : ")
            print(ultimo_tuplo_fim)
            if ultimo_tuplo_fim != None:
                print("entrou")
                print("Num peixes:",param['num'])
                dadosjaula_form = { 'num_form' : param['num'],
                                    'PM_form'  : param['PM'],
                                    'id_jaula' : [ultimo_tuplo_fim.id_jaula],
                                    'PM' : [ultimo_tuplo_fim.PM],
                                    'alimentacao_real' : [ultimo_tuplo_fim.alimentacao_real],
                                    'FC_real' : [ultimo_tuplo_fim.FC_real],
                                    'PM_teorica_alim_real' : [ultimo_tuplo_fim.PM_teorica_alim_real],
                                    'num_mortos_real' : [ultimo_tuplo_fim.num_mortos_real],
                                    'PM_real' : [ultimo_tuplo_fim.PM_real],
                                    'percentagem_mortalidade_real' : [ultimo_tuplo_fim.percentagem_mortalidade_real]}
                first = calc_dados_v2(data,ultimo_tuplo_fim,dadosjaula_form,data.data.month,True)
                first.save()
                print("first:")
                print(first)
            if ultimo_tuplo_inicio != None :
                print("Num peixes 2:",param['num'])
                dadosjaula_form = { 'num_form' : param['num'],
                                    'PM_form'  : param['PM'],
                                    'id_jaula' : [ultimo_tuplo_inicio.id_jaula],
                                    'PM' : [ultimo_tuplo_inicio.PM],
                                    'alimentacao_real' : [ultimo_tuplo_inicio.alimentacao_real],
                                    'FC_real' : [ultimo_tuplo_inicio.FC_real],
                                    'PM_teorica_alim_real' : [ultimo_tuplo_inicio.PM_teorica_alim_real],
                                    'num_mortos_real' : [ultimo_tuplo_inicio.num_mortos_real],
                                    'PM_real' : [ultimo_tuplo_inicio.PM_real],
                                    'percentagem_mortalidade_real' : [ultimo_tuplo_inicio.percentagem_mortalidade_real]}
                sec = calc_dados_v2(data,ultimo_tuplo_inicio,dadosjaula_form,data.data.month,False)
                sec.id = first.id+1
                sec.save()
            messages.success(request, 'Movimento Registado com Sucesso!')

        else:
            print(transicoesJaula_form.errors)
            messages.success(request,('Erro!'))
    else:
        transicoesJaula_form = TransicoesJaulaForm()
        data_form = DataForm()
    return render(request, 'transicoes.html', {'TransicoesJaulaForm': transicoesJaula_form, 'data_form': data_form})
    """
     dadosjaula_form2 = {'id_jaula' : [ultimo_tuplo_fim.id_jaula],
                                            'PM' : [ultimo_tuplo_fim.PM],
                                            'alimentacao_real' : [ultimo_tuplo_fim.alimentacao_real],
                                            'FC_real' : [ultimo_tuplo_fim.FC_real],
                                            'PM_teorica_alim_real' : [ultimo_tuplo_fim.PM_teorica_alim_real],
                                            'num_mortos_real' : [ultimo_tuplo_fim.num_mortos_real],
                                            'PM_real' : [ultimo_tuplo_fim.PM_real],
                                            'percentagem_mortalidade_real' : [ultimo_tuplo_fim.percentagem_mortalidade_real]}
    """
def alimentacao(request):
    
    form = AlimentacaoFcForm()
    data_form = DataForm()
    if request.method == 'POST':
        form = AlimentacaoFcForm(request.POST)
        data_form = DataForm(request.POST)
        if form.is_valid():
            param = dict(request.POST)
            print(param['id_jaula'][0])
            try:    #if data NOT exists
                
                if data_form.is_valid():
                    data = data_form.save()

                ultimo_tuplo = get_latest_tuple_below_date(data,param['id_jaula'][0])


            except:     #if data exists
                
                data_data = data_form.data['data']
                data = Data.objects.get(data=data_data)

                ultimo_tuplo = get_latest_tuple_below_date(data_data,param['id_jaula'][0])
                print("ultiplo tuplo",param['id_jaula'][0])
                param = dict(request.POST)
                print(param['percentagem_alimentacao'])
                
                dadosjaula_form = {'id_jaula' : [ultimo_tuplo.id_jaula],
                                            'PM' : [ultimo_tuplo.PM],
                                            'alimentacao_real' : [ultimo_tuplo.alimentacao_real],
                                            'FC_real' : [ultimo_tuplo.FC_real],
                                            'PM_teorica_alim_real' : [ultimo_tuplo.PM_teorica_alim_real],
                                            'num_mortos_real' : [ultimo_tuplo.num_mortos_real],
                                            'PM_real' : [ultimo_tuplo.PM_real],
                                            'percentagem_mortalidade_real' : [ultimo_tuplo.percentagem_mortalidade_real]}
                tuplo = calc_dados(data,ultimo_tuplo,dadosjaula_form,data.data.month,param['percentagem_alimentacao'][0])
                tuplo.save()
        else:
            print(form.errors)
            print(data_form.errors)
            messages.success(request,('Erro!'))
    return render(request, 'alimentacao.html', {'form': form,'data_form' : data_form})


from datetime import date
from itertools import product, takewhile

from datetime import date, timedelta, datetime

def get_month_year_combinations(start_date, end_date):
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.min.time())
    months = []
    while start_datetime <= end_datetime:
        months.append((start_datetime.month, start_datetime.year))
        start_datetime += timedelta(days=31)
    return list(set(months))



@login_required
def delete_temp(request):
    if request.method == 'POST':
        data_inicial_form = DataForm(request.POST,prefix="inicial")
        data_final_form = DataForm(request.POST,prefix="final")


        data_i = datetime.strptime(data_inicial_form.data["inicial-data"], "%Y-%m-%d")
        try:
            data_f = datetime.strptime(data_final_form.data["final-data"], "%Y-%m-%d")
        except:
            # only one date
            data_f=data_i

        delta = data_f - data_i
        num_days = delta.days + 1 

        for day in range(num_days):
            current_date = data_i + timedelta(days=day)
            temperatura = Temperatura.objects.filter(data__data=current_date).first()            
            if temperatura:
                temperatura.delete()
                
            else:
                print("not temperatura")
        #print(data_inicial_form.data)
        #atualizar calculos
        month_year = get_month_year_combinations(data_i,data_f)
        for k in month_year:
            mes,ano = k
            objects = Temperatura.objects.filter(data__data__month=mes,data__data__year = ano)
            if not objects:
                CalculosTemperatura.objects.filter(mes=mes,ano=ano).delete()
                continue
            temps = []
            print('aqui')
            print(objects)
            for k in objects:
                temps.append(k.temperatura)
            if temps:
                    calculos = CalculosTemperatura(mes=str(mes),ano = str(ano), media = sum(temps)/len(temps),
                                                minimo = min(temps),maximo = max(temps),soma = sum(temps))
                    CalculosTemperatura.objects.filter(mes=str(mes),ano = str(ano)).delete()
                    calculos.save()

        messages.success(request,('Dados Temperatura eliminados!'))
        return render(request, 'delete_temp.html', {'data_inicial_form': data_inicial_form, 'data_final_form': data_final_form})
    else:
        data_inicial_form = DataForm(prefix="inicial")
        data_final_form = DataForm(prefix="final")
        return render(request, 'delete_temp.html', {'data_inicial_form': data_inicial_form, 'data_final_form': data_final_form})

@login_required
def delete_dados(request):
    if request.method == 'POST':
        data_inicial_form = DataForm(request.POST,prefix="inicial")
        data_final_form = DataForm(request.POST,prefix="final")

        data_i = datetime.strptime(data_inicial_form.data["inicial-data"], "%Y-%m-%d")
        try:
            data_f = datetime.strptime(data_final_form.data["final-data"], "%Y-%m-%d")
        except:
            # only one date
            data_f=data_i

        delta = data_f - data_i
        num_days = delta.days + 1 

        for day in range(num_days):
            current_date = data_i + timedelta(days=day)
            desova = Dados.objects.filter(data=current_date).first()
            if desova:
                desova.delete()
                
            else:
                print("not desova")

        messages.success(request,('Dados Desovas eliminados!'))
        return render(request, 'delete_desova.html', {'data_inicial_form': data_inicial_form, 'data_final_form': data_final_form})
    else:
        data_inicial_form = DataForm(prefix="inicial")
        data_final_form = DataForm(prefix="final")
        return render(request, 'delete_dados.html', {'data_inicial_form': data_inicial_form, 'data_final_form': data_final_form})


@login_required
def delete_desova(request):
    if request.method == 'POST':
        data_inicial_form = DataForm(request.POST,prefix="inicial")
        data_final_form = DataForm(request.POST,prefix="final")

        data_i = datetime.strptime(data_inicial_form.data["inicial-data"], "%Y-%m-%d")
        try:
            data_f = datetime.strptime(data_final_form.data["final-data"], "%Y-%m-%d")
        except:
            # only one date
            data_f=data_i

        delta = data_f - data_i
        num_days = delta.days + 1 

        for day in range(num_days):
            current_date = data_i + timedelta(days=day)
            desova = Desova.objects.filter(data=current_date).first()
            if desova:
                desova.delete()
                
            else:
                print("not desova")

        messages.success(request,('Dados Desovas eliminados!'))
        return render(request, 'delete_desova.html', {'data_inicial_form': data_inicial_form, 'data_final_form': data_final_form})
    else:
        data_inicial_form = DataForm(prefix="inicial")
        data_final_form = DataForm(prefix="final")
        return render(request, 'delete_desova.html', {'data_inicial_form': data_inicial_form, 'data_final_form': data_final_form})
    
@login_required
def ins_excel_temp(request):
    if request.method == 'POST':
        temp_form = TemperaturaArrayForm(request.POST)
        data_form = DataForm(request.POST,prefix="inicial")
        data_final_form = DataForm(request.POST,prefix="final")
        if temp_form.is_valid():
            data_i = datetime.strptime(data_form.data["inicial-data"], "%Y-%m-%d")
            data_f = datetime.strptime(data_final_form.data["final-data"], "%Y-%m-%d")
            delta = data_f - data_i
            num_days = delta.days + 1 # include end date in count
            temp_array = (temp_form.data['temperatura_array']).split(';')
            if num_days != len(temp_array):
                messages.success(request, 'Nº de dias diferente de temperaturas')

            else:   
                for t,d in zip(temp_array,range(num_days)):
                    current_date = data_i + timedelta(days=d)
                    date = Data(data=current_date)
                    if not Data.objects.filter(data=current_date).exists():
                        date.save()
                    temp = Temperatura(temperatura=t,data=date)
                    temp.save()
                messages.success(request, 'Dados Temperatura adicionado!')
            # else:        
            #     print(data_form)
            #     print(temp_form)
            #     print(data_final_form)
            #     messages.success(request, 'erro not valid')
        #         data_data = data_form.data['data']
        #         data = Data.objects.get(data=data_data)
        #         temp = temp_form.save(commit=False)
        #         temp.data = data
        #         temp.save()
        #         messages.success(request, 'Dados Temperatura adicionado!')
        else:
            print(data_form)
            print(temp_form)
            print(data_final_form)
            messages.success(request, 'not valid')
    
    data_form = DataForm(prefix="inicial")
    data_final_form = DataForm(prefix="final")
    temp_form = TemperaturaArrayForm()
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
def setup_jaula(request):
    if request.method == 'POST':
        setupjaula_form = SetupJaulaForm(request.POST)
        data_form = DataForm(request.POST)
        dadosjaula_form = DadosJaulaForm(request.POST)
        param = dict(request.POST)

        if setupjaula_form.is_valid():

            print("2:",setupjaula_form.data['id'])
            try:
                jaula = Jaula.objects.get(id=setupjaula_form.data['id'])
                jaula.delete()
            except:
                pass
            jaula = Jaula(param['id'][0],param['massa_volumica'][0],param['volume'][0])
            jaula.save()
            num_peixes = dadosjaula_form.data['num_peixes']
            
            try:
                data = Data.objects.get(param['data'][0])
            except:
                data = Data(param['data'][0])
                data.save()
           
            dados = Dados(
                data = data,
                id_jaula = jaula,
                num_peixes = num_peixes,
                PM = 0,
                Biom = 0,
                percentagem_alimentacao = 0,
                peso = 0,
                sacos_racao = 0,
                FC = 0,
                PM_teorica_alim_real = 0,
                alimentacao_real = 0,
                PM_teorico = 0,
                PM_real = 0,
                percentagem_mortalidade_teorica = 0,
                num_mortos_teorico = 0,
                percentagem_mortalidade_real = 0,
                num_mortos_real = 0,
                peso_medio = 0,
                FC_real = 0,
                )

            dados.save()
            setupjaula_form.save()

            messages.success(request, 'Jaula Nova Adicionada!')

        elif(setupjaula_form.data['id']):
            jaula = Jaula.objects.get(id=setupjaula_form.data['id'])
            jaula.massa_volumica = setupjaula_form.data['massa_volumica']
            jaula.volume = setupjaula_form.data['volume']

            try:    #if data NOT exists
            
                if data_form.is_valid():
                    data = data_form.save()


            except:     #if data exists

                data_data = data_form.data['data']
                data = Data.objects.get(data=data_data)

            jaula = Jaula.objects.get(id=setupjaula_form.data['id'])

            num_peixes = dadosjaula_form.data['num_peixes']
           
            dados = Dados(
                data = data,
                id_jaula = jaula,
                num_peixes = num_peixes,
                PM = 0,
                Biom = 0,
                percentagem_alimentacao = 0,
                peso = 0,
                sacos_racao = 0,
                FC = 0,
                PM_teorica_alim_real = 0,
                alimentacao_real = 0,
                PM_teorico = 0,
                PM_real = 0,
                percentagem_mortalidade_teorica = 0,
                num_mortos_teorico = 0,
                percentagem_mortalidade_real = 0,
                num_mortos_real = 0,
                peso_medio = 0,
                FC_real = 0,
                )

            dados.save()
            jaula.save()
            
            messages.success(request, 'Jaula Atualizada!')
        else:
            messages.success(request, 'DADOS INCORRETOS!')
    else:
        setupjaula_form = SetupJaulaForm()
        data_form = DataForm()
        dadosjaula_form = DadosJaulaForm()
    return render(request, 'setup_jaula.html', {'setupjaula_form': setupjaula_form, 'data_form': data_form, 'dadosjaula_form': dadosjaula_form})

@login_required
def vacinados(request):
    if request.method == 'POST':
        vacinados_form = VacinadosForm(request.POST)
        data_form = DataForm(request.POST)

        if vacinados_form.is_valid():
            try:
                #case there is no data
                if data_form.is_valid():
                    data = data_form.save()

                vacinados = vacinados_form.save(commit=False)
                vacinados.data = data
                vacinados.save()
                messages.success(request, 'Dados Vacinados Atualizado!')
            except:
                #case already exists data
                data_data = data_form.data['data']
                data = Data.objects.get(data=data_data)
                vacinados = vacinados_form.save(commit=False)
                vacinados.data = data
                vacinados.save()
                messages.success(request, 'Dados Vacinados Atualizado!')

        else:
            messages.success(request,('Erro!'))
    else:
        vacinados_form = VacinadosForm()
        data_form = DataForm()
    return render(request, 'vacinados.html', {'vacinados_form': vacinados_form, 'data_form': data_form})

@login_required
def dados_jaula(request):
    if request.method == 'POST':
        dadosjaula_form = DadosJaulaForm(request.POST)
        data_form = DataForm(request.POST)

        valor = 0

        """
        queryset = Alimentacao.objects.filter(
        Q(peso_inicio__lte=x) & Q(peso_fim__gte=x) & Q(id_jaula=0)
        ).annotate(
        temp_diff=functions.Abs(F('temp') - y)
        ).order_by('temp_diff').first()
        if queryset:
            valor = queryset.valor

        print(valor)
        """
        
        try:    #if data NOT exists
            
            if data_form.is_valid():
                data = data_form.save()

            data_anterior = Dados.objects.filter(data__lt=data, id_jaula=dadosjaula_form.data['id_jaula']).order_by('-data').first()


        except:     #if data exists
            
            data_data = data_form.data['data']
            data = Data.objects.get(data=data_data)

            data_anterior = Dados.objects.filter(data__lt=data, id_jaula=dadosjaula_form.data['id_jaula']).order_by('-data').first()

        data_month = data.data.month
        print(data_month)
        param = dict(request.POST)
        dados = calc_dados(data, data_anterior, param, data_month,dados = True)
        
        dados.save()
        
        messages.success(request, 'Dados da Jaula Atualizado!')

    else:
            dadosjaula_form = DadosJaulaForm()
            data_form = DataForm()

    return render(request, 'dados_jaula.html', {'dadosjaula_form': dadosjaula_form, 'data_form': data_form})



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

def calc_dados(data, data_anterior, dadosjaula_form, data_month,alimentacao=-1,dados=False):
  
    if (data_anterior != None):
        num_peixes = int(data_anterior.num_peixes) - int(data_anterior.num_mortos_real)
    
    print("teste3:",dadosjaula_form['id_jaula'][0])
    if dados:
        jaula = Jaula.objects.get(id=dadosjaula_form['id_jaula'][0])
    else:
       jaula = Jaula.objects.get(id=dadosjaula_form['id_jaula'][0].id) 
    if (data_anterior != None):
        PM = float(data_anterior.PM_real)
    else:
        PM = dadosjaula_form['PM'][0]
    
    Biom = PM * num_peixes

    temp = 5
        #temp = float(Temperatura.objects.get(data = data))

    valor = 1

    if alimentacao==-1:
        queryset = AlimentacaoFc.objects.filter(
        Q(peso_inicio__lte=(float(PM) * 1000)) & Q(peso_fim__gte=(float(PM) * 1000)) & Q(id=0) & Q(nome='Alimentacao')
        ).annotate(
        temp_diff=functions.Abs(F('temp') - float(temp))
        ).order_by('temp_diff').first()

        if queryset:
            valor = queryset.valor

        print(valor)
        percentagem_alimentacao = float(valor) / 100

        """
        queryset = AlimentacaoFc.objects.filter(
        Q(peso_inicio__lte=(PM * 1000)) & Q(peso_fim__gte=(PM * 1000)) & Q(id=0) & Q(nome='Alimentacao')
        ).annotate(
        temp_diff=functions.Abs(F('temp') - temp)
        ).order_by('temp_diff').first()
        if queryset:
            valor = queryset.valor
        
        
        print(valor)
        percentagem_alimentacao = float(valor)
        """
    else:
        percentagem_alimentacao = float(alimentacao[0])/100
    
    if data_anterior == None:
        peso = float(Biom) * percentagem_alimentacao
    else:
        if data_anterior.peso == 0:
            peso = float(Biom) * percentagem_alimentacao
        else:
            peso = float(data_anterior.Biom) * percentagem_alimentacao

    sacos_racao = float(peso) / 25
    
    if not (dadosjaula_form['alimentacao_real'][0]):
        alimentacao_real = peso * 30
    else:
        alimentacao_real = float(dadosjaula_form['alimentacao_real'][0])
    
    #FC teorico
    queryset = AlimentacaoFc.objects.filter(
    Q(peso_inicio__lte=(PM * 1000)) & Q(peso_fim__gte=(PM * 1000)) & Q(id=0) & Q(nome='FC')
    ).annotate(
    temp_diff=functions.Abs(F('temp') - temp)
    ).order_by('temp_diff').first()
    if queryset:
        valor = queryset.valor
    
    FC = valor
    if not dadosjaula_form['FC_real'][0]:
        FC_real = int(alimentacao_real) / ( (int(data_anterior.num_peixes) * float(data_anterior.PM)) - (int(num_peixes) * float(PM)))
    else:
        FC_real = float(dadosjaula_form['FC_real'][0])

    if not dadosjaula_form['PM_teorica_alim_real'][0]:
        PM_teorica_alim_real = (alimentacao_real / FC + Biom) / num_peixes
    else:
        print("teste:",dadosjaula_form['PM_teorica_alim_real'][0])
        PM_teorica_alim_real = float(dadosjaula_form['PM_teorica_alim_real'][0])
    
    aum_biom_teorico = (peso * 30) / FC
    biom_total = aum_biom_teorico + Biom
    PM_teorico = biom_total / num_peixes
    
    if not (dadosjaula_form['PM_real'][0]):
        PM_real = PM_teorico
    else:
        PM_real = dadosjaula_form['PM_real'][0]
    
    percentagem_mortalidade_teorica = mortalidade_mes(data_month)/100
    
    num_mortos_teorico = num_peixes * percentagem_mortalidade_teorica
    if not (dadosjaula_form['num_mortos_real'][0]):
        num_mortos_real = num_mortos_teorico
    else:
        num_mortos_real = int(dadosjaula_form['num_mortos_real'][0])
    
    if not (dadosjaula_form['percentagem_mortalidade_real'][0]):
        percentagem_mortalidade_real = float(num_mortos_real / num_peixes * 100)
    else:
        percentagem_mortalidade_real = dadosjaula_form['percentagem_mortalidade_real'][0]
    
    peso_medio = PM_real
    
    
    """
    num_peixes = dadosjaula_form.data['num_peixes']
    PM = dadosjaula_form.data['PM']
    Biom = dadosjaula_form.data['Biom']
    percentagem_alimentacao = dadosjaula_form.data['percentagem_alimentacao']
    peso = dadosjaula_form.data['peso']
    sacos_racao = dadosjaula_form.data['sacos_racao']
    FC = dadosjaula_form.data['FC']
    PM_teorica_alim_real = dadosjaula_form.data['PM_teorica_alim_real']
    alimentacao_real = dadosjaula_form.data['alimentacao_real']
    PM_teorico = dadosjaula_form.data['PM_teorico']
    PM_real = dadosjaula_form.data['PM_real']
    percentagem_mortalidade_teorica = dadosjaula_form.data['percentagem_mortalidade_teorica']
    num_mortos_teorico = dadosjaula_form.data['num_mortos_teorico']
    percentagem_mortalidade_real = dadosjaula_form.data['percentagem_mortalidade_real']
    num_mortos_real = dadosjaula_form.data['num_mortos_real']
    peso_medio = dadosjaula_form.data['peso_medio']
    """
    return Dados(
        data = data,
        id_jaula = jaula,
        num_peixes = num_peixes,
        PM = PM,
        Biom = Biom,
        percentagem_alimentacao = percentagem_alimentacao,
        peso = peso,
        sacos_racao = sacos_racao,
        FC = FC,
        PM_teorica_alim_real = PM_teorica_alim_real,
        alimentacao_real = alimentacao_real,
        PM_teorico = PM_teorico,
        PM_real = PM_real,
        percentagem_mortalidade_teorica = percentagem_mortalidade_teorica,
        num_mortos_teorico = num_mortos_teorico,
        percentagem_mortalidade_real = percentagem_mortalidade_real,
        num_mortos_real = num_mortos_real,
        peso_medio = peso_medio,
        FC_real = FC_real,
        )

def calculate_average_weight(initial_fish_count, initial_average_weight, additional_fish_count, additional_average_weight):
    total_weight = (initial_fish_count * initial_average_weight) + (additional_fish_count * additional_average_weight)
    total_fish_count = initial_fish_count + additional_fish_count
    average_weight = total_weight / total_fish_count
    return average_weight

def calc_dados_v2(data, data_anterior, dadosjaula_form, data_month,insertion):
    num_peixes = int(dadosjaula_form['num_form'][0])
    print("Num peixes calc dados v2:",num_peixes)
    if insertion:  
        if (data_anterior != None):
            print("Data anterior num peixes:",data_anterior.num_peixes)
            print("Data anterior num peixes:",data_anterior.num_mortos_real)
            num_peixes = int(data_anterior.num_peixes) + num_peixes
    else:
        if (data_anterior != None):
            num_peixes = int(data_anterior.num_peixes) - num_peixes
    
    print("teste3:",dadosjaula_form['id_jaula'][0])
   
    jaula = Jaula.objects.get(id=dadosjaula_form['id_jaula'][0].id) 
    if (data_anterior != None):
        PM = calculate_average_weight(float(data_anterior.num_peixes),
                                      float(data_anterior.PM),float(dadosjaula_form['num_form'][0]),float(dadosjaula_form['PM_form'][0]))
    else:
        PM = dadosjaula_form['PM'][0]
    
    Biom = PM * num_peixes

    temp = 5
        #temp = float(Temperatura.objects.get(data = data))

    valor = 1

    queryset = AlimentacaoFc.objects.filter(
    Q(peso_inicio__lte=(float(PM) * 1000)) & Q(peso_fim__gte=(float(PM) * 1000)) & Q(id=0) & Q(nome='Alimentacao')
    ).annotate(
    temp_diff=functions.Abs(F('temp') - float(temp))
    ).order_by('temp_diff').first()

    if queryset:
        valor = queryset.valor

    print(valor)
    percentagem_alimentacao = float(valor) / 100

    """
    queryset = AlimentacaoFc.objects.filter(
    Q(peso_inicio__lte=(PM * 1000)) & Q(peso_fim__gte=(PM * 1000)) & Q(id=0) & Q(nome='Alimentacao')
    ).annotate(
    temp_diff=functions.Abs(F('temp') - temp)
    ).order_by('temp_diff').first()
    if queryset:
        valor = queryset.valor
    
    
    print(valor)
    percentagem_alimentacao = float(valor)
        """
    
    if data_anterior == None:
        peso = float(Biom) * percentagem_alimentacao
    else:
        if data_anterior.Biom == 0:
            peso = float(Biom) * percentagem_alimentacao
        else:
            peso = float(data_anterior.Biom) * percentagem_alimentacao
            
            
    sacos_racao = float(peso) / 25
    
    if not (dadosjaula_form['alimentacao_real'][0]):
        alimentacao_real = peso * 30
    else:
        alimentacao_real = float(dadosjaula_form['alimentacao_real'][0])
    
    #FC teorico
    queryset = AlimentacaoFc.objects.filter(
    Q(peso_inicio__lte=(PM * 1000)) & Q(peso_fim__gte=(PM * 1000)) & Q(id=0) & Q(nome='FC')
    ).annotate(
    temp_diff=functions.Abs(F('temp') - temp)
    ).order_by('temp_diff').first()
    if queryset:
        valor = queryset.valor
    
    FC = valor
    if not dadosjaula_form['FC_real'][0]:
        FC_real = int(alimentacao_real) / ( (int(data_anterior.num_peixes) * float(data_anterior.PM)) - (int(num_peixes) * float(PM)))
    else:
        FC_real = float(dadosjaula_form['FC_real'][0])

    if not dadosjaula_form['PM_teorica_alim_real'][0]:
        if num_peixes == 0:
            PM_teorica_alim_real = 0
        else:
            PM_teorica_alim_real = (alimentacao_real / FC + Biom) / num_peixes
    else:
        print("teste:",dadosjaula_form['PM_teorica_alim_real'][0])
        PM_teorica_alim_real = float(dadosjaula_form['PM_teorica_alim_real'][0])
    
    aum_biom_teorico = (peso * 30) / FC
    biom_total = aum_biom_teorico + Biom
    PM_teorico = 0
    if num_peixes == 0:
        PM_teorico = 0
    else:
        PM_teorico = biom_total / num_peixes
    
    if not (dadosjaula_form['PM_real'][0]):
        PM_real = PM_teorico
    else:
        PM_real = dadosjaula_form['PM_real'][0]
    
    percentagem_mortalidade_teorica = mortalidade_mes(data_month)/100
    
    num_mortos_teorico = num_peixes * percentagem_mortalidade_teorica
    if not (dadosjaula_form['num_mortos_real'][0]):
        num_mortos_real = num_mortos_teorico
    else:
        num_mortos_real = int(dadosjaula_form['num_mortos_real'][0])
    
    if not (dadosjaula_form['percentagem_mortalidade_real'][0]):
        if num_peixes == 0:
            percentagem_mortalidade_real = 0
        else:
            percentagem_mortalidade_real = float(num_mortos_real / num_peixes * 100)
    else:
        percentagem_mortalidade_real = dadosjaula_form['percentagem_mortalidade_real'][0]
    
    peso_medio = PM_real
    
    
    """
    num_peixes = dadosjaula_form.data['num_peixes']
    PM = dadosjaula_form.data['PM']
    Biom = dadosjaula_form.data['Biom']
    percentagem_alimentacao = dadosjaula_form.data['percentagem_alimentacao']
    peso = dadosjaula_form.data['peso']
    sacos_racao = dadosjaula_form.data['sacos_racao']
    FC = dadosjaula_form.data['FC']
    PM_teorica_alim_real = dadosjaula_form.data['PM_teorica_alim_real']
    alimentacao_real = dadosjaula_form.data['alimentacao_real']
    PM_teorico = dadosjaula_form.data['PM_teorico']
    PM_real = dadosjaula_form.data['PM_real']
    percentagem_mortalidade_teorica = dadosjaula_form.data['percentagem_mortalidade_teorica']
    num_mortos_teorico = dadosjaula_form.data['num_mortos_teorico']
    percentagem_mortalidade_real = dadosjaula_form.data['percentagem_mortalidade_real']
    num_mortos_real = dadosjaula_form.data['num_mortos_real']
    peso_medio = dadosjaula_form.data['peso_medio']
    """
    
    if num_peixes == 0:
        dados_obj = Dados(
            data = data,
            id_jaula = jaula,
            num_peixes = num_peixes,
            PM = 0,
            Biom = 0,
            percentagem_alimentacao = percentagem_alimentacao,
            peso = 0,
            sacos_racao = 0,
            FC = 0,
            PM_teorica_alim_real = 0,
            alimentacao_real = 0,
            PM_teorico = 0,
            PM_real = 0,
            percentagem_mortalidade_teorica = 0,
            num_mortos_teorico = 0,
            percentagem_mortalidade_real = 0,
            num_mortos_real = 0,
            peso_medio = 0,
            FC_real = 0,
            )
        return dados_obj
        
    dados_obj = Dados(
        data = data,
        id_jaula = jaula,
        num_peixes = num_peixes,
        PM = PM,
        Biom = Biom,
        percentagem_alimentacao = percentagem_alimentacao,
        peso = peso,
        sacos_racao = sacos_racao,
        FC = FC,
        PM_teorica_alim_real = PM_teorica_alim_real,
        alimentacao_real = alimentacao_real,
        PM_teorico = PM_teorico,
        PM_real = PM_real,
        percentagem_mortalidade_teorica = percentagem_mortalidade_teorica,
        num_mortos_teorico = num_mortos_teorico,
        percentagem_mortalidade_real = percentagem_mortalidade_real,
        num_mortos_real = num_mortos_real,
        peso_medio = peso_medio,
        FC_real = FC_real,
        )
    
    print("Dados obj:",dados_obj)
    return dados_obj 