# -*- coding: utf-8 -*-
from random import randint

# Game settings
guesses = 10
dimensions = 15
direction = randint(0,1)
ocean_sym = ' ~ '
v_front_sym = '/ \\'
v_middle_sym = '|Ξ|'
v_tail_sym = '\ /'
h_front_sym = 'Ξ >'
h_middle_sym = 'ΞΞΞ'
h_tail_sym = '< Ξ'
v_front_hsym = '/X\\'
v_middle_hsym = '|X|'
v_tail_hsym = '\X/'
h_front_hsym = 'ΞX>'
h_middle_hsym = 'ΞXΞ'
h_tail_hsym = '<XΞ'

# Create N x N board
board = []
def board_dimensions(dimensions):
    for x in range(dimensions):
        board.append(['%s' % (ocean_sym)] * dimensions)
board_dimensions(dimensions)

# Function to print board
def print_board(board):
    cols = range(1, len(board[0]) +1)
    rows = 1
    print "    ",
    for n in cols:
        if n < 10:
            print str(n) + " ",
        else:
            print str(n), 
    print
    print "    " + ("---" * dimensions)
    for row in board:
        if rows < 10:
            print " " + str(rows) + " |" + "".join(row)
            rows += 1
        else:
            print str(rows) + " |" + "".join(row)
            rows += 1

    return board

# Create a three-space battleship
if direction > 0: # Create battleship vertically
    ship_col = randint(0, len(board[0]) - 1)
    ship_row = randint(1, len(board) - 2)
    ship_front = ship_row - 1 
    ship_tail = ship_row + 1
else: # Create battleship horizontally
    ship_col = randint(1, len(board[0]) - 2)
    ship_row = randint(0, len(board) - 1)
    ship_front = ship_col + 1
    ship_tail = ship_col - 1
h_ship_cols = [ship_col, ship_front, ship_tail]

# Print ship created vertically or horizontally
if direction > 0:
    def print_ship():
        board[ship_front][ship_col] = "%s" % (v_front_sym)
        board[ship_row][ship_col] = "%s" % (v_middle_sym)
        board[ship_tail][ship_col] = "%s" % (v_tail_sym)
else:
    def print_ship():
        board[ship_row][ship_tail] = "%s" % (h_tail_sym)
        board[ship_row][ship_col] = "%s" % (h_middle_sym)
        board[ship_row][ship_front] = "%s" % (h_front_sym)

# Define 'hot' 'warm' and 'cool' areas for ships created vertically or horizontally
if direction > 0:
    hot_rows = range(ship_row-2, ship_row+3)
    hot_cols = range(ship_col-1, ship_col+2)
    warm_rows = range(ship_row-4, ship_row+5)
    warm_cols = range(ship_col-3, ship_col+4)
    cool_rows = range(0,len(board))
    cool_cols = range(0,len(board[0]))
else:
    hot_cols = range(ship_col-2, ship_col+3)
    hot_rows = range(ship_row-1, ship_row+2)
    warm_cols = range(ship_col-4, ship_col+5)
    warm_rows = range(ship_row-3, ship_row+4)
    cool_cols = range(0,len(board))
    cool_rows = range(0,len(board[0]))

# Check to see if guess was in 'hot' 'warm' or 'cool' area
def check_hot(guess_col, guess_row):
    for i in hot_cols:
        for n in hot_rows:
            if i == guess_col and \
               n == guess_row:       
                return True             
def check_warm(guess_col, guess_row):
    for i in warm_cols:
        for n in warm_rows:
            if i == guess_col and \
               n == guess_row and \
               check_hot(guess_col,guess_row) != True:
                return True               
def check_cool(guess_col, guess_row):
    for i in cool_cols:
        for n in cool_rows:
            if i == guess_col and \
               n == guess_row and \
               check_warm(guess_col,guess_row) != True:
                return True

# Take guesses and print results of each turn
print "Let's Play Battleship!"
print "You have %d guesses to sink my battleship." % (guesses)
print_board(board)
for turn in range(guesses):
    print
    print "-> Turn", turn + 1
    col_input = raw_input("Guess Col: ")
    row_input = raw_input("Guess Row: ")
    # Make sure input is a positive number
    while col_input.isdigit() != True or \
          row_input.isdigit() != True:
        print "Enter a number dummy!"
        print
        col_input = raw_input("Guess Col: ")
        row_input = raw_input("Guess Row: ")
    else: 
        guess_col = int(col_input) - 1
        guess_row = int(row_input) - 1
    
    if direction > 0: # If battleship created vertically
        if guess_col == ship_col and \
          (guess_row == ship_row or \
           guess_row == ship_front or \
           guess_row == ship_tail):
            print_ship()
            if guess_row == ship_front:
                board[ship_front][ship_col] = "%s" % (v_front_hsym)
            elif guess_row == ship_row:
                board[ship_row][ship_col] = "%s" % (v_middle_hsym)
            elif guess_row == ship_tail:
                board[ship_tail][ship_col] = "%s" % (v_tail_hsym)
            print_board(board)
            print "Congratulations! You sunk my battleship!"
            break
        else:
            if turn == guesses - 1:
                if (guess_col < 0 or guess_col > len(board[0])) or \
                   (guess_row < 0 or guess_row > len(board)):
                    print_ship()
                    print_board(board)
                    print "LOL. That's not even in the ocean."
                    print "Game Over!"
                    break
                elif board[guess_row][guess_col] == " H " or \
                     board[guess_row][guess_col] == " W " or \
                     board[guess_row][guess_col] == " C ":                
                    print_ship()
                    print_board(board)
                    print "Dude, you guessed that one already."
                    print "Game Over!"
                    break
                else:
                    if check_hot(guess_col,guess_row) == True:
                        board[guess_row][guess_col] = " H "
                    elif check_warm(guess_col,guess_row) == True:
                        board[guess_row][guess_col] = " W "
                    elif check_cool(guess_col,guess_row) == True:
                        board[guess_row][guess_col] = " C "
                    print_ship()
                    print_board(board)
                    print "Game Over!"
                    break
            elif (guess_col < 0 or guess_col > len(board[0]) -1) or \
               (guess_row < 0 or guess_row > len(board) -1):
                print_board(board)
                print "LOL. That's not even in the ocean."
                print "You just wasted a turn!"
                continue
            elif board[guess_row][guess_col] == " H " or \
                 board[guess_row][guess_col] == " W " or \
                 board[guess_row][guess_col] == " C ": 
                print_board(board)
                print "Dude, you guessed that one already."
                print "You just wasted a turn!"
                continue
            else:
                if check_hot(guess_col,guess_row) == True:
                    board[guess_row][guess_col] = " H "
                elif check_warm(guess_col,guess_row) == True:
                    board[guess_row][guess_col] = " W "
                elif check_cool(guess_col,guess_row) == True:
                    board[guess_row][guess_col] = " C "
                print_board(board)
                print "Missed Me!"
    elif direction < 1: # If battleship created horizontally
        if guess_row == ship_row and \
          (guess_col == ship_col or \
           guess_col == ship_front or \
           guess_col == ship_tail):
            print_ship()
            if guess_col == ship_front:
                board[ship_row][ship_front] = "%s" % (h_front_hsym)
            elif guess_col == ship_col:
                board[ship_row][ship_col] = "%s" % (h_middle_hsym)
            elif guess_col == ship_tail:
                board[ship_row][ship_tail] = "%s" % (h_tail_hsym)
            print_board(board)
            print "Congratulations! You sunk my battleship!"
            break
        else:
            if turn == guesses - 1:
                if (guess_col < 0 or guess_col > len(board[0])) or \
                   (guess_row < 0 or guess_row > len(board)):
                    print_ship()
                    print_board(board)
                    print "LOL. That's not even in the ocean."
                    print "Game Over!"
                    break
                elif board[guess_row][guess_col] == " H " or \
                     board[guess_row][guess_col] == " W " or \
                     board[guess_row][guess_col] == " C ":                
                    print_ship()
                    print_board(board)
                    print "Dude, you guessed that one already."
                    print "Game Over!"
                    break
                else:
                    if check_hot(guess_col,guess_row) == True:
                        board[guess_row][guess_col] = " H "
                    elif check_warm(guess_col,guess_row) == True:
                        board[guess_row][guess_col] = " W "
                    elif check_cool(guess_col,guess_row) == True:
                        board[guess_row][guess_col] = " C "
                    print_ship()
                    print_board(board)
                    print "Game Over!"
                    break
            elif (guess_col < 0 or guess_col > len(board[0]) -1) or \
               (guess_row < 0 or guess_row > len(board) -1):
                print_board(board)
                print "LOL. That's not even in the ocean."
                print "You just wasted a turn!"
                continue
            elif board[guess_row][guess_col] == " H " or \
                 board[guess_row][guess_col] == " W " or \
                 board[guess_row][guess_col] == " C ": 
                print_board(board)
                print "Dude, you guessed that one already."
                print "You just wasted a turn!"
                continue
            else:
                if check_hot(guess_col,guess_row) == True:
                    board[guess_row][guess_col] = " H "
                elif check_warm(guess_col,guess_row) == True:
                    board[guess_row][guess_col] = " W "
                elif check_cool(guess_col,guess_row) == True:
                    board[guess_row][guess_col] = " C "
                print_board(board)
                print "Missed Me!"
    if check_hot(guess_col,guess_row) == True:
        print 'You are hot'  
    elif check_warm(guess_col,guess_row) == True:
        print 'You are warm'
    elif check_cool(guess_col,guess_row) == True:
        print 'You are cool'

