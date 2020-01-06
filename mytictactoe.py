# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 13:40:23 2017

@author: AmatVictoriaCuramIII
"""
#tictactoe
import numpy as np
board = np.array([['* |','* |','* |'],
['* |','* |','* |'],
['* |','* |','* |']])
takenspots = []
def restart():
  gameon = True
  while gameon==True:
      gameon = main()
#      gameon = checkOwin()
def main():
    displayboard()
    playerXgo()
    if playerXgo == False:
        return False
    playerOgo()
    if playerOgo == False:
        return False    
    playerXgo()
    if playerXgo == False:
        return False    
    playerOgo()
    if playerOgo == False:
        return False    
    playerXgo()
    if playerXgo == False:
        return False
    playerOgo()
    if playerOgo == False:
        return False    
    playerXgo()
    if playerXgo == False:
        return False
    playerOgo()
    if playerOgo == False:
        return False
    playerXgo()
    if playerXgo == False:
        return False
def displayboard(): 
    print('----------------------')
    print(board)
    print('----------------------')
def checkposition(x,y):
    truthvalue = [x,y] in takenspots
    if truthvalue == True:
        print('That position is taken, don\'t be a cheater!!! You lose a turn.')
        main()
def playerXgo():
    print('Enter row number (0-2) for your X')
    prex = input("")
    print('Enter column number (0-2) for your X')
    prey = input("")
    x = float(prex)
    y = float(prey) 
    position = [x,y]
    checkposition(x,y)
    takenspots.append(position)
    board[x][y] = 'X |'
    displayboard()
    checkXwin()
    if checkXwin() == False:
        endgame()    
        return False    
def playerOgo():
    print('Enter row number (0-2) for your O')
    prex = input("")
    print('Enter column number (0-2) for your O')
    prey = input("")
    x = float(prex)
    y = float(prey)
    position = [x,y]
    checkposition(x,y)
    takenspots.append(position)
    board[x][y] = 'O |'
    displayboard()
    checkOwin()
    if checkOwin() == False:
        endgame()
        return False
def checkXwin():
    if board[0][0] == 'X |' and board[0][1] == 'X |' and board[0][2] == 'X |':  
        print('Player X is the winner!!!') #top row
        return False
    if board[1][0] == 'X |' and board[1][1] == 'X |' and board[1][2] == 'X |':  
        print('Player X is the winner!!!') #middle row
        return False
    if board[2][0] == 'X |' and board[2][1] == 'X |' and board[2][2] == 'X |':  
        print('Player X is the winner!!!') #bottomrow
        return False
    if board[0][0] == 'X |' and board[1][0] == 'X |' and board[2][0] == 'X |':  
        print('Player X is the winner!!!') #left column
        return False
    if board[0][1] == 'X |' and board[1][1] == 'X |' and board[2][1] == 'X |':  
        print('Player X is the winner!!!') #middle column
        return False
    if board[0][2] == 'X |' and board[1][2] == 'X |' and board[2][2] == 'X |':  
        print('Player X is the winner!!!') #right column
        return False
    if board[0][0] == 'X |' and board[1][1] == 'X |' and board[2][2] == 'X |':  
        print('Player X is the winner!!!') #top left to bottom right diagonal
        return False
    if board[0][2] == 'X |' and board[1][1] == 'X |' and board[2][0] == 'X |':  
        print('Player X is the winner!!!') #top right to bottom left diagonal
        return False
def checkOwin():
    if board[0][0] == 'O |' and board[0][1] == 'O |' and board[0][2] == 'O |':  
        print('Player O is the winner!!!') #top row
        return False
    if board[1][0] == 'O |' and board[1][1] == 'O |' and board[1][2] == 'O |':  
        print('Player O is the winner!!!') #middle row
        return False
    if board[2][0] == 'O |' and board[2][1] == 'O |' and board[2][2] == 'O |':  
        print('Player O is the winner!!!') #bottomrow
        return False
    if board[0][0] == 'O |' and board[1][0] == 'O |' and board[2][0] == 'O |':  
        print('Player O is the winner!!!') #left column
        return False
    if board[0][1] == 'O |' and board[1][1] == 'O |' and board[2][1] == 'O |':  
        print('Player O is the winner!!!') #middle column
        return False
    if board[0][2] == 'O |' and board[1][2] == 'O |' and board[2][2] == 'O |':  
        print('Player O is the winner!!!') #right column
        return False
    if board[0][0] == 'O |' and board[1][1] == 'O |' and board[2][2] == 'O |':  
        print('Player O is the winner!!!') #top left to bottom right diagonal
        return False
    if board[0][2] == 'O |' and board[1][1] == 'O |' and board[2][0] == 'O |':  
        print('Player O is the winner!!!') #top right to bottom left diagonal 
        return False
def endgame():
    print('The game has ended')
restart()