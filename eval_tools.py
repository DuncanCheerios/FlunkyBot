from pseudolegalmoves import pseudo_legal_moves
from helpers import board

#stores the traditional values of each piece.  Negative values 'favor' black and positive 'favor' white.  Kings are stored with dummy placeholder value of 0
values = {"Q":9, "R":5, "B":3, "N":3, "P":1,"q":-9, "r":-5, "b":-3, "n":-3, "p":-1, "K":0, "k":0}

# This maps the difference between attacks/defenders of a piece to the multiplier on its value.  e.g a queen with 1 defenders and 1 attackers (net difference of 0) will have a value multiplier of .7
# Whereas a knight that has 2 more defenders than attacks will have a value of 1.1.  I eyeballed from experience what reasonable values of these might be.
value_weighting = {-10:.1, -9:.1, -8:.1, -7:.1, -6:.1, -5:.1, -4:.1,-3:.1, -2:.2, -1:.3, 0:.7, 1: 1, 2:1.1, 3:1.2, 4:1.3, 5:1.3, 6:1.3, 7:1.3, 8:1.3, 9:1.3, 10:1.3}


# Inputs a board, outputs the relative material count.  Positive favors white, negative favors black.
def mat_count(count_board):
    evaluation = 0
    for row in count_board.status:
        for square in row:
            if square in values:
                evaluation += values[square]
    return (evaluation)



# This is a 'weighted' material count that modifies the value of a piece based on how many times it is attacked/defended.
# The idea is to prevent the BOT from really dumb trades, like sacking a queen to get a rook.  It should 'value' removing the rook at 5, but put the queen into danger should carry a negative value
def weighted_mat_count(count_board):

    # First we need to figure out which squares have material on them and 'count' how many times they are attacked/defended.
    # Fake_board is dummy board which we use to count how many times each square is attacked/defended
    fake_board = board([[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0]], None, None, None, None, None)

    # creates a single set of all pseudolegalmoves on the current board
    temp = pseudo_legal_moves (count_board)
    pseudo_moves = temp[0].union(temp[1])

    # Iterates over all the pseudo legal moves and increments/decrements the 'attack count' that is stored in fake_board
    for move in pseudo_moves:
        # skip castling moves, which don't effect this but mess up the logic
        if move in ["w0-0", "w0-0-0", "b0-0", "b0-0-0"]:
            pass
        elif move[0] in values and move[4].isdigit() and move[5].isdigit():
            # White attackers increment the count, black attackers decrement it
            if move[0].isupper():
                fake_board.status[int(move[5])][int(move[4])] += 1
            else:
                fake_board.status[int(move[5])][int(move[4])] -= 1


    evaluation = 0

    # Now we can go over the actual board, and count the value of the material, using the weight stored in the fakeboard as a multiplier and being very careful with our negative signs
    for row in range (8):               # Iterate over range(8) so that we can easily access both the real board and our 'fake' board
        for square in range(8):
            piece = count_board.status[row][square]
            # For white pieces, we can directly multiply the value of the piece (positive) by the weight (positive) to bump the value up
            if piece in values and piece.isupper():
                evaluation += values[piece] * value_weighting[fake_board.status[row][square]]
            # For black pieces, we
            elif piece in values and piece.islower():
                evaluation += values[piece] * value_weighting[-(fake_board.status[row][square])]
    return (evaluation)