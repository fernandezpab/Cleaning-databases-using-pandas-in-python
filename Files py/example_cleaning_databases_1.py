# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 22:39:36 2021

@author: PC
"""

import pandas as pd
import numpy as np

# We name the url from the source into an element called url

url = "http://www.ciaracec.com.ar/ciara/descargar/01072021_080000-liquidacion-de-divisas-de-los-industriales-de-oleaginosos-y-exportadores-de-cereales-01-07-2021.xls"

# If the url is no longer available you can find the excel in Databses

# We will clean the data from the sheet called "Datos Mensuales"

df = pd.read_excel(url, sheet_name = "Datos Mensuales", skiprows=3, header=[0,1])

# We see that the data has twice the name Diciembre, for this reason we create an index
# to keep only with the data until the first Diciembre

indiceFinal = df[df[('Unnamed: 0_level_0', 'Total liquidacion del mes de:')] == 'Diciembre'].index[0]

df1 = df.iloc[:(indiceFinal+1),] 

# Then we transpose the data an reset the index

df1 = df1.transpose().reset_index()

# Later on we replace in column level_1 with NaNs where the word unnamed appears

df1.loc[df1["level_1"].astype("str").str.contains('Unnamed'), "level_1"] = np.nan

#Then we fill this nan with the data in column 'level_0'

df1["level_1"] = df1["level_1"].fillna(df1["level_0"])

del df1["level_0"]

new_header = df1.iloc[0] #grab the first row for the header

df1 = df1[1:] #take the data less the header row

df1.columns = new_header #set the header row as the df header

df1 = df1.melt("Total liquidacion del mes de:")

df1 = df1.dropna()
df1 = df1.rename(columns={
    "Total liquidacion del mes de:": "year",
    0: "month"})
replace_string = {"Enero": 1, "Febrero": 2, "Marzo ": 3, "Abril": 4, "Mayo": 5, "Junio": 6, "Julio": 7, "Agosto": 8, "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12}
df1 = df1.replace({"month": replace_string})
df1["month"] = pd.to_numeric(df1["month"], errors="coerce")
df1["day"] = 1
df1["Date"] = pd.to_datetime(df1[["year", "month", "day"]])
del df1["day"]
del df1["month"]
del df1["year"]
df1["country"] = "Argentina"
df1 = df1.set_index("Date")
df1 = df1.rename(columns={
    "value": "Liquidacion divisas"})

df1 = df1.sort_index()

