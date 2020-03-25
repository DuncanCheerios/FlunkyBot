from pseudolegalmoves import pseudo_legal_moves

# This is a very wierd function that checks if there is a King in check.  Returns True iff the board state is legal (and the king in question is not in check).

#  The first intended usage is to help determine the legality of moves by seeing if the move would leave the mover's king in check (e.g. If white moving Nf6 would expose the White king to a discovered check).
#  The second usage is to determine if the king is in check for the purposes of evaluating stalemate/checkmate situations

# Required input is a board state.  Optional inputs are a side and a moveset.

# If a side ('w' or 'b') is provided, then the function will return True only if that sides king is in check - this is the intended use of the function.  If no side is provided it will pull the side from the provided boardstate

# If a set of moves is provided, the function will only check to see if any of those moves are attacking the opposite-color king.
# If no move set is provided, the function will generate all pseudo_legal_moves and see if any of them provide check.


def is_legal(legalboard, *s, **kwargs):

    # Error checking:
    if len(s) > 2:
        print ("Error: too many parameters passed to is_legal")

    # Assigning our optional arguments, if any
    side= ""
    moves = set()
    for item in s:
        if item in ['w','b']:
            side = item
        # Sometimes I pass moves as tuple of 2 sets of black and whtite.  Here I combine them
        elif isinstance(item, tuple) and len(item) == 2:
            for everyset in item:
                moves.update(everyset)
        elif isinstance(item, set):
            moves = item

    # if side hasn't been provided, we pull it from the boardstate:
    if side == "":
        # Opposite mode actually flips it around, and checks the king of the opposite side.  Wierd, but occasionally extremely useful
        if "mode" in kwargs and kwargs["mode"] == "opposite":
            if legalboard.turn == 'w':
                side = "b"
            else:
                side = "w"
        else:
            side = legalboard.turn


    # if the moveset was provided, we ensure that there aren't accidentally any moves of the wrong side in the provided set
    if len(moves) != 0:
        if side == 'w':
            moves = {move for move in moves if move[0].islower()}
        if side == 'b':
            moves = {move for move in moves if move[0].isupper()}



    # If side is provided but moveset isn't, we prep the appropriate list of possibilities
    if len(moves) == 0 and side in ['w','b']:
        if side == 'w':
            moves = (pseudo_legal_moves(legalboard))[1]
        elif side == 'b':
            moves = (pseudo_legal_moves(legalboard))[0]

    ## At this point we have a set of moves, called moves, and we need to check if any of them are attacking the opposite color-king.
    for move in moves:
        # if the move is a castle, skip it.  The legality for these is checked in psuedolegalmoves()
        if move in ['w0-0','w0-0-0', 'b0-0', 'b0-0-0']:
            pass
        # If the move is a 'regular' move, check to see if it is attacking the opposite color King.
        elif legalboard.status[int(move[5])][int(move[4])] == 'k' and move[0].isupper():
            return False
        elif legalboard.status[int(move[5])][int(move[4])] == 'K' and move[0].islower():
            return False

    # None of the moves under consideration are attacking the opposite King!  Assuming we passed a smart set of moves to the function, this means the board state is legal!
    return True
