# -*- coding: utf-8 -*-
"""
Created on Sun Jul 25 12:26:34 2021

@author: PC
"""

import requests
import pandas as pd
from zipfile import ZipFile

local_path = "your_local_path"

def get_data(url, ZipFilename, CSVfilename):    
    r = requests.get(url)
    open(ZipFilename, "wb").write(r.content)
    with ZipFile(ZipFilename, 'r') as zipObj:
        zipObj.extract(CSVfilename, local_path)
    return True

url = 'https://www.bruegel.org/wp-content/uploads/2021/06/REER_database_ver14Jun2021.zip'
ZipFilename = local_path + 'REER_database_ver14Jun2021.zip'
CSVfilename = 'REER_database_ver14Jun2021.xls'
get_data(url, ZipFilename, CSVfilename)

df = pd.read_excel(local_path + '/REER_database_ver14Jun2021.xls', sheet_name="REER_MONTHLY_143")
df = df.rename(columns={df.columns[0]: "Date"})
df = df.melt("Date")
df["country"] = df["variable"].str.split("_").str[2]
df["variable"] = df["variable"].str.split("_").str[0] + "_" + df["variable"].str.split("_").str[1]

countries = {"AF":"Afghanistan", "AL":"Albania", "DZ":"Algeria", "AO":"Angola", "AG":"Antigua and Barbuda", "AR":"Argentina", "AM":"Armenia", "AU":"Australia", "AT":"Austria", "AZ":"Azerbaijan", "BS":"Bahamas, The", "BH":"Bahrain", "BD":"Bangladesh", "BB":"Barbados", "BY":"Belarus", "BE":"Belgium", "BZ":"Belize", "BJ":"Benin", "BT":"Bhutan", "BO":"Bolivia", "BA":"Bosnia and Herzegovina", "BW":"Botswana", "BR":"Brazil", "BN":"Brunei", "BG":"Bulgaria", "BF":"Burkina Faso", "BI":"Burundi", "KH":"Cambodia", "CM":"Cameroon", "CA":"Canada", "CV":"Cape Verde", "CF":"Central African Republic", "TD":"Chad", "CL":"Chile", "CN":"China, Mainland", "CO":"Colombia", "KM":"Comoros", "CD":"Congo, Dem. Rep.", "CG":"Congo, Rep.", "CR":"Costa Rica", "CI":"Côte d'Ivoire", "HR":"Croatia", "CY":"Cyprus", "CZ":"Czech Republic", "DK":"Denmark", "DJ":"Djibouti", "DM":"Dominica", "DO":"Dominican Republic", "EC":"Ecuador", "EG":"Egypt, Arab Rep.", "SV":"El Salvador", "GQ":"Equatorial Guinea", "ER":"Eritrea", "EE":"Estonia", "ET":"Ethiopia", "FJ":"Fiji", "FI":"Finland", "FR":"France", "GA":"Gabon", "GM":"Gambia, The", "GE":"Georgia", "DE":"Germany", "GH":"Ghana", "GR":"Greece", "GD":"Grenada", "GT":"Guatemala", "GN":"Guinea", "GW":"Guinea-Bissau", "GY":"Guyana", "HT":"Haiti", "HN":"Honduras", "HK":"Hong Kong, China", "HU":"Hungary", "IS":"Iceland", "IN":"India", "ID":"Indonesia", "IR":"Iran, Islamic Rep.", "IQ":"Iraq", "IE":"Ireland", "IL":"Israel", "IT":"Italy", "JM":"Jamaica", "JP":"Japan", "JO":"Jordan", "KZ":"Kazakhstan", "KE":"Kenya", "KI":"Kiribati", "KR":"Korea, Rep.", "KW":"Kuwait", "KG":"Kyrgyz Republic", "LA":"Lao PDR", "LV":"Latvia", "LB":"Lebanon", "LS":"Lesotho", "LR":"Liberia", "LY":"Libya", "LT":"Lithuania", "LU":"Luxembourg", "MK":"Macedonia, FYR", "MG":"Madagascar", "MW":"Malawi", "MY":"Malaysia", "MV":"Maldives", "ML":"Mali", "MT":"Malta", "MR":"Mauritania", "MU":"Mauritius", "MX":"Mexico", "MD":"Moldova", "MN":"Mongolia", "MA":"Morocco", "MZ":"Mozambique", "MM":"Myanmar", "NA":"Namibia", "NP":"Nepal", "NL":"Netherlands", "AN":"Netherlands Antilles (Curaçao)", "NZ":"New Zealand", "NI":"Nicaragua", "NE":"Niger", "NG":"Nigeria", "NO":"Norway", "OM":"Oman", "PK":"Pakistan", "PA":"Panama", "PG":"Papua New Guinea", "PY":"Paraguay", "PE":"Peru", "PH":"Philippines", "PL":"Poland", "PT":"Portugal", "QA":"Qatar", "RO":"Romania", "RU":"Russian Federation", "RW":"Rwanda", "WS":"Samoa", "ST":"São Tomé and Principe", "SA":"Saudi Arabia", "SN":"Senegal", "SQ":"Serbia", "SC":"Seychelles", "SL":"Sierra Leone", "SG":"Singapore", "SK":"Slovak Republic", "SI":"Slovenia", "SB":"Solomon Islands", "ZA":"South Africa", "ES":"Spain", "LK":"Sri Lanka", "KN":"St. Kitts and Nevis", "LC":"St. Lucia", "VC":"St. Vincent and the Grenadines", "SD":"Sudan", "SR":"Suriname", "SZ":"Swaziland", "SE":"Sweden", "CH":"Switzerland", "SY":"Syrian Arab Republic", "TW":"Taiwan", "TJ":"Tajikistan", "TZ":"Tanzania", "TH":"Thailand", "TG":"Togo", "TO":"Tonga", "TT":"Trinidad and Tobago", "TN":"Tunisia", "TR":"Turkey", "TM":"Turkmenistan", "UG":"Uganda", "UA":"Ukraine", "AE":"United Arab Emirates", "GB":"United Kingdom", "US":"United States", "UY":"Uruguay", "UZ":"Uzbekistan", "VU":"Vanuatu", "VE":"Venezuela, RB", "VN":"Vietnam", "YE":"Yemen, Rep.", "ZM":"Zambia", "EA12":"Euro area 12 (external)", }

for country in countries:
   df["country"]  = df["country"].replace(country, countries[country])

df["Date"] = pd.to_datetime(df["Date"], format="%YM%m")


