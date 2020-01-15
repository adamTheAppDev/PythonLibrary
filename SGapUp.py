# -*- coding: utf-8 -*-
"""
Spyder Editor
"""

#This is a summary statistic + database query tool

def SGapUp(s):
    import numpy as np
    s['GapUp'] = (s['High'].shift(1) - s['Low']) / s['Adj Close'].shift(1)
    s['GapUp'] = s['GapUp'][s['GapUp'] < 0]
    s['GapUp'] = s['GapUp'].fillna(0)
    s['GapUp'] = np.where(s['GapUp'] == 0 , 0, (-1*s['GapUp']))
    return s['GapUp'].tail(1)    
