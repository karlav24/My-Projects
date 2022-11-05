#
# ps9pr4.py (Problem Set 9, Problem 4)
#
# AI Player for use in Connect Four  
#

import random  
from ps9pr3 import *

class AIPlayer(Player):
    def __init__(self, checker, tiebreak, lookahead):
        """ Constructor that initializes the checker, the tiebreak, and the 
        lookahead attributes"""
        assert(checker == 'X' or checker == 'O')
        assert(tiebreak == 'LEFT' or tiebreak == 'RIGHT' or tiebreak == 'RANDOM')
        assert(lookahead >= 0)
        super().__init__(checker)
        self.tiebreak = tiebreak
        self.lookahead = lookahead
    
    def __repr__(self):
        """ Returns a string representation of the object"""
        if self.checker == 'X':
            s = 'Player X '
        if self.checker == 'O':
            s = 'Player O '
        s += '('
        s += self.tiebreak
        s += ', '
        if type(self.lookahead) == int:
            s += str(self.lookahead)
        s += ')'
        return s
    
    def max_score_column(self, scores):
        """ Determines the maximum score for each of the columns and 
        implements a tiebreak method for if more than one column
        shares the same value, returning a single column number"""
        maximum = max(scores)
        list_max = []
        for i in range(len(scores)):
            if scores[i] == maximum:
                list_max += [i]
        if len(list_max) > 1:
            if self.tiebreak == 'LEFT':
                return list_max[0]
            if self.tiebreak == 'RIGHT':
                return list_max[-1]
            if self.tiebreak == 'RANDOM':
                return list_max[random.choice(range(len(list_max)))]
        else:
            return list_max[0]
        
    def scores_for(self, b):
        """"""
        board = Board(6, 7)
        board.slots = b.slots[:]
        scores = [50] * (b.width)
        for col in range(b.width):
            if b.can_add_to(col) == False:
                scores[col] = -1
            elif b.is_win_for(self.checker):
                scores[col] = 100
            elif b.is_win_for(self.opponent_checker()):
                scores[col] = 0
            elif self.lookahead == 0:
                scores[col] = 50
            elif self.lookahead > 0 and b.can_add_to(col) == True:
                 board.add_checker(self.checker, col)
                 opponent_checker = self.opponent_checker()
                 opponent_lookahead = self.lookahead - 1
                 opponent = AIPlayer(opponent_checker, self.tiebreak, opponent_lookahead)
                 opp_scores = opponent.scores_for(b)
                 biggest_val = max(opp_scores)
                 if opponent_lookahead == 1:
                     if biggest_val == 50 and board.is_win_for(self.checker):
                         scores[col] == 50 
                     if biggest_val == 100:
                         scores[col] == 100
                     if biggest_val == 0:
                         scores[col] = 0
                 
                 b.remove_checker(col)
        return scores   
     
        