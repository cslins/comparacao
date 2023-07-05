
import numpy as np           
import skfuzzy as fz
import pandas as pd
import xlrd
import openpyxl

pasta = "0_res_agnt_simples_en0_dataset_artigo_marcos_filipe_2.xlsx"
# excel = pd.read_excel(pasta, sheet_name='res_ag_simples_en0', header=0, engine='openpyxl')

def sistsimples(filename):
    excel = pd.read_excel(filename)
    list_eb = []


    en = 0

    for i in range(len(excel)):
        h = excel["Hora"][i]
        el = excel["El_KW"][i]


        #quando o consumo residencial é igual à energia produzida pelo gerador:
        if (el==0):
            eb = 0

        #quando há excedente de energia:
        if (el>0):
            #caso a energia da bateria não esteja 100% carregada:
            if(en<70):
                eb = el

            #caso a bateria esteja 100% carregada, a produção excedente é enviada para a rede de distribuição:
            elif(en>=70):
                eb = 0

        #quando há necessidade de mais energia:
        if (el<0):
            #durante o horário de 17:30h e 22:30h (tarifa mais cara) e
            #caso a bateria esteja com carga acima de 25%, a residência utiliza a energia armazenada na bateria:
            if (h>=17.5 and h<=22.5 and en>17.5):
                eb = el

            #durante o horário anterior a 17:30h ou superior a 22:30h (tarifa mais barata) ou
            #caso a bateria esteja com carga abaixo de 25%, a residência utiliza a energia da rede de distribuição:	
            elif (h<17.5 or h>22.5 or en<=17.5):
                eb = 0

        en = en+(eb*5/60)
        soc = 100*en/70
        list_eb.append(eb)

    return list_eb, excel