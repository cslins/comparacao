import numpy as np           
import skfuzzy as fz
import matplotlib.pyplot as mp
from skfuzzy import control as ctrl
import pandas as pd
import xlrd
import openpyxl

def sistfuzzy(filename):

    positive_liquid_energy = ctrl.Antecedent(np.arange(0,4.1,0.1),'positive_liquid_energy')
    negative_liquid_energy = ctrl.Antecedent(np.arange(-6,0.1,0.1),'negative_liquid_energy')
    state_of_charge = ctrl.Antecedent(np.arange(0,101,1),'state_of_charge')
    battery_situation = ctrl.Consequent(np.arange(0,101,1),'battery_situation','lom') # 'lom' => método de defuzzificação max of maximum


    positive_liquid_energy['positive_big'] = fz.gaussmf(positive_liquid_energy.universe, 4, 0.7)
    positive_liquid_energy['positive_small'] = fz.gaussmf(positive_liquid_energy.universe, 2.5, 0.7)
    positive_liquid_energy['zero'] = fz.gaussmf(positive_liquid_energy.universe, 0, 0.7)

    negative_liquid_energy['zero'] = fz.gaussmf(negative_liquid_energy.universe, 0, 1)
    negative_liquid_energy['negative_small'] = fz.gaussmf(negative_liquid_energy.universe, -4, 1)
    negative_liquid_energy['negative_big'] = fz.gaussmf(negative_liquid_energy.universe, -6, 1)
    

    state_of_charge['positive_big'] = fz.sigmf(state_of_charge.universe, 90, 0.3)
    state_of_charge['positive_small'] = fz.gaussmf(state_of_charge.universe, 75, 12)
    state_of_charge['zero'] = fz.gaussmf(state_of_charge.universe, 30, 12)
    state_of_charge['negative_big'] = fz.sigmf(state_of_charge.universe, 30, -0.4)

    
    battery_situation['positive_big'] = fz.gaussmf(battery_situation.universe, 100, 20)
    battery_situation['zero'] = fz.gaussmf(battery_situation.universe, 55, 27)
    battery_situation['negative_big'] = fz.trimf(battery_situation.universe, [0, 0, 0])


    # positive_liquid_energy.view()
    # negative_liquid_energy.view()
    # state_of_charge.view()
    # battery_situation.view()



    #%%


    #Cria as regras de decisão difusas:
        
    # Regras no caso da energia liquida ser positiva

    battery_situation_ctrl_positive = ctrl.ControlSystem([
    ctrl.Rule(positive_liquid_energy['positive_big'] & state_of_charge['positive_big'], battery_situation['zero']),
    ctrl.Rule(positive_liquid_energy['positive_big'] & state_of_charge['positive_small'], battery_situation['positive_big']),
    ctrl.Rule(positive_liquid_energy['positive_big'] & state_of_charge['zero'], battery_situation['positive_big']),
    ctrl.Rule(positive_liquid_energy['positive_big'] & state_of_charge['negative_big'], battery_situation['positive_big']),

    ctrl.Rule(positive_liquid_energy['positive_small'] & state_of_charge['positive_big'], battery_situation['zero']),
    ctrl.Rule(positive_liquid_energy['positive_small'] & state_of_charge['positive_small'], battery_situation['positive_big']),
    ctrl.Rule(positive_liquid_energy['positive_small'] & state_of_charge['zero'], battery_situation['positive_big']),
    ctrl.Rule(positive_liquid_energy['positive_small'] & state_of_charge['negative_big'], battery_situation['positive_big']),

    ctrl.Rule(positive_liquid_energy['zero'] & state_of_charge['positive_big'], battery_situation['zero']),
    ctrl.Rule(positive_liquid_energy['zero'] & state_of_charge['positive_small'], battery_situation['positive_big']),
    ctrl.Rule(positive_liquid_energy['zero'] & state_of_charge['zero'], battery_situation['positive_big']),
    ctrl.Rule(positive_liquid_energy['zero'] & state_of_charge['negative_big'], battery_situation['positive_big'])
    ])


    battery_situation_simulador_positive = ctrl.ControlSystemSimulation(battery_situation_ctrl_positive)



    # Rules for the most cheap time interval:

    battery_situation_ctrl_barata = ctrl.ControlSystem([

    
    ctrl.Rule(negative_liquid_energy['zero'] & state_of_charge['positive_big'], battery_situation['positive_big']),
    ctrl.Rule(negative_liquid_energy['zero'] & state_of_charge['positive_small'], battery_situation['positive_big']),
    ctrl.Rule(negative_liquid_energy['zero'] & state_of_charge['zero'], battery_situation['negative_big']),
    ctrl.Rule(negative_liquid_energy['zero'] & state_of_charge['negative_big'], battery_situation['negative_big']),

    ctrl.Rule(negative_liquid_energy['negative_small'] & state_of_charge['positive_big'], battery_situation['positive_big']),
    ctrl.Rule(negative_liquid_energy['negative_small'] & state_of_charge['positive_small'], battery_situation['positive_big']),
    ctrl.Rule(negative_liquid_energy['negative_small'] & state_of_charge['zero'], battery_situation['negative_big']),
    ctrl.Rule(negative_liquid_energy['negative_small'] & state_of_charge['negative_big'], battery_situation['negative_big']),

    ctrl.Rule(negative_liquid_energy['negative_big'] & state_of_charge['positive_big'], battery_situation['positive_big']),
    ctrl.Rule(negative_liquid_energy['negative_big'] & state_of_charge['positive_small'], battery_situation['zero']),
    ctrl.Rule(negative_liquid_energy['negative_big'] & state_of_charge['zero'], battery_situation['negative_big']),
    ctrl.Rule(negative_liquid_energy['negative_big'] & state_of_charge['negative_big'], battery_situation['negative_big'])
    ])


    # Rules for the intermediate time interval:

    battery_situation_ctrl_intermediaria = ctrl.ControlSystem([
    ctrl.Rule(negative_liquid_energy['zero'] & state_of_charge['positive_big'], battery_situation['positive_big']),
    ctrl.Rule(negative_liquid_energy['zero'] & state_of_charge['positive_small'], battery_situation['positive_big']),
    ctrl.Rule(negative_liquid_energy['zero'] & state_of_charge['zero'], battery_situation['positive_big']),
    ctrl.Rule(negative_liquid_energy['zero'] & state_of_charge['negative_big'], battery_situation['negative_big']),

    ctrl.Rule(negative_liquid_energy['negative_small'] & state_of_charge['positive_big'], battery_situation['positive_big']),
    ctrl.Rule(negative_liquid_energy['negative_small'] & state_of_charge['positive_small'], battery_situation['positive_big']),
    ctrl.Rule(negative_liquid_energy['negative_small'] & state_of_charge['zero'], battery_situation['positive_big']),
    ctrl.Rule(negative_liquid_energy['negative_small'] & state_of_charge['negative_big'], battery_situation['negative_big']),

    ctrl.Rule(negative_liquid_energy['negative_big'] & state_of_charge['positive_big'], battery_situation['positive_big']),
    ctrl.Rule(negative_liquid_energy['negative_big'] & state_of_charge['positive_small'], battery_situation['positive_big']),
    ctrl.Rule(negative_liquid_energy['negative_big'] & state_of_charge['zero'], battery_situation['positive_big']),
    ctrl.Rule(negative_liquid_energy['negative_big'] & state_of_charge['negative_big'], battery_situation['negative_big'])
    ])



    # Rules for the most expensive time interval:
    battery_situation_ctrl_cara = ctrl.ControlSystem([
    ctrl.Rule(negative_liquid_energy['zero'] & state_of_charge['positive_big'], battery_situation['positive_big']),
    ctrl.Rule(negative_liquid_energy['zero'] & state_of_charge['positive_small'], battery_situation['positive_big']),
    ctrl.Rule(negative_liquid_energy['zero'] & state_of_charge['zero'], battery_situation['positive_big']),
    ctrl.Rule(negative_liquid_energy['zero'] & state_of_charge['negative_big'], battery_situation['positive_big']),


    ctrl.Rule(negative_liquid_energy['negative_small'] & state_of_charge['positive_big'], battery_situation['positive_big']),
    ctrl.Rule(negative_liquid_energy['negative_small'] & state_of_charge['positive_small'], battery_situation['positive_big']),
    ctrl.Rule(negative_liquid_energy['negative_small'] & state_of_charge['zero'], battery_situation['positive_big']),
    ctrl.Rule(negative_liquid_energy['negative_small'] & state_of_charge['negative_big'], battery_situation['negative_big']),

    ctrl.Rule(negative_liquid_energy['negative_big'] & state_of_charge['positive_big'], battery_situation['positive_big']),
    ctrl.Rule(negative_liquid_energy['negative_big'] & state_of_charge['positive_small'], battery_situation['positive_big']),
    ctrl.Rule(negative_liquid_energy['negative_big'] & state_of_charge['zero'], battery_situation['zero']),
    ctrl.Rule(negative_liquid_energy['negative_big'] & state_of_charge['negative_big'], battery_situation['negative_big'])
    ])

    #Cria e simula um controlador nebuloso:

    battery_situation_simulador_barata = ctrl.ControlSystemSimulation(battery_situation_ctrl_barata)

    battery_situation_simulador_intermediaria = ctrl.ControlSystemSimulation(battery_situation_ctrl_intermediaria)

    battery_situation_simulador_cara = ctrl.ControlSystemSimulation(battery_situation_ctrl_cara)

    #Entra com valores para as variáveis:
    #battery_situation_simulador.input['liquid_energy'] = 0.1
    #battery_situation_simulador.input['state_of_charge'] = 20
    pasta = "1_res_fuzzy_en0_dataset_artigo_marcos_filipe1.xlsx"
    # excel = pd.read_excel(pasta, sheet_name='res_fuzzy_en0', header=0, engine='openpyxl')
    excel = pd.read_excel(filename)
    # excel = df.copy()

    en = 0
    soc = 0

    list_eb_percent = []
    list_eb = []
    list_en = []
    list_soc = []

    # %%

    #Computa o resultado:
    for i in range(len(excel)):
        
        
        if excel["El_KW"][i] >= 0:
            
            battery_limit = ((70 - en) * 60)/5  # cálculo do limite de energia que a bateria pode receber
            
            battery_situation_simulador_positive.input['positive_liquid_energy'] = excel["El_KW"][i]
            battery_situation_simulador_positive.input['state_of_charge'] = soc
            battery_situation_simulador_positive.compute()
            eb_percent = battery_situation_simulador_positive.output['battery_situation']
            if eb_percent is None:
                eb_percent = 0
            
            # se a energia liquida é a maior que a quantidade limite
            # o cálculo de eb é feito utilizando o limite
            if battery_limit < excel["El_KW"][i]:
                eb = battery_limit*(eb_percent/100)
            else:
                eb = excel["El_KW"][i]*(eb_percent/100)
        else:
            
            battery_limit = -60*en/5 # cálculo do limite de energia que a bateria pode descarregar
            
            hour = excel["Hora"][i]
            if (hour>=0 and hour<17.50):
                battery_situation_simulador_barata.input['negative_liquid_energy'] = excel["El_KW"][i]
                battery_situation_simulador_barata.input['state_of_charge'] = soc
                battery_situation_simulador_barata.compute()
                eb_percent = battery_situation_simulador_barata.output['battery_situation']
                if eb_percent is None:
                    eb_percent = 0

            elif (hour>=17.50 and hour<18.50):
                battery_situation_simulador_intermediaria.input['negative_liquid_energy'] = excel["El_KW"][i]
                battery_situation_simulador_intermediaria.input['state_of_charge'] = soc
                battery_situation_simulador_intermediaria.compute()
                eb_percent = battery_situation_simulador_intermediaria.output['battery_situation']
                if eb_percent is None:
                    eb_percent = 0

            elif (hour>=18.50 and hour<21.50):
                battery_situation_simulador_cara.input['negative_liquid_energy'] = excel["El_KW"][i]
                battery_situation_simulador_cara.input['state_of_charge'] = soc
                battery_situation_simulador_cara.compute()
                eb_percent = battery_situation_simulador_cara.output['battery_situation']
                if eb_percent is None:
                    eb_percent = 0

            elif (hour>=21.50 and hour<22.50):
                battery_situation_simulador_intermediaria.input['negative_liquid_energy'] = excel["El_KW"][i]
                battery_situation_simulador_intermediaria.input['state_of_charge'] = soc
                battery_situation_simulador_intermediaria.compute()
                eb_percent = battery_situation_simulador_intermediaria.output['battery_situation']
                if eb_percent is None:
                    eb_percent = 0

            elif (hour>=22.50 and hour<24.00):
                battery_situation_simulador_barata.input['negative_liquid_energy'] = excel["El_KW"][i]
                battery_situation_simulador_barata.input['state_of_charge'] = soc
                battery_situation_simulador_barata.compute()
                eb_percent = battery_situation_simulador_barata.output['battery_situation']
                if eb_percent is None:
                    eb_percent = 0
            
            # se a energia liquida é a maior que a quantidade limite
            # o cálculo de eb é feito utilizando o limite
            if battery_limit > excel["El_KW"][i]:
                eb = battery_limit*(eb_percent/100)
            else:
                eb = excel["El_KW"][i]*(eb_percent/100)
        

        en = en+(eb*5/60)   
        soc = 100*en/70
        list_soc.append(soc)
        list_eb.append(eb)
        list_eb_percent.append(eb_percent)

    return list_eb, list_eb_percent, list_soc, excel

    #%%
    # textfile = open("file_eb.txt", "w")
    # for element in list_eb:
    #     textfile.write(str(element).upper().replace('.', ',', 1) + "\n")
    # textfile.close()

    # print(list_eb)

    # textfile = open("file_soc.txt", "w")
    # for element in list_soc:
    #     textfile.write(str(element).upper().replace('.', ',', 1) + "\n")
    # textfile.close()


