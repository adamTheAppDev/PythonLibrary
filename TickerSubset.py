# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a database scanning/query tool
#This lists all stock tickers that pass the scan

#Import modules
from DatabaseGrabber import DatabaseGrabber
import pandas as pd

#Iteration tracking
counter = 1

#Read in tickers to scan
#port = os.listdir('F:\\Users\\AmatVictoriaCuram\\Database')
#Manually input tickers to scan
port = ['ABIO', 'ACST', 'AEZS', 'AGRX', 'AIRI', 'AKER', 'AKTX', 'AMCN', 'AMDA', 'AMRS', 'AMTX', 'ANTH', 'ANY', 'APDN', 
        'APHB', 'AQXP', 'ARDM', 'ARDX', 'ARGS', 'AST', 'ATOS', 'BAS', 'BCEI', 'BIOC', 'BIS', 'BSPM', 'BST', 'BSTG', 'BXE', 
        'CAPR', 'CBIO', 'CCCL', 'CCCR', 'CCIH', 'CDTI', 'CEI', 'CGIX', 'CLBS', 'CLRB', 'CPHI', 'CPST', 'CRMD', 'CSLT', 'CTIC', 
        'CTRV', 'CVEO', 'CXRX', 'CYCC', 'CYTX', 'DCIX', 'DFBG', 'DRIO', 'DRYS', 'ECR', 'EGLE', 'EGLT', 'EIGR', 'EKSO', 'EPE', 
        'ERI', 'ESEA', 'ESES', 'ESNC', 'EVEP', 'EVOK', 'FCSC', 'FHB', 'FIV', 'FNCX', 'FNJN', 'FSNN', 'FTD', 'GENE', 'GEVO', 
        'GLBS', 'GNCA', 'GPRO', 'GRAM', 'GSAT', 'HK', 'HLG', 'HMNY', 'HTBX', 'IGC', 'IMMY', 'IMUC', 'INVT', 'IPDN', 'IPWR', 
        'IZEA', 'JASN', 'JMEI', 'JONE', 'KODK', 'LEDS', 'LEJU', 'LITB', 'LLEX', 'LODE', 'LPCN', 'MACK', 'MARA', 'MATN', 'MBII', 
        'MBVX', 'MCEP', 'MEIP', 'MNGA', 'MOMO', 'MPO', 'MYOS', 'NAKD', 'NAO', 'NEON', 'NEOS', 'NLST', 'NRE', 'NSPR', 'NTB', 
        'NURO', 'NVIV', 'NWBO', 'NXTD', 'OCLR', 'OGEN', 'OHGI', 'OMED', 'ONCS', 'ONTX', 'OPHC', 'OPHT', 'OPTT', 'ORIG', 'OVAS', 
        'PED', 'PEIX', 'PGLC', 'PLG', 'PSTI', 'PULM', 'RBS', 'RGLS', 'RGSE', 'RIBT', 'RMGN', 'ROSG', 'RUBI', 'RXII', 'SAEX', 
        'SALT', 'SBLK', 'SCON', 'SCYX', 'SGOC', 'SHIP', 'SHOS', 'SNSS', 'SQQQ', 'SXE', 'SYN', 'TBK', 'TCS', 'TEAR', 'TGTX', 
        'TNDM', 'TNXP', 'TOPS', 'TROV', 'TRVN', 'TVIX', 'TWER', 'TWLO', 'USLV', 'UUUU', 'UVXY', 'VIIX', 'VIVE', 'VJET', 'VRML', 
        'VSAR', 'VTGN', 'VXX', 'WHLR', 'WMLP', 'XGTI', 'XPLR', 'XTNT', 'YGE']

#Empty list
refinedportfolio = []
#Confirm symbols
#print(symbols)

#For all tickers to scan
for s in port:
    try:
        #Iteration tracking
        print(counter)
        counter = counter + 1
        #Request data
        q = DatabaseGrabber(s)    
        #If true
        if q['AverageRollingVolume'][-1] > 5000000:
            #if float(SCoeffVar(q)) < -5:
            if q['Age'][-1] > 1000:
                        #if float(SRelStrInd(q)) < 30:
                            #if float(SCommodityChannelIndex(q)) < -80:
                #Insert another if or do commands
                #Confirmation
                print(s)
                #Add to list
                refinedportfolio.append(s)
                            #else:
                                #continue
                        #else:
                            #continue
                    #else:
                        #continue
                #else:
                    #continue
            else:
                continue
        else:
            continue

    except OSError:
        pass

#List refined portfolio
print(refinedportfolio)
#Save tickersubset to folder..
#pd.to_pickle(refinedportfolio, 'C:\\Users\\Username\\Directory\\tickersubset')
