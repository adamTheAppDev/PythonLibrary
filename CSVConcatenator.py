# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 00:35:14 2017

@author: AmatVictoriaCuramIII
"""

#This is a formatting tool for CSV files
#Database management tool

from pandas import read_csv
import pandas as pd
import os
#Get list of files in folder
CSVlist = os.listdir('F:\\Users\\AmatVictoriaCuram\\CSVtoSQL\\')
#Make large dataframe
DailyDose = pd.DataFrame()
#Open and mod each file
for i in CSVlist:
    temp = read_csv('F:\\Users\\AmatVictoriaCuram\\CSVtoSQL\\' +
                         (i), sep = ',') 
    DailyDose = pd.concat([DailyDose, temp], axis = 0)
DailyDose = DailyDose.loc[:,~DailyDose.Ticker.duplicated()]
DailyDose.to_csv('C:\\Users\\AmatVictoriaCuramIII\\Desktop\\Access\\DailyDose.csv',
                    index=False)
