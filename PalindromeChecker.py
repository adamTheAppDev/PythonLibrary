# -*- coding: utf-8 -*-
"""
Created on Tue May  9 23:00:14 2017

@author: AmatVictoriaCuramIII
"""
def main():
    print('What palindrome would you like to test?')
    string = input('')
    start = 0 
    end = -1
    isPalindrome(string,start,end)
def isPalindrome(string,start,end):  
    answer = 'y'
    while answer == 'y':
        if start > 200: #this statement is for limiting infinity loops
            return False
        try:
            if string[start] == string[end]:
                return isPalindrome(string,start+1,end-1)
            else:
                print('It is not a palindrome')
                print('Would you like to try another palindrome?')
                print('Enter ''y'' to try again, or any other response to quit')
                answer = input('')       
                if answer =='y':
                    print('Enter new palindrome')
                    string = input('')
                    continue
                return False 
        except IndexError:
                        print('It is a palindrome.')
                        print('Would you like to try another palindrome? y/n')
                        answer = input('')       
                        if answer =='y':
                            print('Enter new palindrome')
                            string = input('')
                            isPalindrome(string,0,-1)
main()