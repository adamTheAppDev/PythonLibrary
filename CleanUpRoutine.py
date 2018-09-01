# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 00:32:47 2017

@author: AmatVictoriaCuramIII
"""
import os
#Clean up routine

#Clean up TemporaryCSV        
tempCSV = 'F:\\Users\\AmatVictoriaCuram\\TemporaryCSV\\'
fileList1 = os.listdir(tempCSV)
for f in fileList1:
    os.remove(tempCSV + "\\" + f)   
    
tempCSV1 = 'F:\\Users\\AmatVictoriaCuram\\CSVtoSQL\\'
fileList2 = os.listdir(tempCSV1)
for d in fileList2:
    os.remove(tempCSV1 + "\\" + d)  
    