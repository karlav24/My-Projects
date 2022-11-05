#
# ps9pr1.py (Problem Set 9, Problem 1)
#
# A Connect Four Board class
#
# Computer Science 111
#

class Board:
    """ a data type for a Connect Four board with arbitrary dimensions
    """   
    ### add your constructor here ###
    def __init__(self, height, width):
        """ Constructor that initializes the two attributes in 
        each Board object, (height, width)

        """
        self.height = height
        self.width = width
        self.slots = [[' '] * self.width for row in range(self.height)]
        
    def __repr__(self): 
        """ Returns a string that represents a Board object.
        """
        s = ''         #  begin with an empty string

        # add one row of slots at a time to s
        for row in range(self.height):
            s += '|'   # one vertical bar at the start of the row

            for col in range(self.width):
                s += self.slots[row][col] + '|'

            s += '\n'  # newline at the end of the row

        ### add your code here ###
        for row in range((self.width * 2) + 1):
            s  += '-'
        s += '\n'
        s += ' '
        col_num = 0 
        for row in range(self.width):
            if col_num >= 10:
                col_num = col_num - 10
            s += str(col_num)
            s += ' '
            col_num += 1
        return s

    def add_checker(self, checker, col):
        """ adds the specified checker (either 'X' or 'O') to the
            column with the specified index col in the called Board.
            inputs: checker is either 'X' or 'O'
                    col is a valid column index
        """
        assert(checker == 'X' or checker == 'O')
        assert(col >= 0 and col < self.width)
        
        ### put the rest of the method here ###
        row = 0
        while row < self.height and self.slots[row][col] == ' ': 
            #if row == self.height:
                #break
            row += 1
        self.slots[row - 1][col] = checker
            
    ### add your reset method here ###
    def reset(self):
        """ Resets the board, making it empty again"""
        for r in range(self.height):
            for c in range(self.width):
                self.slots[r][c] = ' '
    
    def add_checkers(self, colnums):
        """ takes a string of column numbers and places alternating
            checkers in those columns of the called Board object,
            starting with 'X'.
            input: colnums is a string of valid column numbers
        """
        checker = 'X'   # start by playing 'X'

        for col_str in colnums:
            col = int(col_str)
            if 0 <= col < self.width:
                self.add_checker(checker, col)

            if checker == 'X':
                checker = 'O'
            else:
                checker = 'X'

    ### add your remaining methods here
    def can_add_to(self, col):
        """ Determines if a given column in the Boardn object
        can have a checker added to it"""
        height = self.height
        width = self.width
        count = 0
        for row in range(height):
            if col not in range(width):
                return False
            if self.slots[row][col] == ' ':
                count += 1
        if count > 0:
            return True
        else:
            return False
    def is_full(self):
        """ Determines if the entire Board object is full"""
        width = self.width
        for i in range(width):
            if self.can_add_to(i) == True:
                return False
        return True
    
    def remove_checker(self, col):
        """ Removes a checker from the top of the inputted column """
        row = 0
        if row < self.height:
            if self.slots[row][col] == ' ':
                row += 1
            if self.slots[row][col] != ' ':
                self.slots[row][col] = ' '
    
    def is_horizontal_win(self, checker):
        """ Checks for a horizontal win for the specified checker.
        """
        for row in range(self.height):
            for col in range(self.width - 3):
            # Check if the next four columns in this row
            # contain the specified checker.
                if self.slots[row][col] == checker and \
                self.slots[row][col + 1] == checker and \
                self.slots[row][col + 2] == checker and \
                self.slots[row][col + 3] == checker:
                   return True
        return False
   
    def is_vertical_win(self, checker):
        """ Checks for a vertical win for the specified checker """
        for col in range(self.width):
            for row in range(self.height - 3):
                if self.slots[row][col] == checker and \
                self.slots[row + 1][col] == checker and \
                self.slots[row + 2][col] == checker and \
                self.slots[row + 3][col] == checker:
                    return True
        return False
    
    def is_down_diagonal_win(self, checker):
        """ Checks for a down diagonal win for the specified checker """
        for row in range(self.height - 3):
            for col in range(self.width - 3):
                if self.slots[row][col] == checker and\
                self.slots[row + 1][col + 1] == checker and \
                self.slots[row + 2][col + 2] == checker and \
                self.slots[row + 3][col + 3] == checker:
                    return True
        return False
    def is_up_diagonal_win(self, checker):
        """ Checks for a up diagonal win for the specified checker """
        for row in range(self.height - 3):
            for col in range(self.width - 3):
                if self.slots[row + 3][col] == checker and\
                self.slots[row + 2][col + 1] == checker and \
                self.slots[row + 1][col + 2] == checker and \
                self.slots[row][col + 3] == checker:
                    return True
   
    def is_win_for(self, checker):
        """ Checks for any wins for the specified checker """
        assert(checker == 'X' or checker == 'O')
               
        if self.is_vertical_win(checker) == True:
            return True
        if self.is_horizontal_win(checker) == True:
            return True
        if self.is_down_diagonal_win(checker) == True:
            return True
        if self.is_up_diagonal_win(checker) == True:
            return True
        else:
            return False
            
            
