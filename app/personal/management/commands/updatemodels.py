import pandas as pd
from personal.models import *
import os
from django.core.management.base import BaseCommand
from datetime import datetime
from openpyxl import load_workbook
import calendar
import xlrd
class Command(BaseCommand):
    help = 'import booms'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        files = os.listdir("Ficheiros PECI")
        for file in files:
            if file.endswith("xls") or file.endswith("xlsx"):
                df = pd.read_excel("Ficheiros PECI/"+file)
                df2 = df.fillna(0)
            if file.startswith("Desovas"):
                for DATA, FEMEAS, DESOVADOS, EMBRIONADOS in zip(df2.Data,df2.Fêmeas,df2.Desovados,df2.Embrionados):
                    if (DATA and FEMEAS and DESOVADOS and EMBRIONADOS ) != 0 :
                        DATA = dataFormat(DATA)
                        if not dataIsValid(DATA) or not (str(FEMEAS).isdigit() or str(DESOVADOS).isdigit() or str(EMBRIONADOS).isdigit()):
                            continue
                        models = Desova(data = str(DATA), femeas = FEMEAS, desovados = DESOVADOS, embrionados = EMBRIONADOS)
                        models.save()
            if file.startswith("Temperaturas"):
                print(file) 
                wb = xlrd.open_workbook("Ficheiros PECI/"+file)
                ## por agora não há médias
                ano = file[13:17]
                ws = wb.sheet_by_name(str(ano))
                print(ano)
                mes =1
                for row_index in range(ws.nrows):
                    row = ws.row(row_index)
                    if mes == 12:
                        break
                    if not isMonth(row[0].value) :
                        continue
                    mes = month_to_number(row[0].value)
                    for index in range(1,31):
                        dia =str(index)
                        if len(str(mes)) != 2:
                            mes = "0"+str(mes)
                        if len(str(dia)) != 2:
                            dia = "0"+str(dia)
                        if len (str(row[index].value)) ==0 or (str(mes) == "02" and (dia =="30" or dia =="31")):
                            continue
                        models = Temperatura(data = str(ano)+"-"+str(mes)+"-"+str(dia),temperatura=row[index].value )
                        models.save()
                ### ultima tabela aqui
            if file.startswith("Cópia de Dados"):
                print("Ficheiros PECI/"+file) 
                wb = xlrd.open_workbook("Ficheiros PECI/"+file)
                ## Eventrualmente generalizer com base no nome do ficheiro
                worksheet = wb.sheet_by_index(1)
                table_start = False
                ano = 0
                for row_index in range(worksheet.nrows):
                    cell = worksheet.cell(row_index, 1)
                    if cell.ctype == xlrd.XL_CELL_DATE or isMonth(cell.value):
                        table_start = True
                    else:
                        if table_start:
                            break
                    if table_start:
                        if cell.ctype == xlrd.XL_CELL_DATE:
                            date = xlrd.xldate_as_datetime(cell.value, wb.datemode)
                            date = str(date).split(" ")[0]
                            print(date)
                            ano = date.split("-")[0]
                        else :
                            mes = month_to_number(cell.value)
                            if len(str(mes))!=2:
                                mes = "0"+str(mes)
                            date = str(ano)+"-"+str(mes)+"-"+str(15)
                        models = Jaula(data = date, num_peixes = worksheet.cell(row_index,2).value,
                        PM = worksheet.cell(row_index,3).value, Biom = worksheet.cell(row_index,4).value,
                        percentagem_alimentacao = worksheet.cell(row_index,5).value, peso =worksheet.cell(row_index,6).value,
                        sacos_racao = worksheet.cell(row_index,7).value, FC = worksheet.cell(row_index,9).value,
                        peso_medio = worksheet.cell(row_index,12).value, PM_teorica_alim_real = worksheet.cell(row_index,13).value,
                        alimentacao_real = worksheet.cell(row_index,14).value, PM_teorico = worksheet.cell(row_index,15).value,
                        PM_real = worksheet.cell(row_index,16).value, percentagem_mortalidade_teorica  = worksheet.cell(row_index,18).value,
                        num_mortos_teorico = worksheet.cell(row_index,19).value, percentagem_mortalidade_real = worksheet.cell(row_index,20).value,
                        num_mortos_real = worksheet.cell(row_index,21).value, FC_real = toNone(worksheet.cell(row_index,25).value),
                        retirados = 0, volume = 0 , colocados = 0, id = int(worksheet.name.split(" ")[1]))
                        models.save()

                        
        



def dataFormat(data):
    data = str(data)
    data = data.split(" ")
    return data[0]
def dataIsValid(data):
  try:
    datetime.strptime(data, '%Y-%m-%d')
    return True
  except ValueError:
    return False

def month_to_number(month_name):
    month_name = month_name.lower()
    month_names = [
        "janeiro", "fevereiro", "março", "abril", "maio", "junho",
        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
    ]
    month_number = month_names.index(month_name) + 1
    return month_number
def isMonth(month_name):
    month_name = month_name.lower()
    month_names = [
        "janeiro", "fevereiro", "março", "abril", "maio", "junho",
        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
    ]
    return month_name in month_names

def toNone(string):
    if str(string) == '':
        return 0
    return string
