# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 15:53:34 2018

@author: AmatVictoriaCuramIII
"""

#This will merge the qualitative data with the quantative data already in database
#Import-ant
from pandas import read_csv
import pandas as pd
import os

#Load the CSV
QualitativeData = read_csv('C:\\Users\\AmatVictoriaCuramIII\\Desktop\\Python\\PretrimQualitativeData.csv', sep = ',')
QualitativeDataTickers = list(QualitativeData['Symbol'])
#See what time series need qualitative data
ExistingPickles = os.listdir('F:\\Users\\AmatVictoriaCuram\\Database')

#A gorgeous list comprehension that delivers all tickers in QualitativeData 
#that have a corresponding time series in existing library
CommonList = [x for x in ExistingPickles if x in QualitativeDataTickers]

#for every issue in common, assign each individual qualitative data value as vector
for i in CommonList:
    try:
#        Access Qualitative Data row and pull out data to add to pickle
        QualitativeDataRow = QualitativeData[QualitativeData['Symbol'] == i]
        Symbol = QualitativeDataRow.iloc[0][0]
        SymbolColumnID = 'IsTicker' + Symbol
        Name = QualitativeDataRow.iloc[0][1]
        NameColumnID = 'IsName' + Name
        LastSale = QualitativeDataRow.iloc[0][2]
        MarketCap = QualitativeDataRow.iloc[0][3]
        ADRTSO = QualitativeDataRow.iloc[0][4]
        ADRTSOColumnID = 'IsADRTSO' + ADRTSO
        IPOyear = QualitativeDataRow.iloc[0][5]
        Sector = QualitativeDataRow.iloc[0][6]
        SectorColumnID = 'IsSector' + Sector
        Industry = QualitativeDataRow.iloc[0][7]
        IndustryColumnID = 'IsIndustry' + Industry
        SummaryQuote = QualitativeDataRow.iloc[0][8]
        SummaryQuoteColumnID = 'IsSummaryQuote' + SummaryQuote
#        #Access existing pickles and insert data
        temp = pd.read_pickle('F:\\Users\\AmatVictoriaCuram\\DataBase\\' + i + '\\' + i)
        temp[SymbolColumnID] = 1
        temp[NameColumnID] = 1
        temp['LastSale'] = LastSale
        temp['GivenMarketCap'] = MarketCap
        temp[ADRTSOColumnID] = 1
        temp['IPOyear'] = IPOyear
        temp[SectorColumnID] = 1
        temp[IndustryColumnID] = 1
        temp[SummaryQuoteColumnID] = 1
#                #drop column function
#        temp = temp.drop(['Column','List'], axis = 1) #drop column function
        temp = temp[~temp.index.duplicated(keep='first')]
        pd.to_pickle(temp, 'F:\\Users\\AmatVictoriaCuram\\Database\\' + i + '\\' + i)
        print(i)
    except OSError:
        continue
    except ValueError:
        continue