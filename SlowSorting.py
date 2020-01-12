# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 21:41:36 2017

@author: AmatVictoriaCuramIII
"""

#EZ sorting, gross, let's make a deboaz tree instead.

import pandas as pd
#import numpy as np
import random as rand
print('How many integers would you like to include in this array?')
arraysize = int(input(""))
counter = range(1,arraysize+1)
array = pd.Series(counter)
for i in counter:
    array[i] = rand.randint(1,9)
array2 = array 
array3 = array
def main():
    bubblesort(array)
    insertionsort(array2)
    selectionsort(array3)
#bubblesort
def bubblesort(array):
    print('Bubble sort') 
    print('------------')
    swaps = 0
    for i in range(len(array)-1,0,-1): #reverse list -1
        for r in range(i):
            if array[r] > array[r + 1]:
                swaps = swaps + 1
                temp = array[r]
                array[r] = array[r + 1]
                array[r + 1] = temp
    print(array)
    print('Number of swaps = ',swaps)
    print('')
#insertion sort
def insertionsort(array2):
    print('Insertion sort')
    print('---------------')
    swaps = 0    
    for i in range(1,len(array2)):
        currentvalue = array[i]
        position = i
        while position > 0 and array[position-1] > currentvalue:
            array[position] = array[position-1]
            position = position - 1
        swaps = swaps + 1
        array[position] = currentvalue
    print(array2)
    print('Number of swaps = ',swaps)
    print('')
def selectionsort(array3):
    print('Selection sort')
    print('---------------')    
    swaps = 0    
    for i in range(len(array3)-1,0,-1):
        positionofmax = 0
        for r in range(1, i + 1):
            if array[r] > array[positionofmax]:
                positionofmax = r
                swaps = swaps + 1
        temp = array[i]
        array[i] = array[positionofmax]
        array[positionofmax] = temp
    print(array3)
    print('Number of swaps = ',swaps)
    print('')
main()
