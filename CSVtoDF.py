# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a formatting tool for directory management

#Import modules
from pandas import read_csv
import pandas as pd
import os

#Assign folder with CSVs
CSVfiles = os.listdir('F:\\Users\\AmatVictoriaCuram\\TemporaryCSV')

#Make range from total number of files in folder
ranger = range(0,len(CSVfiles))

#For all files in CSV folder
for i in ranger:
    try:
        #Open files
        temp = read_csv('F:\\Users\\AmatVictoriaCuram\\TemporaryCSV\\' +
                         (CSVfiles[i]), sep = ',')
        #Change index
        temp = temp.set_index('Date')
        #Format index
        temp.index = pd.to_datetime(temp.index, format = "%Y/%m/%d") 
        #Delete duplicate columns
        temp = temp.loc[:,~temp.columns.duplicated()]
        #Delete duplicate index values
        temp = temp[~temp.index.duplicated(keep='first')]
        #If a folder to store pickle does not exist
        if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\Database\\' +
                          CSVfiles[i][:-4]):
            #Make folder
            os.makedirs('F:\\Users\\AmatVictoriaCuram\\Database\\' +
                          CSVfiles[i][:-4])
        #Store pickle
        pd.to_pickle(temp, 'F:\\Users\\AmatVictoriaCuram\\Database\\' +
                          CSVfiles[i][:-4] + '\\' + CSVfiles[i][:-4])
        #Print progress
        print(CSVfiles[i])
    except OSError:
        continue
#Once all files converted to pickles, for all pickles -- this code can be abbreviated by cleaning in above for loop
for i in ranger:
    try:
        #Open pickle
        files = pd.read_pickle('F:\\Users\\AmatVictoriaCuram\\Database\\' +
                        CSVfiles[i][:-4] + '\\' + CSVfiles[i][:-4])
        #Clean values
        for x in files.columns:
            files[x] =  pd.to_numeric(files[x], errors='coerce')
        #Save pickle
        pd.to_pickle(files, 'F:\\Users\\AmatVictoriaCuram\\Database\\' +
                         CSVfiles[i][:-4] + '\\' + CSVfiles[i][:-4])
        #Print progress
        print(CSVfiles[i])
    except OSError:
        continue
        
#this is for testing individual CSVs
#tester = read_csv('F:\\Users\\AmatVictoriaCuram\\TemporaryCSV\\' +
#                     (df['CSVname'][0]), sep = ',')
#tester = tester.set_index('Date')
#pd.to_pickle(tester, 'F:\\Users\\AmatVictoriaCuram\\Database\\' + df['CSVname'][0][:-4])
