# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#Entity Creation
#This is an organizational tool, a process that sets up folders
#Modify the structure and contents of the directory hierarchy to be populated by processes
#Refer to this program when writing/saving data from new apps

#Import modules
import os 

#Assign directory location - unique to localhost
WD = "F:\\Users\\UserName\\FolderName"

#Create the folder from which everything flows.
if not os.path.exists(WD):
    os.makedirs(WD)
    
#Create and edit the primary set of folders; keep it clean
    
#This is where input data is stored
if not os.path.exists(WD + "\\DataSources"):
    os.makedirs(WD + "\\DataSources")
#This is where model output is stored
if not os.path.exists(WD + "\\ModelOutput"):
    os.makedirs(WD + "\\ModelOutput")
#This is where automated/batch files are stored
if not os.path.exists(WD + "\\BatchFiles"):
    os.makedirs(WD + "\\BatchFiles")
#This is where execution/API logs are stored
if not os.path.exists(WD + "\\ExecutionLogs"):
    os.makedirs(WD + "\\ExecutionLogs")    
    
#Create and edit a secondary set of folders within a primary folder; keep it clean

#This is the YahooSource
if not os.path.exists(WD + "\\DataSources\\YahooSource"):
    os.makedirs(WD + "\\DataSources\\YahooSource")
#This is the NASDAQSource
if not os.path.exists(WD + "\\DataSources\\NASDAQSource"):
    os.makedirs(WD + "\\NASDAQSource")
#This is the YahooSource ModelOutput
if not os.path.exists(WD + "\\ModelOutput\\YahooSource"):
    os.makedirs(WD + "\\ModelOutput\\YahooSource")
    
#Create and edit a tertiary set of folders within a secondary folder; keep it clean

#These are YahooSource subfolders
#This is populated by a CSVfetch
if not os.path.exists(WD + "\\DataSources\\YahooSource\\DividendData"):
    os.makedirs(WD + "\\DataSources\\YahooSource\\DividendData")
#This is populated by a CSVfetch
if not os.path.exists(WD + "\\FDL\\DataSources\\YahooSource\\TimeSeriesData"):
    os.makedirs(WD + "\\DataSources\\YahooSource\\TimeSeriesData")
#Concatenate dividend, time series, qualitative, and database modification
if not os.path.exists(WD + "\\DataSources\\YahooSource\\ProcessedData"):
    os.makedirs(WD + "\\DataSources\\YahooSource\\ProcessedData")

#These are NASDAQSource subfolders
#This can be populated by a concatenation and cleaning of NASDAQ data on AMEX NYSE NASDAQ listed stocks
if not os.path.exists(WD + "\\DataSources\\NASDAQSource\\QualitativeData"):
    os.makedirs(WD + "\\DataSources\\NASDAQSource\\QualitativeData")    
#This a ticker list from qualitative data
if not os.path.exists(WD + "\\DataSources\\NASDAQSource\\UniverseLists"):
    os.makedirs(WD + "\\DataSources\\NASDAQSource\\UniverseLists")   
    
#These are frequencies for ModelOutput from YahooSource
if not os.path.exists(WD + "\\ModelOutput\\YahooSource\\DAY"):
    os.makedirs(WD + "\\ModelOutput\\YahooSource\\DAY")
    
#Create and edit a quarternary set of folders within a tertiary folder; keep it clean
if not os.path.exists(WD + "\\DataSources\\YahooSource\\ProcessedData\\DAY"):
    os.makedirs(WD + "\\DataSources\\YahooSource\\ProcessedData\DAY")
if not os.path.exists(WD + "\\DataSources\\YahooSource\\ProcessedData\\WEK"):
    os.makedirs(WD + "\\DataSources\\YahooSource\\ProcessedData\\WEK")
if not os.path.exists(WD + "\\DataSources\\YahooSource\\ProcessedData\\MON"):
    os.makedirs(WD + "\\DataSources\\YahooSource\\ProcessedData\\MON")
if not os.path.exists(WD + "\\DataSources\\YahooSource\\ProcessedData\\DIV"):
    os.makedirs(WD + "\\DataSources\\YahooSource\\ProcessedData\\DIV")
    
#This holds ByTicker and ByModel folders within frequencies folders for ModelOutput from YahooSource
if not os.path.exists(WD + "\\ModelOutput\\YahooSource\\DAY\\DonchianTrend"):
    os.makedirs(WD + "\\ModelOutput\\YahooSource\\DAY\\DonchianTrend")

#Create and edit a 5th set of folders within a quarternary folder; keep it clean
if not os.path.exists(WD + "\\ModelOutput\\YahooSource\\DAY\\DonchianTrend\\ReturnStreams"):
    os.makedirs(WD + "\\ModelOutput\\YahooSource\\DAY\\DonchianTrend\\ReturnStreams")
    
if not os.path.exists(WD + "\\ModelOutput\\YahooSource\\DAY\\DonchianTrend\\ModelOutput"):
    os.makedirs(WD + "\\ModelOutput\\YahooSource\\DAY\\DonchianTrend\\ModelOutput")
