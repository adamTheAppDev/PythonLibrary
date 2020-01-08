# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 23:37:21 2017

@author: AmatVictoriaCuramIII
"""

#This is a formatting tool for database management involving SQL

#TempCSV transfer to CSVtoSQL with Access/SQL COLUMN HEADERS
import pandas as pd
import time as t
import webbrowser as web
from pandas import read_csv
from datetime import date
import datetime
import os
import numpy as np
from pandas import read_csv 
#Get list of files in folder
CSVlist = os.listdir('F:\\Users\\AmatVictoriaCuram\\TemporaryCSV\\')
#Make program output destination
if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\CSVtoSQL'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\CSVtoSQL')
#Open and mod each file
for i in CSVlist:
    temp = read_csv('F:\\Users\\AmatVictoriaCuram\\TemporaryCSV\\' +
                         (i), sep = ',')
    temp.insert(1,'Ticker', i[:-4])
    temp.rename(columns={'Date':'StkDate'}, inplace=True)
#save files to new destination
    temp.to_csv('F:\\Users\\AmatVictoriaCuram\\CSVtoSQL\\' + (i), sep=',', 
                    index = False)    

