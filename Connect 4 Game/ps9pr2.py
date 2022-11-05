#
# ps9pr2.py (Problem Set 9, Problem 2)
#
# A Connect-Four Player class 
#  

from ps9pr1 import Board

# write your class below.

class Player:
    
    def __init__(self, checker):
        """
        Constructor that initializes the attributes in 
        Player, checker

        """
        assert(checker == 'X' or checker == 'O')
        self.checker = checker
        self.num_moves = 0
    
    def __repr__(self):
        """ Returns a string that represents the Player object"""
        if self.checker == 'X':
            return 'Player X'
        if self.checker == 'O':
            return 'Player O'
        
    def opponent_checker(self):
        """ Returns the checker the opponent is using """
        if self.checker == 'X':
            return 'O'
        if self.checker == 'O':
            return 'X'
    
    def next_move(self, b):
        """ Determines whether the inputted column number is a valid spot to 
        put a checker """
        self.num_moves += 1
        while True:
           col = int(input('Enter a column: '))
           if b.width > col >= 0:
               return col
           else:
               print('Try again!')
    