from pseudolegalmoves import pseudo_legal_moves
from helpers import move
from islegal import is_legal

#  Imports a board and figures out what the current legal moves are.  Note it will only check moves for the current side
def legal_moves_finder (legaler_board):

    # Figure out the pseudo_legal moves real quick.  TODO- adjust pseudo_legal_moves to accept a side-specific argument so that it returns just the moves for that side.
    if legaler_board.turn == 'w':
        pseudo_moves = pseudo_legal_moves(legaler_board)[0]
    else:
        pseudo_moves = pseudo_legal_moves(legaler_board)[1]

    # For each move, this makes the move on a temporary board, and then checks if the resulting boardstate is legal.  If it is legal then it gets added to the list.
    legaler_moves = [eachmove for eachmove in pseudo_moves if is_legal(move(legaler_board, eachmove, temp = True), mode = "opposite")]

    # Return the list of legal moves
    return(legaler_moves)

