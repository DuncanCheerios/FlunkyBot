from helpers import move, make_move_pretty
from random import choice
from legal_moves_finder import legal_moves_finder
from eval_tools import mat_count, weighted_mat_count
from islegal import is_legal



# Flunkybot is the function that governs the chess engine logic of flunkybot.

# flunkybot is called with a boardstate and an optional argument of the version of flunkyBOT that is intended to be used.  flunkybot() makes a move an returns an updated board.
def flunkybot(flunky_board, **kwargs):

    # Determine the version of flunkybot to use.
    if "version" in kwargs:
        version = kwargs["version"]
    else:
        # I want this to default to the latest version of flunkybot.  No way in heck I remember to update this - TODO find a better solution
        version = 1.1


    # This uses the evaluation system that lines up with the required version of flunkybot.  This section has some terrible design because
    # I changed some of the basic logic of my evaluation while iterating flunkybot, but I still wanted each version of flunkybot to be present here.
    if version == 1.0:

        # Acquire a list of legal moves
        legal_moves = legal_moves_finder(flunky_board)

        # Determine an evaluation for each move by putting it into a dict

        move_dict = {each_move:flunky1_eval(move(flunky_board, each_move, temp = True)) for each_move in legal_moves}

        #figure out the best evaluation
        if flunky_board.turn == 'w':
            best_eval = max(move_dict, key=move_dict.get)
        else:
            best_eval = min(move_dict, key=move_dict.get)

        candidate_moves = [move for move in move_dict if move_dict[move] == move_dict[best_eval]]
        flunky_move = choice(candidate_moves)

    # Version 1.1
    elif version == 1.1:

        legal_moves = legal_moves_finder(flunky_board)

        # This move list stores a bunch of tuples containing the move and the evaluation of the move
        move_list = [(each_move, flunky1_1_eval(move(flunky_board, each_move, temp = True))) for each_move in legal_moves]

        move_list.sort(key=lambda x:x[1])

        # Grabs the best move.  Which is the first move for white and the last move for black
        if flunky_board.turn == 'w':
            best_eval = move_list[-1][1]
        else:
            best_eval = move_list[0][1]

        candidate_moves = [eachmove for eachmove in move_list if eachmove[1]==best_eval]

        flunky_move = choice(candidate_moves)
        flunky_move = flunky_move[0]

    # Version 1.2
    elif version == 1.2:

        legal_moves = legal_moves_finder(flunky_board)

        # This move list stores a bunch of tuples containing the move and the evaluation of the move
        move_list = [(each_move, flunky1_2_eval(move(flunky_board, each_move, temp = True))) for each_move in legal_moves]

        move_list.sort(key=lambda x:x[1])

        # Grabs the best move.  Which is the first move for white and the last move for black
        if flunky_board.turn == 'w':
            best_eval = move_list[-1][1]
        else:
            best_eval = move_list[0][1]

        candidate_moves = [eachmove for eachmove in move_list if eachmove[1]==best_eval]

        flunky_move = choice(candidate_moves)
        flunky_move = flunky_move[0]

    # If for some reason a nonexistant version of flunkybot is being called
    else:
        print ("THat version of flunkybot doesn't exist.  ERROR in flunkybot()")
        return False

    #Print the move:
    print (f"FlunkyBOT moves: " + make_move_pretty(flunky_move))

    #Make the move and implement the change in the FEN
    move(flunky_board, flunky_move)
    return (flunky_board)





# Version 1.0 Evaluates a board state without 'looking' ahead at all.  A positive result is white-favored, negative is black favored.
def flunky1_eval(eval_board):
    return mat_count(eval_board)


# Version 1.1 reorganizes a bit and learns to avoid stalemate and to prize a checkmate
def flunky1_1_eval(eval_board):

    evaluation = 0

    #moves is the list of moves availble to the other side after flunkybot makes its proposed move.
    eval_moves = legal_moves_finder(eval_board)

    evaluation = mat_count(eval_board)


    #stalemate/checkmate detector
    if len(eval_moves) == 0:
        #checkmate condition
        if not is_legal(eval_board, eval_board.turn):
            if eval_board.turn == "w":
                evaluation = -100000
            else:
                evaluation = 100000
        # Stalemate condition.  I simply multiply by -1 because flunky should value stalemates when it's behind and avoid them when ahead.
        else:
            evaluation *= -1

    return evaluation



# Version 1.2 reorganizes a bit and learns to avoid stalemate and to prize a checkmate
def flunky1_2_eval(eval_board):

    evaluation = 0

    #moves is the list of moves availble to the other side after flunkybot makes its proposed move.
    eval_moves = legal_moves_finder(eval_board)

    evaluation = weighted_mat_count(eval_board)


    #stalemate/checkmate detector
    if len(eval_moves) == 0:
        #checkmate condition
        if not is_legal(eval_board, eval_board.turn):
            if eval_board.turn == "w":
                evaluation = -100000
            else:
                evaluation = 100000
        # Stalemate condition.  I simply multiply by -1 because flunky should value stalemates when it's behind and avoid them when ahead.
        else:
            evaluation *= -1

    return evaluation





