# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 20:13:27 2017

@author: AmatVictoriaCuramIII
"""
print('Please enter the strung together sentence.')
originalString = input("")
newString = ""
counter = 0
for i in originalString:
    if i.isupper():
        if counter == 0:
            newString = newString + i   
        else:
            newString = newString + ' ' + i.lower()
    else:
        newString = newString + i
        counter = counter + 1
print(newString)