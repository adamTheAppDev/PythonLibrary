# -*- coding: utf-8 -*-
"""
Created on Tue May  2 11:09:20 2017

@author: AmatVictoriaCuramIII
"""

#This is a database query tool

def SAdjustedClose(s):
    return s['Adj Close'].tail(1)
