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
    temp_form = TemperaturaArrayForm()
    data_form = DataForm(prefix="inicial")
    data_final_form = DataForm(prefix="final")
    if request.method == 'POST':
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
                    return render(request, 'ins_excel_temp.html', {'temp_form': temp_form, 'data_form': data_form, 'data_final_form': data_final_form})
                else:   
                    for t,d in zip(temp_array,range(num_days)):
                        current_date = data_i + timedelta(days=d)
                        date = Data(data=current_date)
                        if not Data.objects.filter(data=current_date).exists():
                            date.save()
                        temp = Temperatura(temperatura=t,data=date)
                        temp.save()
                    messages.success(request, 'Dados Temperatura adicionado!')
                    return render(request, 'ins_excel_temp.html', {'temp_form': temp_form, 'data_form': data_form, 'data_final_form': data_final_form})
            except Exception as e:
                print(e)
                print("not Valid")
                return render(request, 'ins_excel_temp.html', {'temp_form': temp_form, 'data_form': data_form, 'data_final_form': data_final_form})
        #         data_data = data_form.data['data']
        #         data = Data.objects.get(data=data_data)
        #         temp = temp_form.save(commit=False)
        #         temp.data = data
        #         temp.save()
        #         messages.success(request, 'Dados Temperatura adicionado!')
        # else:
        #     messages.success(request, 'Erro!')
    else:
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
        
        #try:    #if data NOT exists
        
        if data_form.is_valid():
            print("asdasd")
            data = data_form.save()

        dadosjaula = DadosJaulaForm(request.POST)
        dadosjaula.data = data
        print("asdasdasd")
        print(dadosjaula.data)
        print("asdasdasd")
        data_anterior = Dados.objects.filter(data__lt=dadosjaula.data).order_by('-data').first()

        if (dadosjaula_form.data['num_peixes'] == ''):
            dadosjaula.num_peixes = data_anterior.num_peixes - data_anterior.num_mortos_real
        else:
            dadosjaula.num_peixes = dadosjaula_form.data['num_peixes']
        
        dadosjaula.PM = dadosjaula_form.data['PM']

        dadosjaula.Biom = float(dadosjaula.PM) * int(dadosjaula.num_peixes)
        
        dadosjaula.percentagem_alimentacao = dadosjaula_form.data['percentagem_alimentacao']
        
        dadosjaula.peso = float(data_anterior.Biom) * float(dadosjaula.percentagem_alimentacao)
        
        dadosjaula.sacos_racao = float(dadosjaula.peso) * 25
        
        dadosjaula.FC = dadosjaula_form.data['FC']
        
        # perguntar sobre isto
        if (dadosjaula_form.data['alimentacao_real'] == ''):
            dadosjaula.alimentacao_real = float(dadosjaula.peso) * 30
        else:
            dadosjaula.alimentacao_real = dadosjaula_form.data['alimentacao_real']
        
        dadosjaula.PM_teorica_alim_real = (float(dadosjaula.alimentacao_real) / float(dadosjaula.FC) + float(dadosjaula.Biom)) / int(dadosjaula.num_peixes)
        
        #perguntar sobre isto
        dadosjaula.PM_teorico = None
        
        if (dadosjaula_form.data['PM_real'] == ''):
            dadosjaula.PM_real = dadosjaula.PM_teorico
        else:
            dadosjaula.PM_real = dadosjaula_form.data['PM_real']
        dadosjaula.percentagem_mortalidade_teorica = dadosjaula.alimentacao_real
        dadosjaula.num_mortos_teorico = int(dadosjaula.num_peixes) * float(dadosjaula.percentagem_mortalidade_teorica)
        
        if (dadosjaula_form.data['num_mortos_real'] == ''):
            dadosjaula.num_mortos_real = dadosjaula.num_mortos_teorico
        else:
            dadosjaula.num_mortos_real = dadosjaula_form.data['num_mortos_real']
        
        if (dadosjaula_form.data['percentagem_mortalidade_real'] == ''):
            dadosjaula.percentagem_mortalidade_real = int(dadosjaula.num_mortos_real) / int(dadosjaula.num_peixes * 100)
        else:
            dadosjaula.percentagem_mortalidade_real = dadosjaula_form.data['percentagem_mortalidade_real']
        
        dadosjaula.peso_medio = None
        dadosjaula.FC_real = int(dadosjaula.alimentacao_real) / ( (int(data_anterior.num_peixes) * int(data_anterior.PM)) - (int(dadosjaula.num_peixes) * int(dadosjaula.PM)) )
        

        dadosjaula.save()

        print("Simmmmmmmmmmmmmmmmmmmm")

        """
        except: 
            #if data exists
            data_data = data_form.data['data']
            data = Data.objects.get(data=data_data)

            dadosjaula = dadosjaula_form.save(commit=False)
            dadosjaula.data = data
            data_anterior = Dados.get_previous_date(dadosjaula.data)


            if (dadosjaula_form.data['num_peixes'] == None):
                dadosjaula.num_peixes = data_anterior.num_peixes - data_anterior.num_mortos_real
            else:
                dadosjaula.num_peixes = dadosjaula_form.data['num_peixes']

            dadosjaula.Biom = dadosjaula.PM * dadosjaula.num_peixes
            
            dadosjaula.percentagem_alimentacao = dadosjaula_form.data['percentagem_alimentacao']
            
            dadosjaula.peso = data_anterior.Biom * dadosjaula.percentagem_alimentacao
            
            dadosjaula.sacos_racao = dadosjaula.peso * 25
            
            dadosjaula.FC = dadosjaula_form.data['FC']
            
            # perguntar sobre isto
            if (dadosjaula_form.data['alimentacao_real'] == None):
                dadosjaula.alimentacao_real = dadosjaula.peso * 30
            else:
                dadosjaula.alimentacao_real = dadosjaula_form.data['alimentacao_real']

            dadosjaula.PM_teorica_alim_real = (dadosjaula.alimentacao_real / dadosjaula.FC + dadosjaula.Biom) / dadosjaula.num_peixes

            #perguntar sobre isto
            dadosjaula.PM_teorico = None

            if (dadosjaula_form.data['PM_real'] == None):
                dadosjaula.PM_real = dadosjaula.PM_teorico
            else:
                dadosjaula.PM_real = dadosjaula_form.data['PM_real']

            dadosjaula.percentagem_mortalidade_teorica = dadosjaula.alimentacao_real

            dadosjaula.num_mortos_teorico = dadosjaula.num_peixes * dadosjaula.percentagem_mortalidade_teorica

            if (dadosjaula_form.data['num_mortos_real'] == None):
                dadosjaula.num_mortos_real = dadosjaula.num_mortos_teorico
            else:
                dadosjaula.num_mortos_real = dadosjaula_form.data['num_mortos_real']

            if (dadosjaula_form.data[''] == None):
                dadosjaula.percentagem_mortalidade_real = dadosjaula.num_mortos_real / dadosjaula.num_peixes * 100
            else:
                dadosjaula.percentagem_mortalidade_real = dadosjaula_form.data['percentagem_mortalidade_real']

            dadosjaula.peso_medio = None

            dadosjaula.FC_real = dadosjaula.alimentacao_real / ( (data_anterior.num_peixes * data_anterior.PM) - (dadosjaula.num_peixes * dadosjaula.PM) )

            """
        
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
