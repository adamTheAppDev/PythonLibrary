# -*- coding: utf-8 -*-
"""
Created on Sun May 21 11:47:12 2017

@author: AmatVictoriaCuramIII
"""

#Separate folder on F drive, NadersData
#The program after this is NadersDatabaseModification
from pandas import read_csv
import pandas as pd
import os

CSVfiles = os.listdir('F:\\Users\\AmatVictoriaCuram\\TemporaryCSV')
ranger = range(0,len(CSVfiles))
for i in ranger:
    try:
        temp = read_csv('F:\\Users\\AmatVictoriaCuram\\TemporaryCSV\\' +
                         (CSVfiles[i]), sep = ',')
        temp = temp.set_index('Date')
        temp.index = pd.to_datetime(temp.index, format = "%Y/%m/%d") 
        temp = temp.loc[:,~temp.columns.duplicated()]
        temp = temp[~temp.index.duplicated(keep='first')]
        for x in temp.columns:
            temp[x] =  pd.to_numeric(temp[x], errors='coerce')
                #Basic Date information
        temp['Age'] = len(temp['Adj Close'])
        temp['Year'] = temp.index.year
        temp['Month'] = temp.index.month
        temp['Day'] = temp.index.day
        temp['DayOfWeek'] = temp.index.dayofweek
        
        #Index column for global table concatenation
        temp['TickerDate'] = CSVfiles[i][:-4] + temp['Year'].astype(str) + temp['Month'].astype(str) + temp['Day'].astype(str)
        
        if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\NadersData\\' +
                          CSVfiles[i][:-4]):
            os.makedirs('F:\\Users\\AmatVictoriaCuram\\NadersData\\' +
                          CSVfiles[i][:-4])
        pd.to_pickle(temp, 'F:\\Users\\AmatVictoriaCuram\\NadersData\\' +
                          CSVfiles[i][:-4] + '\\' + CSVfiles[i][:-4])
        print(CSVfiles[i])
    except OSError:
        continue
#for i in ranger:
#    try:
#        glaze = pd.read_pickle('F:\\Users\\AmatVictoriaCuram\\NadersData\\' +
#                         (CSVfiles[i][:-4]))
#        for x in glaze.columns:
#            glaze[x] =  pd.to_numeric(glaze[x], errors='coerce')
#        pd.to_pickle(glaze, 'F:\\Users\\AmatVictoriaCuram\\NadersData\\' +
#                          CSVfiles[i][:-4])
#        
#        print(CSVfiles[i])
#    except OSError:
#        continue
#this is for testing individual CSVs
#tester = read_csv('F:\\Users\\AmatVictoriaCuram\\TemporaryCSV\\' +
#                     (df['CSVname'][0]), sep = ',')
#tester = tester.set_index('Date')
#pd.to_pickle(tester, 'F:\\Users\\AmatVictoriaCuram\\Database\\' + df['CSVname'][0][:-4])