import pandas as pd
from matplotlib import pyplot as plt
import datetime as datetime
import numpy as np
import json
import os
from statistics import mean, median
import requests
import datetime, pytz
from sklearn.preprocessing import MinMaxScaler

# ESTA FUNÇÃO TRANSFORMA UM DATAFRAME NO FORMATO ADEQUADO PARA SER INPUT DA REDE NEURAL DE INTERPOLAÇÃO 
# O RESULTADO DISSO É SALVO EM UM ARQUIVO .NPY
def transform_and_save_to_npy(dataframe, filename):
    
    """
    dataframe: é o dataframe a ser ajustado e transformado em um array numpy
    filename: é o nome do arquivo que será escrito
    """
    
    df = dataframe.copy()

    # TRANSFORMA TODOS OS VALORES PARA NUMEROS ENTRE 0 E 1
    scaler = MinMaxScaler()
    df['P'] = scaler.fit_transform(np.array(df['P']).reshape(-1, 1))
    
    # TRANSFORMA NO FORMATO ADEQUADO O DATAFRAME PARA SER ENTRADA DA SRGAN
    lista_dates = df['date'].unique().tolist()
    
    dic = {}

    for d in lista_dates:
        dic[d] = df.loc[df['date'] == d]['P'].tolist()

    df_dates = pd.DataFrame(dic)
    
    
    # O DATAFRAME NO FORMATO ADEQUADO É TRANSFORMADO EM UM ARRAY NUMPY
    data_array = df_dates.transpose().to_numpy()
   
    
    print(data_array[0])
    print(data_array.shape)
    
    # A PASTA SRGAN_power_data_generation-main/ CONTÉM TODO O CÓDIGO DA REDE NEURAL
    # A PASTA data/ CONTÉM OS DADOS QUE SERÃO INTERPOLADOS
    np.save("SRGAN_power_data_generation-main/data/"+ filename[:-5] + '_test_pv_3600', data_array)

    # O SCALER É RETORNADO PARA SER UTLIZADO NOS DADOS INTERPOLADOS DEPOIS
    return scaler




# A PARTIR DO RESULTADO DA INTERPOLACAO (QUE É UM ARRAY NUMPY), ESTA FUNÇÃO CONSTROI O DATAFRAME
def load_result(filename, scaler, dataframe):
    
    """
    dataframe: é o dataframe original, sem interpolação. Ele é utilizado para construir o novo dataframe com informações das datas
    filename: é o nome do arquivo que contém o array resultante da interpolação
    scaler: é o scaler retornado na função anterior. Serve para ajustar o range do array resultante da interpolação
    """
    df = dataframe.copy()
    dates_list = df['date'].unique().tolist()
    
    # LISTA COM TODOS DATETIMES COM DIFERENÇA DE 5 MINUTOS ENTRE ELES, SERVE PARA MONTAR O DATAFRAME RESULTANTE
    # POIS O OUTPUT DA REDE NEURAL NÃO TEM INFORMAÇÃO DE DATAS
    datetime_list = []

    delta = datetime.timedelta(minutes=5)
    for d in dates_list:
        datetime_atual = datetime.datetime(year= d.year, month= d.month, day= d.day)
        while (datetime_atual.month == d.month and datetime_atual.day == d.day):
            datetime_list.append(datetime_atual)
            datetime_atual = datetime_atual + delta
    
    
    # CARREGA O ARQUIVO COM O OUTPUT DA REDE NEURAL
    result = np.load(filename)
    
    # AJUSTA O FORMATO DO ARRAY
    result = np.reshape(result, df.shape[0]*12)
    
    # NOVO DATAFRAME É CONSTRUÍDO COM AS COLUNAS DATETIME E PRODUÇÃO
    new_df = pd.DataFrame(data = {'datetime': datetime_list, 'P': result})
    
    # O RANGE DO OUTPUT DA REDE É DE 0-1, PORTANTO É NECESSÁRIO AJUSTAR DE VOLTA PARA O RANGE ORIGINAL
    new_df['P'] = scaler.inverse_transform(np.array(new_df['P']).reshape(-1, 1))
    
    return new_df
 
    
    
# OS ARQUIVOS NA PASTA pvgis_files NÃO ESTÃO COM OS HORÁRIOS LOCAIS DAS CIDADES AOS QUAIS SE REFEREM
# ESTA FUNÇÃO AJUSTA O TIMEZONE
def ajuste_datetime(df, diferenca_horas):
    
    df['datetime'] = pd.to_datetime(df['time'], format='%Y%m%d:%H%M')
    
    if diferenca_horas == 0:
        return df
    
    delta = datetime.timedelta(hours = diferenca_horas)
    df['datetime'] = df['datetime'] + delta

    
    # COM O AJUSTE DO FUSO HORARIO, O ANO PODE NÃO ESTAR MAIS COMPLETO,
    # POR EXEMPLO, AS PRIMEIRAS HORAS DO ANO DE 2013 PODEM TER SE TORNADO AS ULTIMAS HORAS DO ANO DE 2012
    # O CODIGO ABAIXO REMOVE E ADICIONA ALGUMAS LINHAS NO DATAFRAME PARA QUE ELE CONTENHA UM ANO COMPLETO
    if diferenca_horas < 0:

        df = df.iloc[abs(diferenca_horas):]

    else:

        df = df.iloc[:-diferenca_horas]

    df.reset_index(drop=True, inplace=True)

    if diferenca_horas < 0:
        for i in range(abs(diferenca_horas)):
            df.loc[len(df)] = {'time': '0', 'P': 0, 'datetime': df.datetime.iloc[-1] + datetime.timedelta(hours=1)}

    else:
        for i in range(diferenca_horas):
            new_row = pd.DataFrame([{'time': '0', 'P': 0, 'datetime': df.datetime.iloc[0] - datetime.timedelta(hours=1)}])
            df = pd.concat([new_row, df]).reset_index(drop = True)
            
    return df

