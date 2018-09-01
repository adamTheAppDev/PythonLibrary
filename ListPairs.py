# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 00:37:10 2017

@author: Adam Reinhold Von Fisher - adamrvfisher@gmail.com 
linkedin.com/in/adamrvfisher - github.com/adamrvfisher/TechnicalAnalysisLibrary
"""
#pairing a list into a comprehensive list of pairs.
def ListPairs(tickers):
    import itertools as it
    sublist = it.combinations(tickers, 2)
    fulllist = list(sublist)
    return fulllist
