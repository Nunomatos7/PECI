from django.core.management.base import BaseCommand
import pandas as pd
from personal.models import *
import os
class Comand(BaseCommand):
    help = 'import booms'

    def add_arguments(self, parser):
        pass  

    def handle(self, *args, **options): 
        files = os.listdir("../../../Ficheiros PECI/")
        print(files)
        for file in files:
            df = pd.read_excel(file)
            if file.startswith("Desovas"):
                for DATA, FEMEAS, DESOVADOS, EMBRIONADOS in zip(df.Data,df.Fêmeas,df.Desovados,df.Embrionados):
                    if (DATA and FEMEAS and DESOVADOS and EMBRIONADOS ) != None:
                        models = Desova(data = DATA, femeas = FEMEAS, desovados = DESOVADOS, embrionados = EMBRIONADOS)
                        models.save()