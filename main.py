#
# pyblackjack/main.py
#
# The main file. This will be the Python script to be executed in order for the
# game to run.

# Import everything from the games module
from game import *

print 'PyBlackjack'
print 'A small CLI-based Blackjack game simulator'
print 'Copyright 2012 Aldo Rey Balagulan, Licensed under GNU GPL v3'

option = ''
while option != 'q' and option != 'Q':
    option = raw_input('Options:\n\t[E]asy - 5000 chips\n\t' + 
            '[N]ormal - 2000 chips\n\t' +
            '[H]ard - 500 chips\n\t[R]ags to Riches - 1 chip\n\t' +
            '[Q]uit\nOption: ')
    if option == 'e' or option == 'E':
        game = Game(5000)
    elif option =='n' or option == 'N':
        game = Game(2000)
    elif option == 'h' or option == 'H':
        game = Game(500)
    elif option == 'r' or option == 'R':
        game = Game(1)
