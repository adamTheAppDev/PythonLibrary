# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 00:37:10 2017

@author: Adam Reinhold Von Fisher 
linkedin.com/in/adamrvfisher 
"""

#This program takes a list and pairs all combinations into a comprehensive list of pairs.
#It plugs in to the speed dater

def ListPairs(tickers):
    import itertools as it
    sublist = it.combinations(tickers, 2)
    fulllist = list(sublist)
    return fulllist
