# ReadMe for FlunkyBOT ChessN.E.M.E.Sys

## Table of Contents:

1. Author and Attributions
2. What is a FlunkyBOT ChessN.E.M.E.Sys?
3. Booting FlunkyBOT
4. The Main Menu
5. Beginning a Game
6. Playing Chess
7. Miscellaneous
8. FAQs


## 1. Author and Attributions

FlunkyBOT ChessN.E.M.E.Sys was written by Chris Sorenson.

The sick title card ASCII Art is courtesy of the incredible art generator on [http://patorjk.com/](http://patorjk.com/).

Thanks to Niklas Fiekas, author of the [Python Chess module](https://pypi.org/project/python-chess/).  I didn't actually end up using any of this module, but took plenty of inspiration from it, particularly the idea to create a list of pseudo legal moves.

Big thank you to the  CS50 staff, especially my tf Tom Ballatore.  Teaching FlunkyBOT to play chess was hard, but I can't imagine the challenge in teaching somebody how to program!

## 2. What is a FlunkyBOT ChessN.E.M.E.Sys?

FlunkyBOT ChessN.E.M.E.Sys is very confusingly both the name of the chess platform/program as well as the chess engine program that runs on the platform.

The **_flunky_** in flunkyBOT is partly a personification of my fears of failing this project and partly an endearment of the hard-working but charmingly incompetent chess engine - an inept Igor to my even less apt Dr. Frankenstein

N.E.M.E.Sys stands for **N**euro-**E**valuation-(check)**M**ating-**E**ngine System.  And it's a **very real** and also **extremely accurate** description of the top-of-the-line technologies deployed to make FlunkyBOT so powerful.

## 3. Booting FlunkyBOT

Flunkybot is designed to be ran inside the CS50 IDE by calling flunky.py.

The following modules may need to be installed:
 *[anytree](https://pypi.org/project/anytree/)
 *[sty](https://pypi.org/project/sty/)

Additional optional arguments when calling flunky.py:
 * For faster booting, adding the 'debug' argument will skip the intro crawl on startup ("python flunky.py debug")
 * Alternative additional arguments can be provided to 'skip' to the beginning of a game.  These are more for testing than an actual UI feature, but I'll list them anyway
 * "chaoswar" immediately starts a game between two chaosBOTs
 * "chaos" immediately pits the player against a chaosBOT
 * "morpheusisfightingneo" immpediately pits the two most recent versions of flunkyBOT against eachother.

## 4. The Main Menu

The Main Menu is the first stop after loading flunky.py.

Useful commands from the main menu:
    * "start" will begin a new chess game.  Follow up prompts will aske you who is playing white and who is playing black.
    * "middle" will allow you to pickup a game from any board position by providing a FEN (Forsyth-Edwards Notation, see faqs for details).
    * "help" will provide inormation on the main menu, that is fairly similar to this section of the ReadMe
    * "info" will provide information on the FlunkyBOT ChessN.E.M.E.Sys Platform
    * "scores" will print the current scoreboard


## 5. Beginning a New Game

1. From the Main Menu type 'start' to begin a new game.
2. The first prompt will ask who is playing white.  If a local human is playing white, type 'human.'  Otherwise, type the name of a bot to assign it to play white:
* "flunkybot" will assign the most recent version of flunkybot (currently version 1.2)
* "chaosbot" will assign chaosbot - which makes random legal moves
* "flunkybotv1.0", "flunkybotv1.1", "flunkybotv1.2" will assign specific versions of flunkybot.  Descriptions of the bots can be found in the design doc for this project, or in the info screen accessible from the main menu.
3. The second prompt will ask who is playing black.  Follow the same instructions as in step 2.

Note that it is possible to play human vs human, human vs bot, or bot vs bot games!

## 6. Playing Chess

When it is a human's turn to play a move, they will be provided with a current printout of the board and a prompt for a move that reads _"Enter your move, or type 'help' for assistance: "_.  The platform will only accept legal moves!

#### **_Inputting moves is unintuitive, please read carefully_**

#### All non-castling moves are submitted with a specific 6-7 length string that describes the piece being moved, the starting and destination sqaures and whether it is a 'move' or a 'capture'.  Each character is described below:

1. The symbol for the piece-type being moved
 * White Pieces are represented by capital letters
 * Black pieces are represented by miniscule letters
 * Each piece is represented by the the normal letter: K/k for King, Q/q for Queen, R/r for Rook, B/b for Bishop, N/n for Knight, P/p for Pawn
2. The starting column of the piece being moved, A-H (case insensitive).  In flunkybot (as in normal algebraic chess notation) the columns of the board, left to right from white's perspective, are labelled A-H.
3. The starting row of the piece moved, 1-8. In flunkybot (as in normal algebraic chess notation) the rows of the board, bottom to top from white's perspective, are labelled 1-8.
4. "-" or "x".  "-" if the piece is being moved.  "x" if the piece is capturing another piece.
5. The destination column of the piece being moved, A-H (case insensitive).  In flunkybot (as in normal algebraic chess notation) the columns of the board, left to right from white's perspective, are labelled A-H.
6. The destination row of the piece moved, 1-8. In flunkybot (as in normal algebraic chess notation) the rows of the board, bottom to top from white's perspective, are labelled 1-8.
7. **Only used in pawn Promotions.**  If the move is a pawn promotion, this final character indicates the piece that it is promoting to.  A pawn can promote to Q/q for a queen, R/r for a rook, B/b for a bishop, or N/n for a knight.  Be certain to use a capital letter for white and a miniscule for black.

**Typing 'help' at the move prompt will bring up an abbreviated version of this descripton**

##### Examples:
* Pe2-e4 - White moving a pawn from e2 to e4 - the most common first move of a game
* pe7-e5 - Black moving a pawn from e7 to e5 - the most common response
* nh4-g6 - Black moving a Knight from H4 to G6:
* Ke1xd2 - White King on E1 capturing on D2
* qd8xf6 - Black queen on d8 capturing on f6
* Pd5xe6 - White pawn on d5 capturing on e6.  Note that this could also represent the White pawn capturing by en-passant a pawn on e6
* pf2-f1b - Black pawn on f2 moving to f1 and promoting to a bishop


#### Castling

Castling uses traditional chess notation, with the slight addition of a leading character for the side that is castling

* For white to castle King-Side, type 'w0-0'
* For white to castle Queen-Side, type 'w0-0-0'
* For black to casle King-side, bype 'b0-0'
* For black to castle Queen-Side, type 'b0-0-0'

#### The Movelist

Typing 'moves' at the input prompt provide a very useful list of moves from the current position.  This list is designed as a tool for learning how to format moves appropriately.  This is **not** a list of all legal moves - although every legal move will be on the list, there may be some illegal moves in there as well!

Note that any illegal moves on the move list will still be rejected by the platform!


## 7. Miscellaneous

This section has some useful information for testing and playing with the FlunkyBOT system.


The following shortcuts from the main menu will pit bots against eachother in endless battles. Useful for testing, finding bugs and funny to watch.  Will only print the moves being made and the board at the end of the game.
* "chaoswar" will pit the two chaosBOTs against eachother in an endless series of games.  Great for finding bugs/breaking the program.
* "morpheusisfightingneo" will pit the two most recent versions of flunkyBOT against eachother in an endless series of games.  Useful for testing new versions.
* "morpheusisfightingstupid" will pit the best version of FlunkyBOT against ChaosBOT.


## 8. FAQ's

#### 1:  What is a FEN?

 A FEN (Forsyth-Edwards Notation) is a standard system for documenting the game state of a given chessboard.  A FEN is a string that records 6 items seperated by sapces

 1. A shorthand description of the pieces on each row of the board
 2. The color of the player that must move next ('b' or 'w')
 3. The current castling rights for White and Black (The characters 'K', 'Q', 'k', 'q' represent King and Queenside castling for white and black.  If there are no castling rights, a single hyphen is included)
 4. The En-Passantable square on the board, or a hyphen if no square is enpassantable
 5. The number of half-moves since the last capture or pawn move.
 6. The number of whole moves since the beginning of the game.

For example:  "rnb1kb1r/p1pp1ppp/7q/1B5n/4Pp2/3P1N2/PPP3PP/RNBQ1K1R w kq - 1 8" is the FEN of a position from the famous 'immortal game.' Ignoring the first section, the complicated board state, you can see it is white's turn to play, black can still castle on either side, no square is enpassantable, there has been 1 turn since a capture/pawn push, and it is now the 8th turn of the match!

Most computer chess platforms provide FENs for boardstates, and the FlunkyBOT system is able to read (and output) properly formatted FENs.  You can 'test' the different engines hosted on FlunkyBOT by submitting FENs of puzzles, or even boardstates from famous games (or your own games)!

Note that many sources use abbreviated versions of FEN in certain contexts.  For instance, the FEN of a puzzle will often be provided without parts 5 and 6 if the number of moves does not bear on the solution.  It may be necessary to provide dummy values to Flunkybot when providing these FENs.

#### 2:  How do I play old models of flunkybot

The first two versions of flunkybot are accessible to play.  When prompted "Who is playing white/black", respond with 'flunkybotv1.0' or 'flunkybotv1.1' to play older models

#### 3:  Some sample FENs if you want to try picking up games 'from the middle':

A Critical moment in the opera house game: "rn2kb1r/p3qppp/2p2n2/1p2p1B1/2B1P3/1QN5/PPP2PPP/R3K2R w KQkq - 0 10"
Total Nonsense Board: "2prbk1k/3pnb2/P3pqbk/RP3pnb/BNP3pr/KBQP3p/2BNP3/K1KBRP2 w KQkq - 0 0"
Dunsany's Chess Variant: "rnbqkbnr/pppppppp/8/8/PPPPPPPP/PPPPPPPP/PPPPPPPP/PPPPPPPP w KQkq - 0 0"