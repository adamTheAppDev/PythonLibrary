# -*- coding: utf-8 -*-
"""
Spyder Editor
"""

#This is a summary statistic + database query tool

def SGapDown(s):
    s['GapDown'] = (s['Low'].shift(1) - s['High']) / s['Adj Close'].shift(1)
    s['GapDown'] = s['GapDown'][s['GapDown'] > 0]
    s['GapDown'] = s['GapDown'].fillna(0)
    return s['GapDown'].tail(1)
