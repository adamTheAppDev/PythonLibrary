# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a formatting tool for CSV files
#Directory management tool

#Import modules
from pandas import read_csv
import pandas as pd
import os

#Get list of files in folder
CSVlist = os.listdir('F:\\Users\\AmatVictoriaCuram\\CSVtoSQL\\')

#Make large dataframe
DF = pd.DataFrame()

#Open and mod each file
for i in CSVlist:
    temp = read_csv('F:\\Users\\AmatVictoriaCuram\\CSVtoSQL\\' +
                         (i), sep = ',') 
    DF = pd.concat([DF, temp], axis = 0)
    
#Remove duplicate columns
DF = DF.loc[:,~DF.Ticker.duplicated()]

#Write to CSV
DF.to_csv('C:\\Users\\AmatVictoriaCuramIII\\Desktop\\Access\\DF.csv',
                    index=False)
