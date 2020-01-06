# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 23:39:56 2017

@author: AmatVictoriaCuramIII
"""
def GetANumber(LowerBound, UpperBound):
    BadInput = True
    while BadInput == True:
        print("Please enter a number within the bounds.")
        ChosenNumber = input("")
        try:
            number = float(ChosenNumber)
        except ValueError:
            print("You have not entered a number.")
            continue
        if number >= LowerBound and number <= UpperBound:
            return number
        else:
            BadInput = True
        print("Invalid Input")
GetANumber(0, 100)
