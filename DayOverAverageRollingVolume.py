# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 13:31:53 2017

@author: AmatVictoriaCuramIII
"""
def DayOverAverageRollingVolume(s):
    window = 60
    s['AverageRollingVolume'] = s['Volume'].rolling(center=False, 
                                                        window=window).mean()
    s['DayOverARV'] = s['Volume']/s['AverageRollingVolume'] 
    return s['DayOverARV'].tail(1)