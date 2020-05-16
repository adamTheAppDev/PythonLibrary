# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a database query tool
#This lists all stock tickers that pass the scan

#Import modules
from YahooSourceDailyGrabber import YahooSourceDailyGrabber
import pandas as pd

#Empty data structures
Counter = 0
Empty = []
Empty2 = []

#Read in ticker
Universe = os.listdir('Z:\\Users\\Username\\DirectoryLocation\\DataSources\\YahooSource\\ProcessedData\\DAY')
#Manually assign tickers
#Universe = ['ABIO', 'ACST', 'AEZS', 'AGRX', 'AIRI', 'AKER', 'AKTX', 'AMCN', 'AMDA', 'AMRS', 'AMTX', 'ANTH', 'ANY', 
'APDN', 'APHB', 'AQXP', 'ARDM', 'ARDX', 'ARGS', 'AST', 'ATOS', 'BAS', 'BCEI', 'BIOC', 'BIS', 'BSPM', 'BST', 'BSTG', 
'BXE', 'CAPR', 'CBIO', 'CCCL', 'CCCR', 'CCIH', 'CDTI', 'CEI', 'CGIX', 'CLBS', 'CLRB', 'CPHI', 'CPST', 'CRMD', 'CSLT', 
'CTIC', 'CTRV', 'CVEO', 'CXRX', 'CYCC', 'CYTX', 'DCIX', 'DFBG', 'DRIO', 'DRYS', 'ECR', 'EGLE', 'EGLT', 'EIGR', 'EKSO', 
'EPE', 'ERI', 'ESEA', 'ESES', 'ESNC', 'EVEP', 'EVOK', 'FCSC', 'FHB', 'FIV', 'FNCX', 'FNJN', 'FSNN', 'FTD', 'GENE', 
'GEVO', 'GLBS', 'GNCA', 'GPRO', 'GRAM', 'GSAT', 'HK', 'HLG', 'HMNY', 'HTBX', 'IGC', 'IMMY', 'IMUC', 'INVT', 'IPDN', 
'IPWR', 'IZEA', 'JASN', 'JMEI', 'JONE', 'KODK', 'LEDS', 'LEJU', 'LITB', 'LLEX', 'LODE', 'LPCN', 'MACK', 'MARA', 'MATN', 
'MBII', 'MBVX', 'MCEP', 'MEIP', 'MNGA', 'MOMO', 'MPO', 'MYOS', 'NAKD', 'NAO', 'NEON', 'NEOS', 'NLST', 'NRE', 'NSPR', 'NTB', 
'NURO', 'NVIV', 'NWBO', 'NXTD', 'OCLR', 'OGEN', 'OHGI', 'OMED', 'ONCS', 'ONTX', 'OPHC', 'OPHT', 'OPTT', 'ORIG', 'OVAS', 
'PED', 'PEIX', 'PGLC', 'PLG', 'PSTI', 'PULM', 'RBS', 'RGLS', 'RGSE', 'RIBT', 'RMGN', 'ROSG', 'RUBI', 'RXII', 'SAEX', 'SALT',
'SBLK', 'SCON', 'SCYX', 'SGOC', 'SHIP', 'SHOS', 'SNSS', 'SQQQ', 'SXE', 'SYN', 'TBK', 'TCS', 'TEAR', 'TGTX', 'TNDM', 'TNXP', 
'TOPS', 'TROV', 'TRVN', 'TVIX', 'TWER', 'TWLO', 'USLV', 'UUUU', 'UVXY', 'VIIX', 'VIVE', 'VJET', 'VRML', 'VSAR', 'VTGN', 'VXX', 
'WHLR', 'WMLP', 'XGTI', 'XPLR', 'XTNT', 'YGE']

#Confirm symbols
#print(symbols)

#Trim '.csv'
UniverseList = [s[4:] for s in Universe]
#For all tickers to scan
for Ticker in UniverseList[:]:
    try:
        #Request data
        Asset = YahooSourceDailyGrabber(Ticker)    
        #Scanable metric
        Congestion = Asset['DividendYield'][-1]
        #Add to list
        Empty.append(Ticker)
        Empty2.append(Congestion)
        #List to series
        Emptyseries = pd.Series(Empty)
        #RefinedPortfolio[Counter] = Emptyseries.values
        #Empty[:] = [] 
        print(Counter)
        Counter = Counter + 1        
        
    except OSError:
        pass
#List refined portfolio
RefinedPortfolio = pd.DataFrame(data = Empty2, index=Empty, columns = ['Congestion'])
#Sort by metric
SortedPortfolio = RefinedPortfolio.sort_values(by = ['Congestion'], ascending = True)
#Drop nans
SortedPortfolio = SortedPortfolio.dropna()
