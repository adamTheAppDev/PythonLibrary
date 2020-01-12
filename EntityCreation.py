# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 16:39:32 2019

@author: AmatVictoriaCuramIII
"""

#Entity Creation
#This is an organizational tool, an I/O process that sets up folders
#Modify the structure and contents of the directory hierarchy to be populated by processes
#Refer to this program when writing/saving data from new apps

#Imports
import os 

#Working Directory, standard destination can be used to reduce redundance and standardize for other users

WD = "C:\\Jared\\Users\\Desktop\\JDL"

#Create the folder from which everything flows.
if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\FDL'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\FDL')
    
#Create and edit the primary set of folders; keep it clean
    
#This is where input data is stored
if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\FDL\\DataSources'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\FDL\\DataSources')
#This is where model output is stored
if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\FDL\\ModelOutput'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\FDL\\ModelOutput')
#This is where automated/batch files are stored
if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\FDL\\BatchFiles'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\FDL\\BatchFiles')
#This is where execution/API logs are stored
if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\FDL\\ExecutionLogs'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\FDL\\ExecutionLogs')    
    
#Create and edit a secondary set of folders within a primary folder; keep it clean

#This is the YahooSource
if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\FDL\\DataSources\\YahooSource'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\FDL\\DataSources\\YahooSource')
#This is the NASDAQSource
if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\FDL\\DataSources\\NASDAQSource'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\FDL\\DataSources\\NASDAQSource')
#This is the YahooSource ModelOutput
if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\FDL\\ModelOutput\\YahooSource'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\FDL\\ModelOutput\\YahooSource')
    
#Create and edit a tertiary set of folders within a secondary folder; keep it clean

#These are YahooSource subfolders
#This is populated by a CSVfetch
if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\FDL\\DataSources\\YahooSource\\DividendData'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\FDL\\DataSources\\YahooSource\\DividendData')
#This is populated by a CSVfetch
if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\FDL\\DataSources\\YahooSource\\TimeSeriesData'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\FDL\\DataSources\\YahooSource\\TimeSeriesData')
#Concatenate dividend, time series, qualitative, and database modification
if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\FDL\\DataSources\\YahooSource\\ProcessedData'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\FDL\\DataSources\\YahooSource\\ProcessedData')

#These are NASDAQSource subfolders
#This can be populated by a concatenation and cleaning of NASDAQ data on AMEX NYSE NASDAQ listed stocks
if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\FDL\\DataSources\\NASDAQSource\\QualitativeData'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\FDL\\DataSources\\NASDAQSource\\QualitativeData')    
#This a ticker list from qualitative data
if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\FDL\\DataSources\\NASDAQSource\\UniverseLists'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\FDL\\DataSources\\NASDAQSource\\UniverseLists')   
    
#These are frequencies for ModelOutput from YahooSource
if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\FDL\\ModelOutput\\YahooSource\\DAY'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\FDL\\ModelOutput\\YahooSource\\DAY')
    
#Create and edit a quarternary set of folders within a tertiary folder; keep it clean
if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\FDL\\DataSources\\YahooSource\\ProcessedData\\DAY'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\FDL\\DataSources\\YahooSource\\ProcessedData\DAY')
if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\FDL\\DataSources\\YahooSource\\ProcessedData\\WEK'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\FDL\\DataSources\\YahooSource\\ProcessedData\\WEK')
if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\FDL\\DataSources\\YahooSource\\ProcessedData\\MON'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\FDL\\DataSources\\YahooSource\\ProcessedData\\MON')
if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\FDL\\DataSources\\YahooSource\\ProcessedData\\DIV'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\FDL\\DataSources\\YahooSource\\ProcessedData\\DIV')
    
#This holds ByTicker and ByModel folders within frequencies folders for ModelOutput from YahooSource
if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\FDL\\ModelOutput\\YahooSource\\DAY\\DonchianTrend'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\FDL\\ModelOutput\\YahooSource\\DAY\\DonchianTrend')

#Create and edit a 5th set of folders within a quarternary folder; keep it clean
if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\FDL\\ModelOutput\\YahooSource\\DAY\\DonchianTrend\\ReturnStreams'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\FDL\\ModelOutput\\YahooSource\\DAY\\DonchianTrend\\ReturnStreams')
    
if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\FDL\\ModelOutput\\YahooSource\\DAY\\DonchianTrend\\ModelOutput'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\FDL\\ModelOutput\\YahooSource\\DAY\\DonchianTrend\\ModelOutput')



