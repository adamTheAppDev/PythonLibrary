# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a directory management tool for use in batch file..

#Import modules
import os

#Select directory        
tempCSV = 'F:\\Users\\AmatVictoriaCuram\\TemporaryCSV\\'

#List all files in directory
fileList1 = os.listdir(tempCSV)

#For all files in list
for f in fileList1:
    #Remove from directory
    os.remove(tempCSV + "\\" + f)
    
#Select directory
tempCSV1 = 'F:\\Users\\AmatVictoriaCuram\\CSVtoSQL\\'
#List all files in directory
fileList2 = os.listdir(tempCSV1)

#For all files in list
for d in fileList2:
    #Remove from directory
    os.remove(tempCSV1 + "\\" + d)  
