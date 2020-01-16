# -*- coding: utf-8 -*-
"""
Created on Sat May 20 16:33:06 2017

@author: AmatVictoriaCuramIII
"""

#This is an outdated database query tool

import os 
import pandas as pd
index = range(0,len(os.listdir('F:\\Users\\AmatVictoriaCuram\\Database')))
goodsymbols = pd.DataFrame(os.listdir('F:\\Users\\AmatVictoriaCuram\\Database')
 ,columns = ['Symbol'])
for i in index:
    goodsymbols['Symbol'][i] = goodsymbols['Symbol'][i]#[:-4]
print(goodsymbols)
goodsymbols.to_csv('newgoodsymbols.csv',sep=',')
