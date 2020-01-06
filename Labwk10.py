# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 17:03:49 2017

@author: AmatVictoriaCuramIII
"""

#Lab10pt2
file = open("numbers.txt","r") 
largest = (-99999999999**1500)
for line in file: 
    if int(line) > largest:
        largest = int(line)
print(largest)