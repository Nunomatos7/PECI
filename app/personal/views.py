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

def alimentacao(request):
    form = AlimentacaoForm()
    if request.method == 'POST':
        param = dict(request.POST)
        print(param)
        print(param['id_jaula'])
        jaula = Jaula.objects.get(id=int(param['id_jaula'][0]))
        print(jaula)
        alimentacao =  Alimentacao.objects.filter(peso_inicio = int(param['peso_inicio'][0]),peso_fim=int(param['peso_fim'][0]), temp = int(param['temp'][0]), id_jaula = jaula).first()
        print("alimentacao")
        print(alimentacao)
        if alimentacao:
            print(param['valor'])
            alimentacao.valor = int(param['valor'][0])
            alimentacao.save()
            messages.success(request,('Alimentacao atualizada'))
            return render(request, 'alimentacao.html', {'form': form})
        else:
            messages.success(request,('Erro!'))
    return render(request, 'alimentacao.html', {'form': form})


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

        messages.success(request,('Dados Temperatura eliminados!'))
        return render(request, 'delete_temp.html', {'data_inicial_form': data_inicial_form, 'data_final_form': data_final_form})
    else:
        data_inicial_form = DataForm(prefix="inicial")
        data_final_form = DataForm(prefix="final")
        return render(request, 'delete_temp.html', {'data_inicial_form': data_inicial_form, 'data_final_form': data_final_form})
    
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
         
        if setupjaula_form.is_valid():
            setupjaula_form.save()
            messages.success(request, 'Jaula Nova Adicionada!')
        elif(setupjaula_form.data['id']):
            jaula = Jaula.objects.get(id=setupjaula_form.data['id'])
            jaula.massa_volumica = setupjaula_form.data['massa_volumica']
            jaula.volume = setupjaula_form.data['volume']
            jaula.save()
            messages.success(request, 'Jaula Atualizada!')
        else:
            messages.success(request, 'DADOS INCORRETOS!')
    else:
        setupjaula_form = SetupJaulaForm()
    return render(request, 'setup_jaula.html', {'setupjaula_form': setupjaula_form})

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

        try:    #if data NOT exists
            
            if data_form.is_valid():
                data = data_form.save()

            data_anterior = Dados.objects.filter(data__lt=data, id_jaula=dadosjaula_form.data['id_jaula']).order_by('-data').first()


        except:     #if data exists
            
            data_data = data_form.data['data']
            data = Data.objects.get(data=data_data)

            data_anterior = Dados.objects.filter(data__lt=data, id_jaula=dadosjaula_form.data['id_jaula']).order_by('-data').first()

        jaula = Jaula.objects.get(id=dadosjaula_form.data['id_jaula'])

        print(data_anterior.num_peixes)
        print(data_anterior.PM)
        
        if (data_anterior != None):
            num_peixes = int(data_anterior.num_peixes) - int(data_anterior.num_mortos_real)
        else:
            #temporario
            num_peixes = int(dadosjaula_form.data['num_peixes'])

        PM = data_anterior.PM_real

        Biom = float(PM) * num_peixes
        
        percentagem_alimentacao = float(dadosjaula_form.data['percentagem_alimentacao'])
        
        peso = float(data_anterior.Biom) * percentagem_alimentacao
        
        sacos_racao = peso * 25
        
        FC_real = float(dadosjaula_form.data['FC'])
        
        if (dadosjaula_form.data['alimentacao_real'] == ''):
            alimentacao_real = peso * 30
        else:
            alimentacao_real = float(dadosjaula_form.data['alimentacao_real'])
        
        FC = int(alimentacao_real) / ( (int(data_anterior.num_peixes) * float(data_anterior.PM)) - (int(num_peixes) * float(PM)) )

        PM_teorica_alim_real = (alimentacao_real / FC + Biom) / num_peixes
        
        PM_teorico = PM_teorica_alim_real
        
        if (dadosjaula_form.data['PM_real'] == ''):
            PM_real = PM_teorico
        else:
            PM_real = dadosjaula_form.data['PM_real']
        
        percentagem_mortalidade_teorica = alimentacao_real
        
        num_mortos_teorico = num_peixes * percentagem_mortalidade_teorica
        
        if (dadosjaula_form.data['num_mortos_real'] == ''):
            num_mortos_real = num_mortos_teorico
        else:
            num_mortos_real = int(dadosjaula_form.data['num_mortos_real'])
        
        if (dadosjaula_form.data['num_mortos_real'] == ''):
            num_mortos_real = num_mortos_teorico
        else:
            num_mortos_real = int(dadosjaula_form.data['num_mortos_real'])
        
        if (dadosjaula_form.data['percentagem_mortalidade_real'] == ''):
            percentagem_mortalidade_real = float(num_mortos_real / num_peixes * 100)
        else:
            percentagem_mortalidade_real = dadosjaula_form.data['percentagem_mortalidade_real']
        
        peso_medio = 1
        
        
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
        dados = Dados(
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
def transicoes(request):
    if request.method == 'POST':
        transicoesJaula_form = TransicoesJaulaForm(request.POST)
        data_form = DataForm(request.POST)

        if transicoesJaula_form.is_valid():
            #jaulaInicio = transicoesJaula_form.data['jaula_inicio']
            #jaulaFim = transicoesJaula_form.data['jaula_fim']
            #models.Movimento.objects.get(id_jaula = jaulaInicio).update(num = models.Movimento.objects.get(id_jaula = jaulaInicio).num - transicoesJaula_form.data['num'])
            #models.Movimento.objects.get(id_jaula = jaulaFim).update(num = models.Movimento.objects.get(id_jaula = jaulaFim).num + transicoesJaula_form.data['num'])
            try:
                #case there is no data
                if data_form.is_valid():
                    data = data_form.save()

                transicao = transicoesJaula_form.save(commit=False)
                transicao.data = data
                transicao.save()
                messages.success(request, 'Movimento Registado com Sucesso!')
            except:
                #case already exists data
                data_data = data_form.data['data']
                data = Data.objects.get(data=data_data)
                transicao = transicoesJaula_form.save(commit=False)
                transicao.data = data
                transicao.save()
                messages.success(request, 'Movimento Registado com Sucesso!')

        else:
            messages.success(request,('Erro!'))
    else:
        transicoesJaula_form = TransicoesJaulaForm()
        data_form = DataForm()
    return render(request, 'transicoes.html', {'TransicoesJaulaForm': transicoesJaula_form, 'data_form': data_form})



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
