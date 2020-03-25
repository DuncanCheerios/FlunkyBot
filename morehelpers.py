from time import sleep
from random import normalvariate, triangular, random
from sty import bg, fg, ef, rs

# MOre useful functions are stored here


# This prints the current board state.  It started as just an array of characters - 0's for blank squares, uppercase letters for white pieces, lowercase for black.  Then it grew and grew
# over time.  Now it actually looks like a real board!  The color scheme is horrifying, but the unicode pieces don't show up too well on dark/light square colors, so I made do with this monstrosity of brown and green.
def printboard(printingboard):

    #temp is what we'll call the status of the board which contains the actual locations of the pieces
    temp = printingboard.status

    # Prep some useful values.
    rowcount = 8    # I'll iterate backwards over the rows

    # Useful mapping of the characters.  Some redundancy in here because I kept changing my mind about how to do this and might change it again.  The unicode chess pieces aren't great,
    # so I'm currently mapping the white pieces to the black pieces then recoloring them to white.
    unicode_map = {'0': 0x0020, 'k':0x265A, 'q':0x265B, 'r':0x265C, 'b':0x265D, 'n':0x265E, 'p':0x265F, 'K':0x265A, 'Q':0x265B, 'R':0x265C, 'B':0x265D, 'N':0x265E, 'P':0x265F}

    # The colors for the squares. A lightish green for white and a brown for black
    square_color_map = {True: (0,190,100), False:(168,98,28)}

    # The colors for the pieces.  Off-white and black
    piece_color_map = {True: (225, 255, 225), False: (0,0,0)}

    # parity will track whether the square being printed should have a dark or light background.  True corresponds to light square.  False corresponds to dark square.
    parity = True

    # We iterate backwards over the rows of the chessboard to print each in turn
    for row in range(len(temp)):
        # The label of the row
        print (f"{rowcount} ", end= "")

        #The actual squares of the board, with 'parity' tracking the light/darkness of squares
        for character in temp[7-row]:
            # Quickly figure out if it is a white or black piece so we can pring the appropriate color
            color = True
            if character != '0'and character.islower():
                color = False
            # I'm pretty proud of the * to unpack a tuple into a list of arguments.  This prints the actual squares of the board
            print (bg(*square_color_map[parity]) + fg(*piece_color_map[color]) + "{:{width}}".format(chr(unicode_map[character]), width = 2) + bg.rs + fg.rs, end = "")

            parity = not parity

        print ("")

        # We need to flip the parity to prep for the next row and decrement the rowcount
        parity =not parity
        rowcount -= 1


    # Print the labels of the colums.  The unicode squares and pieces have wierd widths, so I couldn't quite align the letters with the columns.  The missing space between D and E kind of accounts for that
    print (chr(0x2005) + chr(0x200A) + "A B C DE F G H")

    return True




# This function recovers the FEN from board status section
def FEN_recover (fen_board):
    # Start with an empty string for the fen
    fen = ""

    # Convert my board state to the FEN version by iterating over the squares of my digital board.  The only trick here is replacing consecutive 0's with integers
    for row in range(8):
        temp = "".join(fen_board.status[7-row])
        i=0
        while i<8:
            if fen_board.status[7-row][i] != "0":
                fen += fen_board.status[7-row][i]
                i += 1
            else:
                number = 0
                while i<8 and fen_board.status[7-row][i] == "0":
                    number +=1
                    i+=1
                else:
                    fen += str(number)
        fen += "/"

    # load up the other components of the FEN.  Note that I need a bit of logic to convert how I store castling rights back to a standard FEN notation.
    fen += (f" {fen_board.turn} ")

    # Load up the castling rights. . .
    if fen_board.castle == "----":
        fen += "-"
    else:
        for char in fen_board.castle:
            if char != "-":
                fen += char

    # these elements of the FEN are stored identically in my board class, so they load directly.
    fen += (f" {fen_board.passant}")
    fen += (f" {fen_board.half}")
    fen += (f" {fen_board.whole}")

    #return the FEN
    return (fen.rstrip('/'))


# Useful little function for printing a txt document line-by-line with a little bit of delay, to provide a nice scrolling effect.
#  I handle a lot of menus and info screens as text docs, so this gets a bit of use
def print_doc(document):
    file = open(f"{document}.txt", "r")
    lines = file.read().split("\n")
    for line in lines:
            print (line)
            sleep(.1)

# This is the opening crawl and fake loading screen for FlunkyBOT.  Functionally valueless, but fun to work on when I was burned out on the hard stuff.
# The random sleep times are interjected to create the illusion of an old system struggling to load a program.
def opening():
    # Prints a row of decorative characters
    for i in range(100):
        print(chr(0x2042), end = "", flush = True)
        sleep(triangular(0,.02,.005))
    print("")

    # These are all extremely important systems that need to be initialized.  Absolutely crucial.
    for very_important_and_real_system in ["Primary Cores Engaging", "Circulating SuperCoolant", "Priming Neural Nodes"]:
        print ("\n---" + very_important_and_real_system + "----")
        for i in range(25):
            sleep(triangular(0,.15,.05))
            print(chr(0x220E), end = "", flush = True)
        print ("--------100%\n")

    # Prints the Titlecard stored in a txt file.  A lot of effort was put in to make this scroll look appropriately janky  TODO - add more jankiness. Some miscolored letters would be neat
    file = open("Titlecard.txt", "r")
    for row in file:
        for letter in row:
            if letter == "\n":
                x = -1
                while x < 0:
                  x = normalvariate(.1,.15)
                sleep(x)
                print (letter, end = "", flush = True)
            else:
                print(letter, end="", flush = True)
    print ("")


# Prompts the user to decide who is going to play a given side.  List of users may expand as my chess engine iterates
def recieve_player(color):
    user_input = ""
    while user_input not in ["human", "chaosbot", "flunkybotv1.0", "flunkybotv1.1", "flunkybotv1.2", "flunkybot"]:
        # This logs incorrect inputs to a text file so that I can increase useability
        if user_input != "":
            log_incorrect_input(user_input, "recieve_player")
        # Ask the user who is playing a given side
        user_input = input(f"Who is playing {color}? Options are 'human', 'chaosbot', or 'flunkybot'")
    # if they type flunkybot, we assume they want the most recent model.  Not great design, because I have to remember to update the model here, but it works for now
    if user_input == "flunkybot":
        return ("flunkybotv1.2")
    return user_input


# Just some decorative text for the bots to print so it's clear when they are thinking
def prepturn(robot):
    text = " preparing to move: . . . ."
    print (f"{robot}", end = "")
    for char in text:
        print (char, flush = True, end= "")
    print("")


#prints a little scoreboard.  Scores is assumed to be a dict with keys of the names of the team and values of how many points they have
def print_scores(scores):
    print ("*** Scoreboard: ***")
    for team in scores:
        print (team + ": " + str(scores[team]) + "  ", end = "")
    print ("")


# This helps logs an incorrect inputs to a txt file so that I can review them and potentially update my menus
def log_incorrect_input(user_input, function_name):
    file = open(f"incorrect_commands.txt", "a")
    file.write(f"Incorrect Input Passed to {function_name}. Input was: {user_input}\n")
