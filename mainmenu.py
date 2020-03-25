from morehelpers import print_doc, log_incorrect_input, print_scores
from play import play, scores
from helpers import request_fen


# This loads up my main menu
def mainmenu():

    # Prep soem useful variables.
    user_input = ""
    menu_title = 1

    while user_input not in ["start", "play", "begin", "Start", "Play", "Begin"]:

        #Print the menu screen.  The menu-title variable makes sure that the menu header only prints once, even if the while-loop
        #repeats.  Useful if the user keeps inputting bad inputs
        if menu_title != 0:
            print_doc('menu')
            menu_title = 0

        #Figure out what the user wants to do.
        user_input = input ("What would you like to do?")


        # Starts a new game, side selection to happen in the next screen
        if user_input in ["start", "play", "begin", "Start", "Play", "Begin", "newgame", "new"]:
            play(FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

        # Prints the info screen
        elif user_input in ["info","Info", "Information", "information"]:
            print_doc("info")

        # Prints the info screen
        elif user_input in ["help", "Help"]:
            print_doc("menuhelp")

        # Picks up a game from the middle
        elif user_input in ["middle", "Middle", "FEN", "fen"]:
            play(FEN = request_fen())

        # prints the scoreboard
        elif user_input in ["scores", "SCORES", "score", "SCORE", "Score"]:
            print_scores (scores)

        # Starts an infinite loop of games between chaosBOTs.  Fun to watch and useful for debugging
        elif user_input in ["Chaoswar", "chaoswar"]:
            while True:
                play(white = "chaosbot", black = "chaosbot", FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", war = True)

        # Starts an infinite loop of games between two versions of flunkybot.  Fun to watch and useful for debugging
        elif user_input in ["Flunkywar", "flunkywar"]:
            while True:
                play(white = "flunkybotv1.1", black = "flunkybotv1.0", FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", war = True)

        # Starts an infinite loop of games between best two versions of flunkybot.  Useful for improving the algorithms
        elif user_input in ["morpheusisfightingneo"]:
            while True:
                play(white = "flunkybotv1.2", black = "flunkybotv1.1", FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", war = True)

        #Pits the best and the worst bots against eachother.
        elif user_input in ["morpheusisfightingstupid"]:
            while True:
                play(white = "chaosbot", black = "flunkybotv1.1", FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", war = True)

        # If we get an unexpected input, I log it into a file so that I can update my logic to be more understandable later
        else:
            log_incorrect_input(user_input, "mainmenu")
            print ("Command not recognized, please try again or type 'help' to see available commands")
