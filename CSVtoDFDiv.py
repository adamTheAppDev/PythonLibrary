# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#Import modules
from pandas import read_csv
import pandas as pd
import os

#This is a formatting tool for directory management

#Find files to iterate through
CSVfiles = os.listdir('F:\\Users\\UserName\\TemporaryDiv')
#Create iterable
ranger = range(0,len(CSVfiles))
#For all files in folder
for i in ranger:
    try:
        #Open file
        temp = read_csv('F:\\Users\\UserName\\TemporaryDiv\\' +
                         (CSVfiles[i]), sep = ',')
        #Set index
        temp = temp.set_index('Date')
        #Format index
        temp.index = pd.to_datetime(temp.index, format = "%Y/%m/%d") 
        #Delete duplicate columns
        temp = temp.loc[:,~temp.columns.duplicated()]
        #Delete duplicate rows
        temp = temp[~temp.index.duplicated(keep='first')]
        #Create folder if it doesn't exist
        if not os.path.exists('F:\\Users\\UserName\\Database\\' +
                          CSVfiles[i][:-7]):
            os.makedirs('F:\\Users\\UserName\\Database\\' +
                          CSVfiles[i][:-7])
        #Save to pickle
        pd.to_pickle(temp, 'F:\\Users\\UserName\\Database\\' +
                          CSVfiles[i][:-7] + '\\' + CSVfiles[i][:-4])
    except OSError:
        continue
#For all files
for i in ranger:
    try:
        files = pd.read_pickle('F:\\Users\\UserName\\Database\\' +
                         (CSVfiles[i][:-4]))
        #For all columns in file
        for x in files.columns:
            #Change str to num -- This code can be implemented in above for loop to improve performance
            files[x] =  pd.to_numeric(files[x], errors='coerce')
        #Save file to pickle
        pd.to_pickle(files, 'F:\\Users\\UserName\\Database\\' +
                          CSVfiles[i][:-4])
    except OSError:
        continue
        
#this is for testing individual CSVs
#tester = read_csv('F:\\Users\\UserName\\TemporaryCSV\\' +
#                     (df['CSVname'][0]), sep = ',')
#tester = tester.set_index('Date')
#pd.to_pickle(tester, 'F:\\Users\\UserName\\Database\\' + df['CSVname'][0][:-4])
