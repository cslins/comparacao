"""
Created on Oct 05 2020
Updated_1 on Mai 05 2021
Updated_2 on Jun 07 2021
Updated_3 on Jan 12 2022
@author: Raimunda Branco

"Agente Fuzzy"
"""

import numpy as np           
import skfuzzy as fz
import matplotlib.pyplot as mp
from skfuzzy import control as ctrl
import pandas as pd
import xlrd
import openpyxl

# Cria as variáveis de entrada (antecedentes) do problema:
# liquid energy (El) = energy produced by the distributed generator (Eg) - energy consumed by the consumer load (Ec)

def sistfuzzyorig(filename):
    
    liquid_energy = ctrl.Antecedent(np.arange(-6,4.1,0.1),'liquid_energy')
    # state_of_charge (SoC) is the level of eletricity charge stored in the battery
    state_of_charge = ctrl.Antecedent(np.arange(0,101,1),'state_of_charge')


    #  Cria a variável de saída (consequente) do problema:
    # battery_situation (Eb) is a decision about if the battery will be charged or discharged
    battery_situation = ctrl.Consequent(np.arange(-6,6.1,0.1),'battery_situation')

    """
    #Cria automaticamente o mapeamento entre valores nítidos e difusos usando uma função de pertinência padrão (triangular):
    liquid_energy.automf(names=['positive_big', 'positive_small', 'zero', 'negative_small', 'negative_big'])

    """

    # Cria as funções de pertinência usando tipos variados:

    liquid_energy['positive_big'] = fz.trapmf(liquid_energy.universe, [2, 4, 6, 7])
    liquid_energy['positive_small'] = fz.trimf(liquid_energy.universe, [0, 2, 4])
    liquid_energy['zero'] = fz.trimf(liquid_energy.universe, [-2, 0, 2])
    liquid_energy['negative_small'] = fz.trimf(liquid_energy.universe, [-4, -2.5, 0])
    liquid_energy['negative_big'] = fz.trapmf(liquid_energy.universe, [-7, -6, -4, -2])

    state_of_charge['positive_big'] = fz.trimf(state_of_charge.universe, [75, 100, 100])
    state_of_charge['positive_small'] = fz.trimf(state_of_charge.universe, [50, 75, 100])
    state_of_charge['zero'] = fz.trimf(state_of_charge.universe, [25, 50, 75])
    state_of_charge['negative_small'] = fz.trimf(state_of_charge.universe, [0, 25, 50])
    state_of_charge['negative_big'] = fz.trimf(state_of_charge.universe, [0, 0, 40])

    battery_situation['positive_big'] = fz.trimf(battery_situation.universe, [4.2, 6, 6])
    battery_situation['positive_small'] = fz.trimf(battery_situation.universe, [0, 2.1, 4.5])
    battery_situation['zero'] = fz.trimf(battery_situation.universe, [-3, 0, 3])
    battery_situation['negative_small'] = fz.trimf(battery_situation.universe, [-4, -2.1, 0])
    battery_situation['negative_big'] = fz.trimf(battery_situation.universe, [-6, -6, -4.3])

    #Mostra graficamente as funções de partinência criadas:
    # liquid_energy.view()
    # state_of_charge.view()
    # battery_situation.view()

    #Cria as regras de decisão difusas:
    # Rules for the most cheap time interval:
    rule1 = ctrl.Rule(liquid_energy['positive_big'] & state_of_charge['positive_big'], battery_situation['zero'])
    rule2 = ctrl.Rule(liquid_energy['positive_big'] & state_of_charge['positive_small'], battery_situation['positive_small'])
    rule3 = ctrl.Rule(liquid_energy['positive_big'] & state_of_charge['zero'], battery_situation['positive_small'])
    rule4 = ctrl.Rule(liquid_energy['positive_big'] & state_of_charge['negative_small'], battery_situation['positive_big'])
    rule5 = ctrl.Rule(liquid_energy['positive_big'] & state_of_charge['negative_big'], battery_situation['positive_big'])

    rule6 = ctrl.Rule(liquid_energy['positive_small'] & state_of_charge['positive_big'], battery_situation['zero'])
    rule7 = ctrl.Rule(liquid_energy['positive_small'] & state_of_charge['positive_small'], battery_situation['positive_small'])
    rule8 = ctrl.Rule(liquid_energy['positive_small'] & state_of_charge['zero'], battery_situation['positive_big'])
    rule9 = ctrl.Rule(liquid_energy['positive_small'] & state_of_charge['negative_small'], battery_situation['positive_small'])
    rule10 = ctrl.Rule(liquid_energy['positive_small'] & state_of_charge['negative_big'], battery_situation['positive_small'])

    rule11 = ctrl.Rule(liquid_energy['zero'] & state_of_charge['positive_big'], battery_situation['zero'])
    rule12 = ctrl.Rule(liquid_energy['zero'] & state_of_charge['positive_small'], battery_situation['zero'])
    rule13 = ctrl.Rule(liquid_energy['zero'] & state_of_charge['zero'], battery_situation['zero'])
    rule14 = ctrl.Rule(liquid_energy['zero'] & state_of_charge['negative_small'], battery_situation['zero'])
    rule15 = ctrl.Rule(liquid_energy['zero'] & state_of_charge['negative_big'], battery_situation['zero'])

    rule16 = ctrl.Rule(liquid_energy['negative_small'] & state_of_charge['positive_big'], battery_situation['negative_big'])
    rule17 = ctrl.Rule(liquid_energy['negative_small'] & state_of_charge['positive_small'], battery_situation['negative_small'])
    rule18 = ctrl.Rule(liquid_energy['negative_small'] & state_of_charge['zero'], battery_situation['zero'])
    rule19 = ctrl.Rule(liquid_energy['negative_small'] & state_of_charge['negative_small'], battery_situation['zero'])
    rule20 = ctrl.Rule(liquid_energy['negative_small'] & state_of_charge['negative_big'], battery_situation['zero'])

    rule21 = ctrl.Rule(liquid_energy['negative_big'] & state_of_charge['positive_big'], battery_situation['negative_big'])
    rule22 = ctrl.Rule(liquid_energy['negative_big'] & state_of_charge['positive_small'], battery_situation['negative_small'])
    rule23 = ctrl.Rule(liquid_energy['negative_big'] & state_of_charge['zero'], battery_situation['zero'])
    rule24 = ctrl.Rule(liquid_energy['negative_big'] & state_of_charge['negative_small'], battery_situation['zero'])
    rule25 = ctrl.Rule(liquid_energy['negative_big'] & state_of_charge['negative_big'], battery_situation['zero'])

    # Rules for the intermediate time interval:
    rule26 = ctrl.Rule(liquid_energy['positive_big'] & state_of_charge['positive_big'], battery_situation['zero'])
    rule27 = ctrl.Rule(liquid_energy['positive_big'] & state_of_charge['positive_small'], battery_situation['positive_small'])
    rule28 = ctrl.Rule(liquid_energy['positive_big'] & state_of_charge['zero'], battery_situation['positive_small'])
    rule29 = ctrl.Rule(liquid_energy['positive_big'] & state_of_charge['negative_small'], battery_situation['positive_big'])
    rule30 = ctrl.Rule(liquid_energy['positive_big'] & state_of_charge['negative_big'], battery_situation['positive_big'])

    rule31 = ctrl.Rule(liquid_energy['positive_small'] & state_of_charge['positive_big'], battery_situation['zero'])
    rule32 = ctrl.Rule(liquid_energy['positive_small'] & state_of_charge['positive_small'], battery_situation['positive_small'])
    rule33 = ctrl.Rule(liquid_energy['positive_small'] & state_of_charge['zero'], battery_situation['positive_big'])
    rule34 = ctrl.Rule(liquid_energy['positive_small'] & state_of_charge['negative_small'], battery_situation['positive_small'])
    rule35 = ctrl.Rule(liquid_energy['positive_small'] & state_of_charge['negative_big'], battery_situation['positive_small'])

    rule36 = ctrl.Rule(liquid_energy['zero'] & state_of_charge['positive_big'], battery_situation['zero'])
    rule37 = ctrl.Rule(liquid_energy['zero'] & state_of_charge['positive_small'], battery_situation['zero'])
    rule38 = ctrl.Rule(liquid_energy['zero'] & state_of_charge['zero'], battery_situation['zero'])
    rule39 = ctrl.Rule(liquid_energy['zero'] & state_of_charge['negative_small'], battery_situation['zero'])
    rule40 = ctrl.Rule(liquid_energy['zero'] & state_of_charge['negative_big'], battery_situation['zero'])

    rule41 = ctrl.Rule(liquid_energy['negative_small'] & state_of_charge['positive_big'], battery_situation['negative_big'])
    rule42 = ctrl.Rule(liquid_energy['negative_small'] & state_of_charge['positive_small'], battery_situation['negative_small'])
    rule43 = ctrl.Rule(liquid_energy['negative_small'] & state_of_charge['zero'], battery_situation['negative_small'])
    rule44 = ctrl.Rule(liquid_energy['negative_small'] & state_of_charge['negative_small'], battery_situation['zero'])
    rule45 = ctrl.Rule(liquid_energy['negative_small'] & state_of_charge['negative_big'], battery_situation['zero'])

    rule46 = ctrl.Rule(liquid_energy['negative_big'] & state_of_charge['positive_big'], battery_situation['negative_big'])
    rule47 = ctrl.Rule(liquid_energy['negative_big'] & state_of_charge['positive_small'], battery_situation['negative_big'])
    rule48 = ctrl.Rule(liquid_energy['negative_big'] & state_of_charge['zero'], battery_situation['negative_small'])
    rule49 = ctrl.Rule(liquid_energy['negative_big'] & state_of_charge['negative_small'], battery_situation['zero'])
    rule50 = ctrl.Rule(liquid_energy['negative_big'] & state_of_charge['negative_big'], battery_situation['zero'])

    # Rules for the most expensive time interval:
    rule51 = ctrl.Rule(liquid_energy['positive_big'] & state_of_charge['positive_big'], battery_situation['zero'])
    rule52 = ctrl.Rule(liquid_energy['positive_big'] & state_of_charge['positive_small'], battery_situation['positive_small'])
    rule53 = ctrl.Rule(liquid_energy['positive_big'] & state_of_charge['zero'], battery_situation['positive_small'])
    rule54 = ctrl.Rule(liquid_energy['positive_big'] & state_of_charge['negative_small'], battery_situation['positive_big'])
    rule55 = ctrl.Rule(liquid_energy['positive_big'] & state_of_charge['negative_big'], battery_situation['positive_big'])

    rule56 = ctrl.Rule(liquid_energy['positive_small'] & state_of_charge['positive_big'], battery_situation['zero'])
    rule57 = ctrl.Rule(liquid_energy['positive_small'] & state_of_charge['positive_small'], battery_situation['positive_small'])
    rule58 = ctrl.Rule(liquid_energy['positive_small'] & state_of_charge['zero'], battery_situation['positive_small'])
    rule59 = ctrl.Rule(liquid_energy['positive_small'] & state_of_charge['negative_small'], battery_situation['positive_small'])
    rule60 = ctrl.Rule(liquid_energy['positive_small'] & state_of_charge['negative_big'], battery_situation['positive_small'])

    rule61 = ctrl.Rule(liquid_energy['zero'] & state_of_charge['positive_big'], battery_situation['zero'])
    rule62 = ctrl.Rule(liquid_energy['zero'] & state_of_charge['positive_small'], battery_situation['zero'])
    rule63 = ctrl.Rule(liquid_energy['zero'] & state_of_charge['zero'], battery_situation['zero'])
    rule64 = ctrl.Rule(liquid_energy['zero'] & state_of_charge['negative_small'], battery_situation['zero'])
    rule65 = ctrl.Rule(liquid_energy['zero'] & state_of_charge['negative_big'], battery_situation['zero'])

    rule66 = ctrl.Rule(liquid_energy['negative_small'] & state_of_charge['positive_big'], battery_situation['negative_big'])
    rule67 = ctrl.Rule(liquid_energy['negative_small'] & state_of_charge['positive_small'], battery_situation['negative_big'])
    rule68 = ctrl.Rule(liquid_energy['negative_small'] & state_of_charge['zero'], battery_situation['negative_big'])
    rule69 = ctrl.Rule(liquid_energy['negative_small'] & state_of_charge['negative_small'], battery_situation['zero'])
    rule70 = ctrl.Rule(liquid_energy['negative_small'] & state_of_charge['negative_big'], battery_situation['zero'])

    rule71 = ctrl.Rule(liquid_energy['negative_big'] & state_of_charge['positive_big'], battery_situation['negative_big'])
    rule72 = ctrl.Rule(liquid_energy['negative_big'] & state_of_charge['positive_small'], battery_situation['negative_big'])
    rule73 = ctrl.Rule(liquid_energy['negative_big'] & state_of_charge['zero'], battery_situation['negative_big'])
    rule74 = ctrl.Rule(liquid_energy['negative_big'] & state_of_charge['negative_small'], battery_situation['zero'])
    rule75 = ctrl.Rule(liquid_energy['negative_big'] & state_of_charge['negative_big'], battery_situation['zero'])


    #Cria e simula um controlador nebuloso:
    battery_situation_ctrl_barata = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10,
                                                        rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20,
                                                        rule21, rule22, rule23, rule24, rule25])
    battery_situation_simulador_barata = ctrl.ControlSystemSimulation(battery_situation_ctrl_barata)

    battery_situation_ctrl_intermediaria = ctrl.ControlSystem([rule26, rule27, rule28, rule29, rule30, rule31, rule32, rule33, rule34, rule35,
                                                               rule36, rule37, rule38, rule39, rule40, rule41, rule42, rule43, rule44, rule45,
                                                               rule46, rule47, rule48, rule49, rule50])
    battery_situation_simulador_intermediaria = ctrl.ControlSystemSimulation(battery_situation_ctrl_intermediaria)

    battery_situation_ctrl_cara = ctrl.ControlSystem([rule51, rule52, rule53, rule54, rule55, rule56, rule57, rule58, rule59, rule60,
                                                      rule61, rule62, rule63, rule64, rule65, rule66, rule67, rule68, rule69, rule70,
                                                      rule71, rule72, rule73, rule74, rule75])
    battery_situation_simulador_cara = ctrl.ControlSystemSimulation(battery_situation_ctrl_cara)

    #Entra com valores para as variáveis:
    #battery_situation_simulador.input['liquid_energy'] = 0.1
    #battery_situation_simulador.input['state_of_charge'] = 20
    pasta = "1_res_fuzzy_en0_dataset_artigo_marcos_filipe1.xlsx"
    # excel = pd.read_excel(pasta, sheet_name='res_fuzzy_en0', header=0, engine='openpyxl')
    excel = pd.read_excel(filename)
    
    en = 0
    soc = 0
    list_eb = []

    #Computa o resultado:
    for i in range(len(excel)):
        hour = excel["Hora"][i]
        if (hour>=0 and hour<17.50):
            battery_situation_simulador_barata.input['liquid_energy'] = excel["El_KW"][i]
            battery_situation_simulador_barata.input['state_of_charge'] = soc
            battery_situation_simulador_barata.compute()
            eb = battery_situation_simulador_barata.output['battery_situation']
            if eb is None:
                eb = 0

        elif (hour>=17.50 and hour<18.50):
            battery_situation_simulador_intermediaria.input['liquid_energy'] = excel["El_KW"][i]
            battery_situation_simulador_intermediaria.input['state_of_charge'] = soc
            battery_situation_simulador_intermediaria.compute()
            eb = battery_situation_simulador_intermediaria.output['battery_situation']
            if eb is None:
                eb = 0

        elif (hour>=18.50 and hour<21.50):
            battery_situation_simulador_cara.input['liquid_energy'] = excel["El_KW"][i]
            battery_situation_simulador_cara.input['state_of_charge'] = soc
            battery_situation_simulador_cara.compute()
            eb = battery_situation_simulador_cara.output['battery_situation']
            if eb is None:
                eb = 0

        elif (hour>=21.50 and hour<22.50):
            battery_situation_simulador_intermediaria.input['liquid_energy'] = excel["El_KW"][i]
            battery_situation_simulador_intermediaria.input['state_of_charge'] = soc
            battery_situation_simulador_intermediaria.compute()
            eb = battery_situation_simulador_intermediaria.output['battery_situation']
            if eb is None:
                eb = 0

        elif (hour>=22.50 and hour<24.00):
            battery_situation_simulador_barata.input['liquid_energy'] = excel["El_KW"][i]
            battery_situation_simulador_barata.input['state_of_charge'] = soc
            battery_situation_simulador_barata.compute()
            eb = battery_situation_simulador_barata.output['battery_situation']
            if eb is None:
                eb = 0

        en = en+(eb*5/60)
        soc = 100*en/70
        list_eb.append(eb)

    return list_eb, excel

#     #%%
# textfile = open("file_eb_or.txt", "w")
# for element in list_eb:
#     textfile.write(str(element).upper().replace('.', ',', 1) + "\n")
# textfile.close()
