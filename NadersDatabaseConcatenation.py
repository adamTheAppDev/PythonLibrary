# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 20:59:57 2018

@author: AmatVictoriaCuramIII
"""

#Database concatenation into global table
#Import
import os
import pandas as pd
#Make a folder and put a pickle in there
#If there is no Table Folder,
if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\NadersTable'):
    #Make table folder.
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\NadersTable')
#If there is no pickle in the folder, 
if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\NadersTable\\NadersTable'):
    #Make the blank pickle.    
    NadersTable = pd.DataFrame()
    #Save the blank pickle to populate later
    pd.to_pickle(NadersTable,'F:\\Users\\AmatVictoriaCuram\\NadersTable\\NadersTable')
#Find all folders that will be iterated over
CurrentPickles = os.listdir('F:\\Users\\AmatVictoriaCuram\\NadersData')
#Open pickle for the global table, 
CascadeTable = pd.DataFrame()
#For every item in database
CascadeList = list(range(0,len(CurrentPickles),50))
CascadeList = CascadeList + [(len(CurrentPickles))]
#CascadeFolder
if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\CascadeFolder'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\CascadeFolder')

try:
    for i in range(len(CascadeList)):
        Cascadei = pd.DataFrame()
        print('Made new cascade file #' + str(i))
        for ii in CurrentPickles[CascadeList[i]:CascadeList[i+1]]:
            #Open the pickle to be added to global table
            temp = pd.read_pickle('F:\\Users\\AmatVictoriaCuram\\NadersData\\' + ii + '\\' + ii)
            #Since we are now having multiple dates in same table, change index to ticker+date
            temp = temp.set_index('TickerDate')
            #Concatenate data below existing data
            Cascadei = pd.concat([Cascadei,temp])
            print(ii+' Appended to cascade')
#            print([CascadeList[i],CascadeList[i+1]])  
        pd.to_pickle(Cascadei, 'F:\\Users\\AmatVictoriaCuram\\CascadeFolder\\Cascade' + str(i))
except IndexError:
    pass

NadersTable = pd.read_pickle('F:\\Users\\AmatVictoriaCuram\\NadersTable\\NadersTable')
CurrentCascade = os.listdir('F:\\Users\\AmatVictoriaCuram\\CascadeFolder')
for i in CurrentCascade:
    #Open the pickle to be added to global table
    temp = pd.read_pickle('F:\\Users\\AmatVictoriaCuram\\CascadeFolder\\' + i)
    #Since we are now having multiple dates in same table, change index to ticker+date
#    temp = temp.set_index('TickerDate')
    #Concatenate data below existing data
    NadersTable = pd.concat([NadersTable,temp])
    print(i)
#Save the global table
print('Saving pickle...')
pd.to_pickle(NadersTable, 'F:\\Users\\AmatVictoriaCuram\\NadersTable\\NadersTable')
print('Saving csv...')
NadersTable.to_csv('F:\\Users\\AmatVictoriaCuram\\NadersTable\\NadersTable.csv', index = True)