# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 12:05:09 2017

@author: AmatVictoriaCuramIII
"""
#backwards string programs
def main():
    userInput = getInput()
    reverseAndDisplay(userInput)
def getInput():
    print('Please enter a string that you would like displayed backwards.')
    stringy = input("")
    return stringy
def reverseAndDisplay(userInput):
    newlist = []
    reverserange = range(len(userInput)-1,-1,-1)
    for i in reverserange:
        newlist.append(userInput[i])
    newstring = ''.join(newlist)
    print(newstring)
main()