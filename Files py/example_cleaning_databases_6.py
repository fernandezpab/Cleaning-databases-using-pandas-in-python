# -*- coding: utf-8 -*-
"""
Created on Sat Jul 31 23:11:46 2021

@author: PC
"""

import pandas as pd
from datetime import datetime
import requests
import numpy as np
import re

sheets = ['10','11','12','13','14','15','16']
skiprows = [6,5,6,6,6,6]

worksheets = {
    10: {
        "skiprows": 6,
        "prefix": 'IPC sin alimentos'
    }, 
    
    11: {
        "skiprows": 5,
        "prefix": 'IPC de energéticos'
    }, 
    12: {
        "skiprows": 6,
        "prefix": 'IPC total menos energéticos y alimentos'
    }, 
    13: {
        "skiprows": 6,
        "prefix": 'IPC de servicios'
    }, 
    14: {
        "skiprows": 6,
        "prefix": 'IPC de bienes durables'
    }, 
    15: {
        "skiprows": 6,
        "prefix": 'IPC de bienes semi-durables'
    }, 
    16: {
        "skiprows": 6,
        "prefix": 'IPC de bienes no durables'
    }
    
}    

url = "https://www.dane.gov.co/files/investigaciones/boletines/ipc/anexo_ipc_may21.xlsx"
r = requests.get(url, allow_redirects=False, verify=False)

dfFinal = pd.DataFrame()

for key in worksheets.keys():

    df = pd.read_excel(r.content, skiprows=worksheets[key]["skiprows"], sheet_name=str(key),header=[0,1])
    df = df.drop(columns=df.columns[6:]) 
    df = df.dropna(how='all').dropna(how='all', subset= df.columns[1:])

    if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.map(' - '.join)

    for col in df.columns:
        new_col = re.sub(' +', ' ', col).replace(" - Unnamed: 0_level_1", "").replace("- Unnamed: 1_level_1","").replace(" - Unnamed: 2_level_1","")
        df = df.rename(columns={col: new_col})
        
    df['Mes '] = df['Mes '].replace(
        {
        "Enero": "01-01",
        "Febrero": "02-01",
        "Marzo": "03-01",
        "Abril": "04-01",
        "Mayo": "05-01",
        "Mayo ": "05-01",
        "Junio": "06-01",
        "Julio": "07-01",
        "Agosto": "08-01",
        "Septiembre": "09-01",
        "Octubre": "10-01",
        "Noviembre": "11-01",
        "Diciembre": "12-01",

        })
   
    df['Año'] = df['Año'].astype(str).apply(lambda x: x.replace('.0', ''))
    df['Date'] = df['Año'] + ' - ' + df['Mes ']
    del df['Año']
    del df['Mes '] 

    df['Date']=pd.to_datetime(df['Date'])
    df = df.set_index('Date')

    for col in df.columns:
        df = df.rename(columns={col: worksheets[key]["prefix"] + ' - ' + col})

    dfFinal = dfFinal.merge(df, how='outer', left_index=True, right_index=True)

dfFinal['country'] = 'Colombia'
