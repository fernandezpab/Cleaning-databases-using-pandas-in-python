# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 22:00:03 2021

@author: PC
"""

import pandas as pd
from datetime import datetime
import numpy as np
import re

# In this example we create a loop to take three spreadsheets at the same time

# We create a dictionary to call the sheet from the "read_excel" funcion and a prefix
# to add it so that we can recognize from which sheet is the data

loop = {
    1:{"sheet":'as', "prefix":'Ambos Sexos'},
    2:{"sheet":'h', "prefix":'Hombre'}, 
    3:{"sheet":'m', "prefix":'Mujer'} 
}

# We create the data frame where the final database will be charged

dfFinal = pd.DataFrame()        

# Then we start the loop

for key in loop.keys():     
    df = pd.read_excel("https://www.ine.cl/docs/default-source/ocupacion-y-desocupacion/cuadros-estadisticos/series-de-tiempo-nueva-calibraci%C3%B3n-proyecciones-de-poblaci%C3%B3n-censo-2017/serie-categor%C3%ADa-en-la-ocupaci%C3%B3n.xlsx?sfvrsn=70dc54db_41", skiprows=5, sheet_name=loop[key]["sheet"], header=[0,1])

# First, we add a '-' to separate the multiIndex
    
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.map(' - '.join)

    for col in df.columns:
        new_col = re.sub(' +', ' ', col).replace(" - nota", "").replace(" - Unnamed: 0_level_1", "").replace("- Unnamed: 1_level_1","").replace(" /2","").replace(" /3","").replace(" /4","").replace(" /5","").replace(" /6","")
        df = df.rename(columns={col: new_col})

    df = df.dropna(how = 'all').dropna(how = 'all',axis=1)

    df = df.loc[:,~(df=='a').any()]    
    df = df.loc[:,~(df=='b').any()] 
    df = df.dropna(how='all', subset=df.columns[1:])

    df['Trimestre '] = df['Trimestre '].astype(str)

    df['Trimestre '] = df['Trimestre '].replace(
        {
            "Ene - Mar": "02-01",
            "Feb - Abr": "03-01",
            "Mar - May": "04-01",
            "Abr - Jun": "05-01",
            "May -Jul":  "06-01",
            "Jun - Ago": "07-01",
            "Jul - Sep": "08-01",
            "Ago - Oct": "09-01",
            "Sep - Nov": "10-01",
            "Oct - Dic": "11-01",
            "Nov - Ene": "12-01",
            "Dic - Feb": "01-01",
        })

    df['Año'] = df['Año'].astype(str)

    df['Date'] = df['Año'] + '-' + df['Trimestre ']

    del df['Año']
    del df['Trimestre '] 

# We transform the Date in datetime

    df['Date']=pd.to_datetime(df['Date'])

# We set the Date as an Index  

    df = df.set_index('Date')

# We add the prefix
    
    for col in df.columns:
        df = df.rename(columns={col: loop[key]["prefix"] + ' - ' + col})
    
# Finally, we merge the data in the dataframe called dfFinal 
    
    dfFinal = dfFinal.merge(df, how='outer', left_index=True, right_index=True)

dfFinal
