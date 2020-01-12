# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 23:29:44 2017

@author: AmatVictoriaCuramIII
"""

#This is a sorting and database query tool, technical indicators must be populated already
#This lists all stock tickers that pass the scan

#Import modules
from DatabaseGrabber import DatabaseGrabber
import os
from YahooSourceDailyGrabber import YahooSourceDailyGrabber
import pandas as pd

#Variable assignment
Counter = 0
Empty = []
Empty2 = []
#Universe = os.listdir('F:\\Users\\AmatVictoriaCuram\\Database')
Universe = ['ABIO', 'ACST', 'AEZS', 'AGRX', 'AIRI', 'AKER', 'AKTX', 'AMCN']# 'AMDA', 'AMRS', 'AMTX', 'ANTH', 'ANY', 'APDN', 'APHB', 'AQXP', 'ARDM', 'ARDX', 'ARGS', 'AST', 'ATOS', 'BAS', 'BCEI', 'BIOC', 'BIS', 'BSPM', 'BST', 'BSTG', 'BXE', 'CAPR', 'CBIO', 'CCCL', 'CCCR', 'CCIH', 'CDTI', 'CEI', 'CGIX', 'CLBS', 'CLRB', 'CPHI', 'CPST', 'CRMD', 'CSLT', 'CTIC', 'CTRV', 'CVEO', 'CXRX', 'CYCC', 'CYTX', 'DCIX', 'DFBG', 'DRIO', 'DRYS', 'ECR', 'EGLE', 'EGLT', 'EIGR', 'EKSO', 'EPE', 'ERI', 'ESEA', 'ESES', 'ESNC', 'EVEP', 'EVOK', 'FCSC', 'FHB', 'FIV', 'FNCX', 'FNJN', 'FSNN', 'FTD', 'GENE', 'GEVO', 'GLBS', 'GNCA', 'GPRO', 'GRAM', 'GSAT', 'HK', 'HLG', 'HMNY', 'HTBX', 'IGC', 'IMMY', 'IMUC', 'INVT', 'IPDN', 'IPWR', 'IZEA', 'JASN', 'JMEI', 'JONE', 'KODK', 'LEDS', 'LEJU', 'LITB', 'LLEX', 'LODE', 'LPCN', 'MACK', 'MARA', 'MATN', 'MBII', 'MBVX', 'MCEP', 'MEIP', 'MNGA', 'MOMO', 'MPO', 'MYOS', 'NAKD', 'NAO', 'NEON', 'NEOS', 'NLST', 'NRE', 'NSPR', 'NTB', 'NURO', 'NVIV', 'NWBO', 'NXTD', 'OCLR', 'OGEN', 'OHGI', 'OMED', 'ONCS', 'ONTX', 'OPHC', 'OPHT', 'OPTT', 'ORIG', 'OVAS', 'PED', 'PEIX', 'PGLC', 'PLG', 'PSTI', 'PULM', 'RBS', 'RGLS', 'RGSE', 'RIBT', 'RMGN', 'ROSG', 'RUBI', 'RXII', 'SAEX', 'SALT', 'SBLK', 'SCON', 'SCYX', 'SGOC', 'SHIP', 'SHOS', 'SNSS', 'SQQQ', 'SXE', 'SYN', 'TBK', 'TCS', 'TEAR', 'TGTX', 'TNDM', 'TNXP', 'TOPS', 'TROV', 'TRVN', 'TVIX', 'TWER', 'TWLO', 'USLV', 'UUUU', 'UVXY', 'VIIX', 'VIVE', 'VJET', 'VRML', 'VSAR', 'VTGN', 'VXX', 'WHLR', 'WMLP', 'XGTI', 'XPLR', 'XTNT', 'YGE']
#print(symbols)
for Ticker in Universe[:100]:
    try:
        Asset = YahooSourceDailyGrabber(Ticker)    
        DY = Asset['5wkEfficiency'][-1]
        Empty.append(Ticker)
        Empty2.append(DY)
        Emptyseries = pd.Series(Empty)
        print(Counter)
        Counter = Counter + 1        

    except OSError:
        pass
#List refined portfolio
RefinedPortfolio = pd.DataFrame(data = Empty2, index=Empty, columns = ['EF'])
SortedPortfolio = RefinedPortfolio.sort_values(by = ['EF'], ascending = True)
SortedPortfolio = SortedPortfolio.dropna()
print(SortedPortfolio)
