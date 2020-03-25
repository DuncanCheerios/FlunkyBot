# Please don't look at this - it's truly awful.  It was one of the first things I wrote for this project, and I just needed somewhere I could get the ball rolling a bit.


# pseudo_legal_moves inputs a board and outputs two sets, one of all of white's pseudo-legal-moves and one of blacks pseudo-legal-moves

# There are two reasons these moves may not be legal:  They may leave one's own king in check, and moves that 'capture' a king will also be listed.
# These 'illegal' moves are left in here deliberately - it is extremely useful to be able to detect checks and checkmates to have a list of moves that might include king-captures.


def pseudo_legal_moves(pseudoboard):
    white_pseudo_legal_moves = set()
    black_pseudo_legal_moves = set()

    #Iterate over all the rows and the squares of those rows to detect each piece
    for row in range(8):
        for square in range(8):

            # White King Logic
            if pseudoboard.status[row][square] == "K":
                for i in [-1,0,1]:
                    for j in [-1,0,1]:
                        if row + i in list(range(8)) and square+j in list(range(8)):
                            #Move logic
                            if pseudoboard.status[row + i][square+j].islower() or pseudoboard.status[row + i][square+j] =='0':
                                white_pseudo_legal_moves.add(f"K{square}{row}-{square+j}{row+i}")
                            #Capture logic
                            elif pseudoboard.status[row+i][square+j] in ['b','q','r','n','p','k']:
                                white_pseudo_legal_moves.add(f"K{square}{row}x{square+j}{row+i}")

            # Black King Logic
            elif pseudoboard.status[row][square] == "k":
                for i in [-1,0,1]:
                    for j in [-1,0,1]:
                        if row + i in list(range(8)) and square+j in list(range(8)):
                            if pseudoboard.status[row + i][square+j].isupper() or pseudoboard.status[row + i][square+j] =='0':
                                black_pseudo_legal_moves.add(f"k{square}{row}-{square+j}{row+i}")
                            elif pseudoboard.status[row+i][square+j] in ['B','Q','R','N','P','K']:
                                black_pseudo_legal_moves.add(f"k{square}{row}x{square+j}{row+i}")

            # White pawn logic
            elif pseudoboard.status[row][square] == "P":
                #First we do the pawn movement logic, then the pawn capture logic

                # If pawn on original row, check if it can move 1 and then 2 squares
                if row == 1:
                    if pseudoboard.status[row+1][square] == '0':
                        white_pseudo_legal_moves.add(f"P{square}{row}-{square}{row+1}")
                        if pseudoboard.status[row+2][square] == '0':
                            white_pseudo_legal_moves.add(f"P{square}{row}-{square}{row+2}")
                # if pawn in middle of pseudoboard, check if it can move 1 square
                elif row in list(range(2,6)):
                    if pseudoboard.status[row+1][square] == '0':
                        white_pseudo_legal_moves.add(f"P{square}{row}-{square}{row+1}")
                # check if pawn can promote
                elif row == 6 and pseudoboard.status[7][square]=='0':
                    for promotions in ['N',"R","B","Q"]:
                        white_pseudo_legal_moves.add(f"P{square}{row}-{square}{row+1}{promotions}")

                # Pawn capture logic
                for i in [-1,1]:
                    # Considers all captures that aren't also promotions
                    if row+1 in range(7) and square + i in range(8) and pseudoboard.status[row+1][square+i] in ['b','q','r','n','p', 'k']:
                        white_pseudo_legal_moves.add(f"P{square}{row}x{square+i}{row+1}")
                    # Considers all captures that are also promotions
                    if row+1 == 7 and square + i in range(8) and pseudoboard.status[row+1][square+i] in ['b','q','r','n','p', 'k']:
                        for promotions in ['N',"R","B","Q"]:
                            white_pseudo_legal_moves.add(f"P{square}{row}x{square+i}{row+1}{promotions}")

            # Black pawn logic
            elif pseudoboard.status[row][square] == "p":
                # If pawn on original row, check if it can move 1 and then 2 squares
                if row == 6:
                    if pseudoboard.status[row-1][square] == '0':
                        black_pseudo_legal_moves.add(f"p{square}{row}-{square}{row-1}")
                        if pseudoboard.status[row-2][square] == '0':
                            black_pseudo_legal_moves.add(f"p{square}{row}-{square}{row-2}")
                # if pawn in middle of pseudoboard, check if it can move 1 square
                elif row in list(range(2,6)):
                    if pseudoboard.status[row-1][square] == '0':
                        black_pseudo_legal_moves.add(f"p{square}{row}-{square}{row-1}")
                # check if pawn can promote
                elif row == 1 and pseudoboard.status[0][square]=='0':
                    for promotions in ['n',"r","b","q"]:
                        black_pseudo_legal_moves.add(f"p{square}{row}-{square}{row-1}{promotions}")

                # Pawn capture logic
                for i in [-1,1]:
                    # Considers all captures that aren't also promotions
                    if row-1 in range(1,7) and square + i in range(8) and pseudoboard.status[row-1][square+i] in ['B','Q','R','N','P','K']:
                        black_pseudo_legal_moves.add(f"p{square}{row}x{square+i}{row-1}")
                    # Considers all captures that are also promotions
                    if row-1 ==0 and square + i in range(8) and pseudoboard.status[row-1][square+i] in ['B','Q','R','N','P','K']:
                        for promotions in ['n',"r","b","q"]:
                            black_pseudo_legal_moves.add(f"p{square}{row}x{square+i}{row-1}{promotions}")


            # Rook Logic for White:
            elif pseudoboard.status[row][square] == "R":
                #moving/capturing to the right
                i=1
                while square + i in range(8) and pseudoboard.status[row][square + i] == '0':
                    white_pseudo_legal_moves.add(f"R{square}{row}-{square+i}{row}")
                    i +=1
                if square + i in range(8) and pseudoboard.status[row][square + i] in ['b','q','r','n','p','k']:
                    white_pseudo_legal_moves.add(f"R{square}{row}x{square+i}{row}")

                #moving/capturing to the left
                i=1
                while square - i in range(8) and pseudoboard.status[row][square - i] == '0':
                    white_pseudo_legal_moves.add(f"R{square}{row}-{square-i}{row}")
                    i +=1
                if square - i in range(8) and pseudoboard.status[row][square - i] in ['b','q','r','n','p','k']:
                    white_pseudo_legal_moves.add(f"R{square}{row}x{square-i}{row}")

                #moving/capturing up
                i=1
                while row + i in range(8) and pseudoboard.status[row+i][square] == '0':
                    white_pseudo_legal_moves.add(f"R{square}{row}-{square}{row+i}")
                    i +=1
                if row + i in range(8) and pseudoboard.status[row + i][square] in ['b','q','r','n','p','k']:
                    white_pseudo_legal_moves.add(f"R{square}{row}x{square}{row+i}")

                #moving/capturing down
                i=1
                while row - i in range(8) and pseudoboard.status[row-i][square] == '0':
                    white_pseudo_legal_moves.add(f"R{square}{row}-{square}{row-i}")
                    i +=1
                if row - i in range(8) and pseudoboard.status[row - i][square] in ['b','q','r','n','p','k']:
                    white_pseudo_legal_moves.add(f"R{square}{row}x{square}{row-i}")

            # Rook Logic for Black:
            elif pseudoboard.status[row][square] == "r":

                i=1
                while square + i in range(8) and pseudoboard.status[row][square + i] == '0':
                    black_pseudo_legal_moves.add(f"r{square}{row}-{square+i}{row}")
                    i +=1
                if square + i in range(8) and pseudoboard.status[row][square + i] in ['B','Q','R','N','P','K']:
                    black_pseudo_legal_moves.add(f"r{square}{row}x{square+i}{row}")


                i=1
                while square - i in range(8) and pseudoboard.status[row][square - i] == '0':
                    black_pseudo_legal_moves.add(f"r{square}{row}-{square-i}{row}")
                    i +=1
                if square - i in range(8) and pseudoboard.status[row][square - i] in ['B','Q','R','N','P','K']:
                    black_pseudo_legal_moves.add(f"r{square}{row}x{square-i}{row}")


                i=1
                while row + i in range(8) and pseudoboard.status[row+i][square] == '0':
                    black_pseudo_legal_moves.add(f"r{square}{row}-{square}{row+i}")
                    i +=1
                if row + i in range(8) and pseudoboard.status[row + i][square] in ['B','Q','R','N','P','K']:
                    black_pseudo_legal_moves.add(f"r{square}{row}x{square}{row+i}")


                i=1
                while row - i in range(8) and pseudoboard.status[row-i][square] == '0':
                    black_pseudo_legal_moves.add(f"r{square}{row}-{square}{row-i}")
                    i +=1
                if row - i in range(8) and pseudoboard.status[row - i][square] in ['B','Q','R','N','P','K']:
                    black_pseudo_legal_moves.add(f"r{square}{row}x{square}{row-i}")

            #White Bishop Logic

            elif pseudoboard.status[row][square] == "B":

                i=1
                while square + i in range(8) and row + i in range(8) and pseudoboard.status[row+i][square + i] == '0':
                    white_pseudo_legal_moves.add(f"B{square}{row}-{square+i}{row+i}")
                    i +=1
                if square + i in range(8) and row + i in range(8) and pseudoboard.status[row+i][square + i] in ['b','q','r','n','p','k']:
                    white_pseudo_legal_moves.add(f"B{square}{row}x{square+i}{row+i}")


                i=1
                while square + i in range(8) and row - i in range(8) and pseudoboard.status[row-i][square + i] == '0':
                    white_pseudo_legal_moves.add(f"B{square}{row}-{square+i}{row-i}")
                    i +=1
                if square + i in range(8) and row - i in range(8) and pseudoboard.status[row-i][square + i] in ['b','q','r','n','p','k']:
                    white_pseudo_legal_moves.add(f"B{square}{row}x{square+i}{row-i}")


                i=1
                while square - i in range(8) and row + i in range(8) and pseudoboard.status[row+i][square - i] == '0':
                    white_pseudo_legal_moves.add(f"B{square}{row}-{square-i}{row+i}")
                    i +=1
                if square - i in range(8) and row + i in range(8) and pseudoboard.status[row+i][square - i] in ['b','q','r','n','p','k']:
                    white_pseudo_legal_moves.add(f"B{square}{row}x{square-i}{row+i}")


                i=1
                while square - i in range(8) and row - i in range(8) and pseudoboard.status[row-i][square - i] == '0':
                    white_pseudo_legal_moves.add(f"B{square}{row}-{square-i}{row-i}")
                    i +=1
                if square - i in range(8) and row - i in range(8) and pseudoboard.status[row-i][square - i] in ['b','q','r','n','p','k']:
                    white_pseudo_legal_moves.add(f"B{square}{row}x{square-i}{row-i}")

            # Black Bishop Logic

            elif pseudoboard.status[row][square] == "b":

                i=1
                while square + i in range(8) and row + i in range(8) and pseudoboard.status[row+i][square + i] == '0':
                    black_pseudo_legal_moves.add(f"b{square}{row}-{square+i}{row+i}")
                    i +=1
                if square + i in range(8) and row + i in range(8) and pseudoboard.status[row+i][square + i] in ['B','Q','R','N','P','K']:
                    black_pseudo_legal_moves.add(f"b{square}{row}x{square+i}{row+i}")


                i=1
                while square + i in range(8) and row - i in range(8) and pseudoboard.status[row-i][square + i] == '0':
                    black_pseudo_legal_moves.add(f"b{square}{row}-{square+i}{row-i}")
                    i +=1
                if square + i in range(8) and row - i in range(8) and pseudoboard.status[row-i][square + i] in ['B','Q','R','N','P','K']:
                    black_pseudo_legal_moves.add(f"b{square}{row}x{square+i}{row-i}")


                i=1
                while square - i in range(8) and row + i in range(8) and pseudoboard.status[row+i][square - i] == '0':
                    black_pseudo_legal_moves.add(f"b{square}{row}-{square-i}{row+i}")
                    i +=1
                if square - i in range(8) and row + i in range(8) and pseudoboard.status[row+i][square - i] in ['B','Q','R','N','P','K']:
                    black_pseudo_legal_moves.add(f"b{square}{row}x{square-i}{row+i}")


                i=1
                while square - i in range(8) and row - i in range(8) and pseudoboard.status[row-i][square - i] == '0':
                    black_pseudo_legal_moves.add(f"b{square}{row}-{square-i}{row-i}")
                    i +=1
                if square - i in range(8) and row - i in range(8) and pseudoboard.status[row-i][square - i] in ['B','Q','R','N','P','K']:
                    black_pseudo_legal_moves.add(f"b{square}{row}x{square-i}{row-i}")

            # White Queen Logic

            elif pseudoboard.status[row][square] == "Q":

                i=1
                while square + i in range(8) and row + i in range(8) and pseudoboard.status[row+i][square + i] == '0':
                    white_pseudo_legal_moves.add(f"Q{square}{row}-{square+i}{row+i}")
                    i +=1
                if square + i in range(8) and row + i in range(8) and pseudoboard.status[row+i][square + i] in ['b','q','r','n','p','k']:
                    white_pseudo_legal_moves.add(f"Q{square}{row}x{square+i}{row+i}")


                i=1
                while square + i in range(8) and row - i in range(8) and pseudoboard.status[row-i][square + i] == '0':
                    white_pseudo_legal_moves.add(f"Q{square}{row}-{square+i}{row-i}")
                    i +=1
                if square + i in range(8) and row - i in range(8) and pseudoboard.status[row-i][square + i] in ['b','q','r','n','p','k']:
                    white_pseudo_legal_moves.add(f"Q{square}{row}x{square+i}{row-i}")


                i=1
                while square - i in range(8) and row + i in range(8) and pseudoboard.status[row+i][square - i] == '0':
                    white_pseudo_legal_moves.add(f"Q{square}{row}-{square-i}{row+i}")
                    i +=1
                if square - i in range(8) and row + i in range(8) and pseudoboard.status[row+i][square - i] in ['b','q','r','n','p','k']:
                    white_pseudo_legal_moves.add(f"Q{square}{row}x{square-i}{row+i}")


                i=1
                while square - i in range(8) and row - i in range(8) and pseudoboard.status[row-i][square - i] == '0':
                    white_pseudo_legal_moves.add(f"Q{square}{row}-{square-i}{row-i}")
                    i +=1
                if square - i in range(8) and row - i in range(8) and pseudoboard.status[row-i][square - i] in ['b','q','r','n','p','k']:
                    white_pseudo_legal_moves.add(f"Q{square}{row}x{square-i}{row-i}")

                i=1
                while square + i in range(8) and pseudoboard.status[row][square + i] == '0':
                    white_pseudo_legal_moves.add(f"Q{square}{row}-{square+i}{row}")
                    i +=1
                if square + i in range(8) and pseudoboard.status[row][square + i] in ['b','q','r','n','p','k']:
                    white_pseudo_legal_moves.add(f"Q{square}{row}x{square+i}{row}")


                i=1
                while square - i in range(8) and pseudoboard.status[row][square - i] == '0':
                    white_pseudo_legal_moves.add(f"Q{square}{row}-{square-i}{row}")
                    i +=1
                if square - i in range(8) and pseudoboard.status[row][square - i] in ['b','q','r','n','p','k']:
                    white_pseudo_legal_moves.add(f"Q{square}{row}x{square-i}{row}")


                i=1
                while row + i in range(8) and pseudoboard.status[row+i][square] == '0':
                    white_pseudo_legal_moves.add(f"Q{square}{row}-{square}{row+i}")
                    i +=1
                if row + i in range(8) and pseudoboard.status[row + i][square] in ['b','q','r','n','p','k']:
                    white_pseudo_legal_moves.add(f"Q{square}{row}x{square}{row+i}")


                i=1
                while row - i in range(8) and pseudoboard.status[row-i][square] == '0':
                    white_pseudo_legal_moves.add(f"Q{square}{row}-{square}{row-i}")
                    i +=1
                if row - i in range(8) and pseudoboard.status[row - i][square] in ['b','q','r','n','p','k']:
                    white_pseudo_legal_moves.add(f"Q{square}{row}x{square}{row-i}")


            # Black Queen Logic

            elif pseudoboard.status[row][square] == "q":

                i=1
                while square + i in range(8) and row + i in range(8) and pseudoboard.status[row+i][square + i] == '0':
                    black_pseudo_legal_moves.add(f"q{square}{row}-{square+i}{row+i}")
                    i +=1
                if square + i in range(8) and row + i in range(8) and pseudoboard.status[row+i][square + i] in ['B','Q','R','N','P','K']:
                    black_pseudo_legal_moves.add(f"q{square}{row}x{square+i}{row+i}")


                i=1
                while square + i in range(8) and row - i in range(8) and pseudoboard.status[row-i][square + i] == '0':
                    black_pseudo_legal_moves.add(f"q{square}{row}-{square+i}{row-i}")
                    i +=1
                if square + i in range(8) and row - i in range(8) and pseudoboard.status[row-i][square + i] in ['B','Q','R','N','P','K']:
                    black_pseudo_legal_moves.add(f"q{square}{row}x{square+i}{row-i}")


                i=1
                while square - i in range(8) and row + i in range(8) and pseudoboard.status[row+i][square - i] == '0':
                    black_pseudo_legal_moves.add(f"q{square}{row}-{square-i}{row+i}")
                    i +=1
                if square - i in range(8) and row + i in range(8) and pseudoboard.status[row+i][square - i] in ['B','Q','R','N','P','K']:
                    black_pseudo_legal_moves.add(f"q{square}{row}x{square-i}{row+i}")


                i=1
                while square - i in range(8) and row - i in range(8) and pseudoboard.status[row-i][square - i] == '0':
                    black_pseudo_legal_moves.add(f"q{square}{row}-{square-i}{row-i}")
                    i +=1
                if square - i in range(8) and row - i in range(8) and pseudoboard.status[row-i][square - i] in ['B','Q','R','N','P','K']:
                    black_pseudo_legal_moves.add(f"q{square}{row}x{square-i}{row-i}")

                i=1
                while square + i in range(8) and pseudoboard.status[row][square + i] == '0':
                    black_pseudo_legal_moves.add(f"q{square}{row}-{square+i}{row}")
                    i +=1
                if square + i in range(8) and pseudoboard.status[row][square + i] in ['B','Q','R','N','P','K']:
                    black_pseudo_legal_moves.add(f"q{square}{row}x{square+i}{row}")


                i=1
                while square - i in range(8) and pseudoboard.status[row][square - i] == '0':
                    black_pseudo_legal_moves.add(f"q{square}{row}-{square-i}{row}")
                    i +=1
                if square - i in range(8) and pseudoboard.status[row][square - i] in ['B','Q','R','N','P','K']:
                    black_pseudo_legal_moves.add(f"q{square}{row}x{square-i}{row}")


                i=1
                while row + i in range(8) and pseudoboard.status[row+i][square] == '0':
                    black_pseudo_legal_moves.add(f"q{square}{row}-{square}{row+i}")
                    i +=1
                if row + i in range(8) and pseudoboard.status[row + i][square] in ['B','Q','R','N','P','K']:
                    black_pseudo_legal_moves.add(f"q{square}{row}x{square}{row+i}")


                i=1
                while row - i in range(8) and pseudoboard.status[row-i][square] == '0':
                    black_pseudo_legal_moves.add(f"q{square}{row}-{square}{row-i}")
                    i +=1
                if row - i in range(8) and pseudoboard.status[row - i][square] in ['B','Q','R','N','P','K']:
                    black_pseudo_legal_moves.add(f"q{square}{row}x{square}{row-i}")


            # White Knight Logic
            elif pseudoboard.status[row][square] == "N":
                for i in [-2,2]:
                    for j in [-1,1]:
                        if row + i in range(8) and square + j in range(8):
                            if pseudoboard.status[row+i][square+j] == '0':
                                white_pseudo_legal_moves.add(f"N{square}{row}-{square+j}{row+i}")
                            elif pseudoboard.status[row+i][square+j] in ['b','q','r','n','p','k']:
                                white_pseudo_legal_moves.add(f"N{square}{row}x{square+j}{row+i}")
                        if square + i in range(8) and row + j in range(8):
                            if pseudoboard.status[row+j][square+i] == '0':
                                white_pseudo_legal_moves.add(f"N{square}{row}-{square+i}{row+j}")
                            elif pseudoboard.status[row+j][square+i] in ['b','q','r','n','p','k']:
                                white_pseudo_legal_moves.add(f"N{square}{row}x{square+i}{row+j}")

            # Black Knight Board Logic
            elif pseudoboard.status[row][square] == "n":
                for i in [-2,2]:
                    for j in [-1,1]:
                        if row + i in range(8) and square + j in range(8):
                            if pseudoboard.status[row+i][square+j] == '0':
                                black_pseudo_legal_moves.add(f"n{square}{row}-{square+j}{row+i}")
                            elif pseudoboard.status[row+i][square+j] in ['B','Q','R','N','P','K']:
                                black_pseudo_legal_moves.add(f"n{square}{row}x{square+j}{row+i}")
                        if square + i in range(8) and row + j in range(8):
                            if pseudoboard.status[row+j][square+i] == '0':
                                black_pseudo_legal_moves.add(f"n{square}{row}-{square+i}{row+j}")
                            elif pseudoboard.status[row+j][square+i] in ['B','Q','R','N','P','K']:
                                black_pseudo_legal_moves.add(f"n{square}{row}x{square+i}{row+j}")


    # Handling of Castling logic.  We need to check a couple things to see if castling is pseudo legal.  Have the King or rook moved at any point in the game so far?
    # Is the king currently in check?  Are the spaces betweent the rook and king clear?  Will the king travel through a threatened square?

    #White's King-Side Castle

    #pseudoboard.castle guaruntees that the King/Rook are still eligible, the second part guaruntees the squares between are empty.
    if "K" in pseudoboard.castle and pseudoboard.status[0][5] == '0' and pseudoboard.status[0][6] =='0':
        #This conditional checks if the king is currently in check or if any of the squares it will travel through are attacked
        for move in black_pseudo_legal_moves:
            if move[4:6] in ['40','50','60']:
                break
        else:
            white_pseudo_legal_moves.add(f"w0-0")

    # White Queen-side Castle
    if "Q" in pseudoboard.castle and pseudoboard.status[0][3] == '0' and pseudoboard.status[0][2] =='0' and pseudoboard.status[0][1]:
        #This conditional checks if the king is currently in check or if any of the squares it will travel through are attacked
        for move in black_pseudo_legal_moves:
            if move[4:6] in ['40','30','20']:
                break
        else:
            white_pseudo_legal_moves.add(f"w0-0-0")

    #Black King's side castle
    if "k" in pseudoboard.castle and pseudoboard.status[7][5] == '0' and pseudoboard.status[7][6] =='0':
        #This conditional checks if the king is currently in check or if any of the squares it will travel through are attacked
        for move in white_pseudo_legal_moves:
            if move[4:6] in ['47','57','67']:
                break
        else:
            black_pseudo_legal_moves.add(f"b0-0")

    # White Queen-side Castle
    if "q" in pseudoboard.castle and pseudoboard.status[7][3] == '0' and pseudoboard.status[7][2] =='0' and pseudoboard.status[7][1]:
        #This conditional checks if the king is currently in check or if any of the squares it will travel through are attacked
        for move in white_pseudo_legal_moves:
            if move[4:6] in ['47','37','27']:
                break
        else:
            black_pseudo_legal_moves.add(f"b0-0-0")




    # EnPassant Logic. Fortunately pseudoboard.fen stores if a square is 'enpassantable', ie a pawn just double-moved past this square.  As long as move() handles updating pseudoboard.passant, the following works fine

    if pseudoboard.passant != "-":
        # we need to convert the passant square stored in the FEN to something understandable:
        columns = {'a':'0','b':'1','c':'2','d':'3','e':'4','f':'5','g':'6','h':'7'}
        passant_square = [int(pseudoboard.passant[1])-1, int(columns[pseudoboard.passant[0]])]
        #For Black enpassanting white
        if passant_square[0] == 2:
            if passant_square[1] + 1 in range(8) and pseudoboard.status[3][passant_square[1]+1] == 'p':
                black_pseudo_legal_moves.add(f"p{passant_square[1]+1}{3}x{passant_square[1]}{2}")
            if passant_square[1] - 1 in range(8) and pseudoboard.status[3][passant_square[1]-1] == 'p':
                black_pseudo_legal_moves.add(f"p{passant_square[1]-1}{3}x{passant_square[1]}{2}")
        #White enpassanting black
        if passant_square[0] == 5:
            if passant_square[1]+1 in range(8) and pseudoboard.status[4][passant_square[1]+1] == 'P':
                white_pseudo_legal_moves.add(f"P{passant_square[1]+1}{4}x{passant_square[1]}{5}")
            if passant_square[1]-1 in range(8) and pseudoboard.status[4][passant_square[1]-1] == 'P':
                white_pseudo_legal_moves.add(f"P{passant_square[1]-1}{4}x{passant_square[1]}{5}")


    # Finally we return both sets of moves
    return(white_pseudo_legal_moves, black_pseudo_legal_moves)