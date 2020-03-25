from pseudolegalmoves import pseudo_legal_moves
from islegal import is_legal
import copy
from anytree import NodeMixin, RenderTree
from morehelpers import FEN_recover, print_doc, printboard, log_incorrect_input

# This file contains a ton of useful functions that get used throughout the program.


# My definition of the board class.  If I could start over, I'd do a lot more with class methods.
# Basically this is just a seperated out version of a FEN, though I store some of the data slightly differently
class board():
    def __init__(self, status, turn, castle, passant, half, whole):
        self.status = status
        self.turn = turn
        self.castle = castle
        self.passant = passant
        self.half = half
        self.whole = whole

# #The node of the tree that I'll use to store the game
# class boardnode(board, NodeMixin):
#     def __init__(self, parent=None):
#         self.parent = parent
#         self.simple_eval = simple_eval
#         self.complex_eval = complex_eval
#         self.priority = priority




# Takes in a FEN, double check its data, load it into my 'board' class.  One of the earlier functions I wrote, I'm not very happy with it now!
def FENload(FEN):

    # Declare a blank chessboard, and we will fill in the blanks as we go
    chessboard = board(None, None, None, None, None, None)
    temp = FEN.split()
    # Check that our input FEN has all the components
    if len(temp) != 6:
        print ("Provided FEN is invalid! Incorrect number of arguments")
        return False

    # We will strip the FEN-board of the /'s and the integers and move the string onto this temp1 string
    temp1 = ""
    # Iterates over the FEN-style boardstate and creates our teporary string
    for char in temp[0]:
        if char.isalpha():
            temp1 += char
        elif char.isdigit():
            for j in range(int(char)):
                temp1 += "0"

    # Quick error check
    if len(temp1) != 64:
        print ("Provided FEN is invalid! Board state is incorrect length")
        return False

    # Now we move from the temp1 string onto our boardstate
    chessboard.status = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
    i = 0
    for row in range(8):
        for square in range(8):
            chessboard.status[7-row][square] = temp1[i]
            i += 1

    # The rest of the items are quick transfers from the FEN to the chessboard.  Each gets error-checked just in case. TODO
    if temp[1] not in ("w","b"):
        print ("Provided FEN is invalid!")
        return False
    else:
        chessboard.turn = temp[1]
    chessboard.castle = temp[2]  #include error check eventually TODO
    chessboard.passant = temp[3] # include error check eventually TODO
    chessboard.half = temp[4] #include error check TODO
    chessboard.whole = int(temp[5]) #include error check TODO

    return (chessboard)



# Inputs a board, and prompts the user for a move.  It checks if the move is legal, makes the move on the board, and returns the updated board.

def request_move(requestboard):

    # Let the player know whose turn it is, and load up a list of pseudo_legal_moves
    if requestboard.turn == 'w':
        moves = pseudo_legal_moves(requestboard)[0]
        print ("--White to Move--")
    else:
        moves = pseudo_legal_moves(requestboard)[1]
        print ("--Black to Move--")

    # Gets a move (or command) from the user and doesn't exit until a legal move has been recieved and updated to the board.
    while True:

        # The user can do many things from here, like request help or request a list of possible moves, but the main goal is to get them to input a move
        user_input = input("Enter your move, or type 'help' for assistance:  ")

        # User requests help
        if user_input == "help":
            print_doc("helptext")

        # User requests the FEN of the current board state.  Kind of redundant now that I always print the FEN above to the board.
        elif user_input == "FEN":
            print("\nCurrent FEN: " + FEN_recover(requestboard))
            print("*****\n")

        # User requests info. Provides information on the versions of engines.  Not terribly useful from this screen
        elif user_input == "info":
            print_doc("info")

        # Exits the user to the main menu.
        elif user_input == "menu":
            confirmation = ""
            while confirmation not in ["y","n"]:
                confirmation = input("About to Abandon Current Game . . . Are you sure? (y/n):")
            if confirmation == "y":
                return ("exit")
            else:
                pass

        # User requests list of possible moves.  Useful for the player to check the formatting of moves
        elif user_input == "moves":
            print("\n" + "*" * 50 + "\nHere is a list of moves for reference.  While all legal moves will be on this list, some moves listed may be illegal.\n")
            print_pretty_moves(moves)
            print("")
            printboard(requestboard)
            print("")

        # If the user attempted to provide a move, we enter here
        else:
            # This converts the move provided to the format the program uses
            player_move = recieve_move(user_input)

            # Check if the provided move is pseudolegal, and then if it is legal.  To check if it is legal, we actually implement the move on a temporary version of the board.
            if player_move in moves and is_legal(move(requestboard, player_move, temp = True), requestboard.turn):
                #implement the move on the board
                move(requestboard, player_move)
                return(requestboard)
            # If the move is either not in the list of pseudolegalmoves or isn't a legal move, we reprompt the user
            else:
                # I log most of the improper inputs in a txt file so I can see where common errors are being made
                log_incorrect_input (user_input, "request_move")
                print("Input Error: Provided Move incorrectly formatted or illegal, please try again")


#Creates a temporary board to make testing manipulations on.  I'm sure a shallow copy would work, but I decided to overkill.
def make_temp_board(input_board):
    temp_board = board(None, None, None, None, None, None)
    temp_board.status = copy.deepcopy(input_board.status)
    temp_board.half = copy.deepcopy(input_board.half)
    temp_board.whole = copy.deepcopy(input_board.whole)
    temp_board.passant = copy.deepcopy(input_board.passant)
    temp_board.castle = copy.deepcopy(input_board.castle)
    temp_board.turn = copy.deepcopy(input_board.turn)
    return (temp_board)


# Implements a move on a board.  Updates all 6 parts of the board as appropriate.
def move(input_moveboard, move, **kwargs):

    # Sometimes we need to make moves on 'temporary' board without affecting the actual gameboard.  This gives us that option
    if "temp" in kwargs and kwargs["temp"] == True:
        moveboard = make_temp_board(input_moveboard)
    else:
        moveboard = input_moveboard

    columns = {'a':'0','b':'1','c':'2','d':'3','e':'4','f':'5','g':'6','h':'7'}
    #Special handling of castling moves.  Hardcoded relocation of the King and the Rook.
    if move == 'w0-0':
        moveboard.status[0][4] = '0'
        moveboard.status[0][5] = 'R'
        moveboard.status[0][6] = 'K'
        moveboard.status[0][7] = '0'
    elif move =='w0-0-0':
        moveboard.status[0][4] = '0'
        moveboard.status[0][3] = 'R'
        moveboard.status[0][2] = 'K'
        moveboard.status[0][0] = '0'
    elif move =='b0-0':
        moveboard.status[7][4] = '0'
        moveboard.status[7][5] = 'r'
        moveboard.status[7][6] = 'k'
        moveboard.status[7][7] = '0'
    elif move =='b0-0-0':
        moveboard.status[7][4] = '0'
        moveboard.status[7][3] = 'r'
        moveboard.status[7][2] = 'k'
        moveboard.status[7][0] = '0'


    # Special handling of En Passant Moves:
    # We check if an en passant is even possible, then we check if the move is trying to capture the enpassantable sqaure.  This guaruntees that an en passant was both attemmpted and legal
    elif moveboard.passant != "-" and move[3] == 'x' and move[4] == columns[moveboard.passant[0]] and move[5] == str(int(moveboard.passant[1])-1):
        #implement the enpassant
        if moveboard.turn == 'w':
            #vacate the capturing pawn's old square
            moveboard.status[int(move[2])][int(move[1])] = '0'
            # remove the enpassanted pawn
            moveboard.status[int(move[5])-1][int(move[4])] = '0'
            # place the pawn in the new square
            moveboard.status[int(move[5])][int(move[4])] = move[0]
        if moveboard.turn == 'b':
            #vacate the capturing pawn's old square
            moveboard.status[int(move[2])][int(move[1])] = '0'
            # remove the enpassanted pawn
            moveboard.status[int(move[5])+1][int(move[4])] = '0'
            # place the pawn in the new square
            moveboard.status[int(move[5])][int(move[4])] = move[0]


    # If the move isn't a castle or an enpassant, then we evaluate as a 'normal' move
    else:
        #move[5]move[4] is the destination sqaure, so we put the piece there
        moveboard.status[int(move[5])][int(move[4])] = move[0]
        # vacate the origin sqaure
        moveboard.status[int(move[2])][int(move[1])] = '0'
        # Final check to see if the move is a pawn promotion and place the new piece (move[6]) there
        if len(move) == 7:
            moveboard.status[int(move[5])][int(move[4])] = move[6]



    # update castling legality.  Basically the first time the King or a rook move, we need to negate the castling rights for that color on the appropriate side.
    if move[0:3] in ['r77','k47']:
        moveboard.castle = moveboard.castle.replace('k','-')
    if move[0:3] in ['r07','k47']:
        moveboard.castle = moveboard.castle.replace('q','-')
    if move[0:3] in ['R70','K40']:
        moveboard.castle = moveboard.castle.replace('K','-')
    if move[0:3] in ['R00','K40']:
        moveboard.castle = moveboard.castle.replace('Q','-')
    # Also update the castling legality if they move itself was a castle
    if move in ["w0-0-0", "w0-0"]:
        moveboard.castle = moveboard.castle.replace('K','-')
        moveboard.castle = moveboard.castle.replace('Q','-')
    elif move in ["b0-0-0", "b0-0"]:
        moveboard.castle = moveboard.castle.replace('k','-')
        moveboard.castle = moveboard.castle.replace('q','-')


    # If a pawn makes a double move to a square adjacent to an enemy pawn, we need to update the en passant status
    #Checks for a white double move
    if move[0] == "P" and move[5] == "3" and move[2] == "1":
        #Checks for an adjacent pawn that could theoretically en passant
        if ((int(move[1])-1 in range(8)) and moveboard.status[3][int(move[1])-1] == "p") or ((int(move[1])+1 in range(8)) and moveboard.status[3][int(move[1])+1] == "p"):
            columns = ['a','b','c','d','e','f','g','h']
            moveboard.passant = columns[int(move[1])] + '3'
    # repeat for black
    elif move[0] == "p" and move[5] == "4" and move[2] =="6":
        if ((int(move[1])-1 in range(8)) and moveboard.status[4][int(move[1])-1] == "P") or ((int(move[1])+1 in range(8)) and moveboard.status[4][int(move[1])+1] == "P"):
            columns = ['a','b','c','d','e','f','g','h']
            moveboard.passant = columns[int(move[1])] + '6'
    # If no enpassant is possible, reset the en passant status
    else: moveboard.passant = "-"

    # adjust the half-turn status.  This counts the number of moves since the last pawn more or capture and is used to declare draws in chess
    if move[0] in ['p',"P"] or move[3] == "x":
        moveboard.half = "-"
    elif moveboard.half == "-":
        moveboard.half = "1"
    else:
        moveboard.half = str(int(moveboard.half) + 1)


    # Switch the turn between white and black.  If black just moves, we also need to increment the whole turn counter
    if moveboard.turn == 'w':
        moveboard.turn = 'b'
    elif moveboard.turn == "b":
        moveboard.whole += 1
        moveboard.turn = 'w'

    #Phew - we're done here and return the new board status
    return(moveboard)


# Inputs a set of moves in my internal format and prints out the list of moves in normalish notation.
def print_pretty_moves(moveset):
    print ("List of Moves: ", end = "")
    movelist = [make_move_pretty(move) for move in moveset]
    print (", ".join(movelist))



# Converts the move as stored by the program to a presentable chess notation that is similar to standard algebraic notation
def make_move_pretty (move):
    # list of columns that I'll index into to conert my numbered columns to lettered columns
    columns = ['a','b','c','d','e','f','g','h']
    # Special handling of castle moves.
    if move in ['w0-0','w0-0-0', 'b0-0', 'b0-0-0']:
        return (move)

    # Most moves are handled here
    else:
        pretty_move = ""
        for i in range(len(move)):
            # replace the column numbers with column letters
            if i in [1,4]:
                pretty_move += columns[int(move[i])]
            # increment the row numbers, because in chess we start counting at 1 and not 0
            elif i in [2,5]:
                pretty_move +=str((int(move[i]) + 1))
            #The other characters can be carried over directly
            else:
                pretty_move += move[i]
        return (pretty_move)


# Converts the user's inputted move into the computer's preferred format.  Basically the inverse of make_move_pretty()
def recieve_move(movestring):
    columns = {'a':'0','b':'1','c':'2','d':'3','e':'4','f':'5','g':'6','h':'7', 'A':'0','B':'1','C':'2','D':'3','E':'4','F':'5','G':'6','H':'7'}
    formatted_move = []
    # Special handling of castling moves
    if movestring in ['w0-0','w0-0-0', 'b0-0', 'b0-0-0']:
        return (movestring)
    #For other moves
    try:
        for i in range(len(movestring)):
            # Replaces column letters with numbers
            if i in [1,4]:
                formatted_move.append((columns[movestring[i]]))
            # Decrements row number
            elif i in [2,5]:
                formatted_move.append(str(int(movestring[i])-1))
            else:
                formatted_move.append(movestring[i])
        return("".join(str(x) for x in formatted_move))
    except:
        return("000000000")





# Requests a FEN from the User
def request_fen():
    while True:
        userinput = input("Please provide a FEN!  Or type 'start' to begin a new game!:  ")
        # if they type start, we provide the fen of a starting board
        if userinput == 'start':
            return ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        elif userinput == "info":
            print_doc("info")
        #chekcs that the provided fen is loadable.  Then returns it!
        elif FENload(userinput) != False:
            return userinput
