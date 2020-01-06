# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 12:36:13 2017

@author: AmatVictoriaCuramIII
"""

#Tick Tack Toe
def main():
  again = True
  while again==True:
    play_1_game()
    again = get_yes_or_no("Would you like to play again (Y/N)? ")
    
def get_yes_or_no(prompt):
  input_str = input(prompt)
  while (True):
    if ((input_str== 'Y') or (input_str== 'y')):
      return True
    if ((input_str== 'N') or (input_str== 'n')):
      return False
    print( "Invalid Input")
    input_str = input(prompt)
      
def play_1_game():
  board = [['*','*','*'], ['*','*','*'], ['*','*','*']]
  move_count = 0
  display_board(board)
  while (True):

    move_count +=1
    return
  
  print("code for play 1 game")
  
def display_board(board):
  print ('--------')
  for i in range(len(board)):
    print('|' + board[i][0] + '|'+ board[i][1] + '|' + board[i][2]+'|' )
  print ('--------')
main()