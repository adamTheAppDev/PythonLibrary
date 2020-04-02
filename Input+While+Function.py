# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#Input, while loops, functions

#Definte function
def GetANumber(LowerBound, UpperBound):
    #Flag
    BadInput = True
    #Until valid input received
    while BadInput == True:
        print("Please enter a number within the bounds.")
        ChosenNumber = input("")

        try:
            #Convert to float
            number = float(ChosenNumber)
        except ValueError:
            print("You have not entered a number.")
            continue
        #Input test
        if number >= LowerBound and number <= UpperBound:
            #Valid input
            return number
        else:
            #Invalid input
            BadInput = True
        print("Invalid Input")
#Run function
GetANumber(0, 100)
