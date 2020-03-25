from sys import argv
from morehelpers import opening
from play import play
from mainmenu import mainmenu

def main():



    # Prints the title card on startup.  Random delay in the line printing to give it an old-fahsioned feeling
    # If the user provides any other command line argument then it skips this step to save me time in testing
    if len(argv) == 1:
        opening()


    # Some useful shortcuts to skip directly to playing a game.

    # Starts a game between two chaosbots
    if "chaoswar" in argv:
        play(white = "chaosbot", black = "chaosbot", FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", war = True)

    # Starts a game against a chaosbot
    elif "chaos" in argv:
        play(white = "human", black = "chaosbot", FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    # Starts a game against a Flunkybot
    elif "flunky" in argv:
        play(white = "human", black = "flunkybotv1.2", FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    elif "morpheusisfightingneo" in argv:
        while(True):
            play(white = "flunkybotv1.2", black = "flunkybotv1.1", FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", war = True)

    mainmenu()


if __name__ == "__main__":
    main()