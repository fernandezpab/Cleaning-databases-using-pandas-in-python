# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 19:11:37 2021

@author: PC
"""

import pandas as pd
import datetime
import re

import requests
       
url = "https://www.indec.gob.ar/ftp/cuadros/economia/sh_emae_mensual_base2004.xls"
r_tot = requests.get(url, allow_redirects=True)

df = pd.read_excel("https://www.indec.gob.ar/ftp/cuadros/economia/sh_emae_mensual_base2004.xls", sheet_name="EMAE n° índice y variaciones", skiprows= 2,
                           header=[0])

df.dropna(axis=0, how='all',inplace=True)
df.dropna(axis=1, how='all',inplace=True)    
df["year"] = pd.to_numeric(df["Período"], errors="coerce").ffill()
df["month"] = df["Período"]
replace_string = {"Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4, "Mayo": 5, "Junio": 6, "Julio": 7, "Agosto": 8, "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12}
df = df.replace({"month": replace_string})
df["month"] = pd.to_numeric(df["month"], errors="coerce")
df = df[df["month"] <= 12]
df["day"] = 1
df["Date"] = pd.to_datetime(df[["year", "month", "day"]])
del df["Período"]
del df["day"]
del df["month"]
del df["year"]

for col in df.columns:
     new_col = re.sub(' +', ' ', col).replace("\n2004=100", "")
     df = df.rename(columns={col: new_col})

df = df[df.columns.drop(list(df.filter(regex='%')))]

df
