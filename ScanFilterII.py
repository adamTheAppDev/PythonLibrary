# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 23:29:44 2017

@author: AmatVictoriaCuramIII
"""

#This is a database scanning/query tool
#This lists all stock tickers that pass the scan

#Get modules
from SAge import SAge
from SAverageReturn import SAverageReturn
from SCoeffVar import SCoeffVar
from STrend import STrend
from SRelStrInd import SRelStrInd
from DayOverAverageRollingVolume import DayOverAverageRollingVolume
from SAverageRollingVolume import SAverageRollingVolume
from SAdjustedClose import SAdjustedClose
from SAverageReturn import SAverageReturn
from pandas import read_csv
from DatabaseGrabber import DatabaseGrabber
from SCommodityChannelIndex import SCommodityChannelIndex
import os

counter = 1
#import the CSV
#df = read_csv('goodsymbols.csv', sep = ',')
#df = df[300]
#symbols = df.Symbol.values
#port = os.listdir('F:\\Users\\AmatVictoriaCuram\\Database')
port=['ABIO', 'ACST', 'AEZS', 'AGRX', 'AIRI', 'AKER', 'AKTX', 'AMCN', 'AMDA', 'AMRS', 'AMTX', 'ANTH', 'ANY', 'APDN', 'APHB', 'AQXP', 'ARDM', 'ARDX', 'ARGS', 'AST', 'ATOS', 'BAS', 'BCEI', 'BIOC', 'BIS', 'BSPM', 'BST', 'BSTG', 'BXE', 'CAPR', 'CBIO', 'CCCL', 'CCCR', 'CCIH', 'CDTI', 'CEI', 'CGIX', 'CLBS', 'CLRB', 'CPHI', 'CPST', 'CRMD', 'CSLT', 'CTIC', 'CTRV', 'CVEO', 'CXRX', 'CYCC', 'CYTX', 'DCIX', 'DFBG', 'DRIO', 'DRYS', 'ECR', 'EGLE', 'EGLT', 'EIGR', 'EKSO', 'EPE', 'ERI', 'ESEA', 'ESES', 'ESNC', 'EVEP', 'EVOK', 'FCSC', 'FHB', 'FIV', 'FNCX', 'FNJN', 'FSNN', 'FTD', 'GENE', 'GEVO', 'GLBS', 'GNCA', 'GPRO', 'GRAM', 'GSAT', 'HK', 'HLG', 'HMNY', 'HTBX', 'IGC', 'IMMY', 'IMUC', 'INVT', 'IPDN', 'IPWR', 'IZEA', 'JASN', 'JMEI', 'JONE', 'KODK', 'LEDS', 'LEJU', 'LITB', 'LLEX', 'LODE', 'LPCN', 'MACK', 'MARA', 'MATN', 'MBII', 'MBVX', 'MCEP', 'MEIP', 'MNGA', 'MOMO', 'MPO', 'MYOS', 'NAKD', 'NAO', 'NEON', 'NEOS', 'NLST', 'NRE', 'NSPR', 'NTB', 'NURO', 'NVIV', 'NWBO', 'NXTD', 'OCLR', 'OGEN', 'OHGI', 'OMED', 'ONCS', 'ONTX', 'OPHC', 'OPHT', 'OPTT', 'ORIG', 'OVAS', 'PED', 'PEIX', 'PGLC', 'PLG', 'PSTI', 'PULM', 'RBS', 'RGLS', 'RGSE', 'RIBT', 'RMGN', 'ROSG', 'RUBI', 'RXII', 'SAEX', 'SALT', 'SBLK', 'SCON', 'SCYX', 'SGOC', 'SHIP', 'SHOS', 'SNSS', 'SQQQ', 'SXE', 'SYN', 'TBK', 'TCS', 'TEAR', 'TGTX', 'TNDM', 'TNXP', 'TOPS', 'TROV', 'TRVN', 'TVIX', 'TWER', 'TWLO', 'USLV', 'UUUU', 'UVXY', 'VIIX', 'VIVE', 'VJET', 'VRML', 'VSAR', 'VTGN', 'VXX', 'WHLR', 'WMLP', 'XGTI', 'XPLR', 'XTNT', 'YGE']
refinedportfolio = []
#print(symbols)
for s in port:
    try:
        print(counter)
        counter = counter + 1
        q = DatabaseGrabber(s)        
        if float(SAverageReturn(q)) < -1:
#            if float(SCoeffVar(q)) < -5:
            if float(SAverageRollingVolume(q)) > 50000:
                if float(SAge(q)) > 1000:
#                        if float(SRelStrInd(q)) < 30:
#                            if float(SCommodityChannelIndex(q)) < -80:
                    #   ask another if or do commands
                        print(s)
                        refinedportfolio.append(s)
#                            else:
#                                continue
#                        else:
#                            continue
#                    else:
#                        continue
#                else:
#                    continue
#            else:
#                continue
        else:
            continue


#                ) > 500000 and sum( and sum(SRelStrInd(q)) < 30:
        
#              and sum(DayOverAverageRollingVolume(q)
#        ) > 5 and sum(SAverageReturn(q)) < .02 and sum(SCoeffVar(q)
#        ) < 1:
    except OSError:
        pass
#List refined portfolio
print(refinedportfolio)
