from helpers import move, make_move_pretty
from random import choice
from legal_moves_finder import legal_moves_finder

# Chaosbot is the BOT that makes totally random moves.  It chooses uniformly from a list of all legal moves.
# N.B. Chaosbot tends to move the same piece over and over again - if it has a Queen in the middle of the board that has 25 legal moves, it's much more likely to move that queen than a pawn that only has 1 legal moves
def chaosbot(chaos_board):

    # Acquire a list of legal moves:
    legal_moves = legal_moves_finder(chaos_board)


    # Choose the random move from the list
    chaos_move = choice(legal_moves)
    print (f"ChaosBOT moves: " + make_move_pretty(chaos_move))

    # Implement the move and return the new boardstate
    return (move(chaos_board, chaos_move))