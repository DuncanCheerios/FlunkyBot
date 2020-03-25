from helpers import FENload, request_fen, FEN_recover, request_move
from morehelpers import printboard, print_doc, prepturn, FEN_recover, log_incorrect_input
from time import sleep
from morehelpers import recieve_player, print_scores
from chaosbot import  chaosbot
from legal_moves_finder import legal_moves_finder
from islegal import is_legal
from flunkybot import flunkybot

# List of valid players and my score dict
players = ["human", "chaosbot", "flunkybot1.0", "flunkybot1.1", "flunkybot1.2"]
scores = {'human':0, 'chaosbot':0, 'flunkybotv1.0':0, "flunkybotv1.1":0, "flunkybotv1.2":0}


# Play() begins and manages a chess game with optional agurments for white player, black player, and a fen.

# Additionally, if War = True then this will engage a slightly different mode, where it streamlines the process and only prints each move and the final boardstate when the game is over
# "War" is designed for multiple-game engagements between bots.

def play(**kwargs): # optional arguments white = "" black = "" FEN = ""

    # sides is a dict that should assign players (human, flunkybot, chaosbot, etc) to the keys 'w' and 'b'
    sides = {}

    # Figure out the arguments, either by assigning them or by requesting them from the player
    if "FEN" in kwargs:
        mainboard = FENload(kwargs["FEN"])
    else:
        mainboard = FENload(request_fen())

    if "white" in kwargs:
        sides['w'] = kwargs["white"]
    else:
        sides['w'] = recieve_player("White")

    if "black" in kwargs:
        sides['b'] = kwargs["black"]
    else:
        sides['b'] = recieve_player("Black")

    if "war" in kwargs:
        war = kwargs["war"]

    else:
        war = False


    # Prints my header for the match
    if not war:
        print_doc("play")
        print_scores(scores)

    # This is the actual gameplay loop.  Each iteration of the loop will check to see if the game is over (checkmate/stalemate), then prepare to recieve the next turn from the appropriate source
    while True:


        # If there are no legal moves then the game is over.  This will figure out if it's a stalemate or a checkamte and act accordingly
        if len(legal_moves_finder(mainboard)) == 0:

            #  This looks for a checkmate by seeing if the King is in check
            if not is_legal(mainboard, mainboard.turn):
                #If there is a checkmate, we alert
                print("Checkmate!  Game Over!")
                printboard (mainboard)
                #Adust the scores.  Kinda crappy right now, but it gets the job done
                if mainboard.turn == "w":
                    scores[sides["b"]] += 1
                else:
                    scores[sides["w"]] += 1

                print_scores(scores)

                # If war mode is engaged, we pause for a few seconds so that the user can examine the final board state before the new game starts
                if war:
                    sleep(1)

                return True

            # This is the case for a stalemate - no legal moves available and the king is not in check
            else:
                print ("Stalemate - No legal moves available.  Game Over")
                printboard (mainboard)

                #Adust the scores.
                scores[sides["w"]] += .5
                scores[sides["b"]] += .5

                print_scores(scores)

                # If war mode is engaged, we pause for a few seconds so that the user can examine the final board state before the new game starts
                if war:
                    sleep(1)

                return True

        # Implements the 50-move rule in chess.  So that my bots don't fight forever, I enforce this as a mandatory draw instead of the traditional optional draw.
        # As this rule basically never affects human matches, I don't consider this a big deal
        if mainboard.half.isdigit() and int(mainboard.half) >= 100:

            print ("50-Move Rule Applied.  Game is a Draw.")
            printboard (mainboard)

            #Adust the scores.  I should change this so it assigns .5 points to each drawing player.  Right now it does the worst thing, it assings 1 point to the loser!  TODO FIX THIS
            scores[sides["w"]] += .5
            scores[sides["b"]] += .5

            print_scores(scores)

            # If war mode is engaged, we pause for a few seconds so that the user can examine the final board state before the new game starts
            if war:
                sleep(1)

            return True

        #If we reach this poing then the game is not over - and we can prepare to request the next move!

        #Unless we are in war-mode, we print the header for the turn:
        if not war:
            print("*"*50)
            print(f"   ---Turn {mainboard.whole}---\nCurrent FEN: "+ FEN_recover(mainboard))
            sleep(.1)
            printboard(mainboard)

        if war: #For the video demo only  TODO - remove later
            printboard(mainboard)


        # Request a move from the appropriate human or engine source  #TODO - this should be streamlined as the number of 'players' available increases
        if sides[mainboard.turn] == "human":
            player_move = request_move(mainboard)
            #This is the route for the player to 'quit' a game
            if player_move == 'exit':
                return True
            #assuming the player provides a move - we replace the board with the output of their move.
            else:
                mainboard = player_move
        #These next few elifs request moves from the appropriate versions of the engines.  All the legal-move checking happens before the new board is returned here.
        elif sides[mainboard.turn] == "chaosbot":
            if not war:
                prepturn("chaosbot")
            mainboard = chaosbot(mainboard)
        elif sides[mainboard.turn] == "flunkybotv1.0":
            if not war:
                prepturn("flunkybotv1.0")
            mainboard = flunkybot(mainboard, version = 1.0)
        elif sides[mainboard.turn] == "flunkybotv1.1":
            if not war:
                prepturn("flunkybotv1.1")
            mainboard = flunkybot(mainboard, version=1.1)
        elif sides[mainboard.turn] == "flunkybotv1.2":
            if not war:
                prepturn("flunkybotv1.2")
            mainboard = flunkybot(mainboard, version=1.2)

