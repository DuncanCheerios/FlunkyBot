## Design Document for FlunkyBOT ChessN.E.M.E.Sys

#### The Goal:
I had no  finish line in mind for this project.  The plan was to work towards a chess engine and see how far I got!

There were three main parts to my project:
1. Implementing rules and logic of chess
2. Building a platform to play on
3. Making an engine to play against

#### 1. The Rules of Chess

I created a custom board class that would store information similar to the standard FEN notation so it'd be easilty compatible with other digital chess platforms.  This made it easy to 'import' and 'export' board states betwen my program and other chess platforoms- to pose puzzles to my engines, to pick up games in the middle, or for debugging.  The class stores 6 pieces of information, most critically the position of the pieces on the board in a 2-D array.  Eventually - the plan was to expand my class definition to integrate with the logic of the actual chess engine.

With the board in hand, the next step was teaching the program how pieces move.  It's easy to **_say_** Bishops move diagonally.  But suppose a player wants to move the white bishop from H2 to D6.  Are those squares on the same diagonal?  Is there a piece that blocks the movement on G3, F4 or E5?  Or a white piece already placed on D6?  Will moving the bishop expose the white king to discovered check?  Or perhaps the King is already in check and the bishop can't move at all.  The situation gets more complicated when considering the strange rules that govern pawns (double-moves, diagonal capturing, en passanting, promotions) and castling.

The key was in seperating **_"legal"_** moves from **_"pseudo legal moves"_**.

**Pseudo_legal_moves()** generates the set of moves that a piece is _threatening_ to make, if it's own King safety wasn't a concern - this is an important distinction, because a piece can be legally threatening a square without actually being able to legally move to that square (such as if the piece itself if pinned to its own king).  I also chose to include moves that 'capture' the king in the set of pseudo-legal-moves;  even though the king can't even be captured in play, it is important to 'see' these moves to evaluate whether or not board states are legal.

My **is_legal()** function does exactly that.  I check the _actual_ legality of each move by calling **pseudo_legal_moves** a second time after the move has been implemented (on a temporary, imaginary board) and seeing if any of these pseudo-moves 'capture' the king (i.e. put the king in check).

So **pseudo_legal_moves()** does the actual lion's share of chess logic, iterating over every piece on the board and figuring out where it could move if King safety was no concern.  A piece like a knight or King is simple - it can only ever move/capture 8 fixed squares.

#### 2. Building a Platform

I originally anticipated building only an extremely barebones UI for the project - just enough to serve the needs of working on the chess engine.  But the more time I spent with flunkyBOT, the more convenience I desired, and I expanded the UI.  The graphics of the chessboard is a good example.

1. Version 1 graphics was just printouts of the move notations
2. Version 2 was a simple grid of 64 characters - letters for pieces and 0's for blank sqaures
3. Version 3 added an Ascii grid
4. Version 4 revamped with unicode symbols for actual chess pieces
5. Version 5 finally added colors to the squares and pieces!

>rnbqkbnr
>pppppppp
>00000000
>00000000
>00000000
>00000000
>PPPPPPPP
>RNBQKBRN
>**My second version of graphics.  Not very legible!**

Other UI features, many of which are invisible, followed the same route of organic growth.  Inputting moves, for example, became much more user-friendly as I iterated.  The ability to 'call' a list of available moves, the ability to retrieve the FEN from any position with a command, the ability to play multiple games without restarting the program, etc.

My favorite feature is the ability to set two engines against eachother in a never ending duel of games.  I call it "war" mode, and I usually let my engines duke it out while I work.

#### 3. Making the Chess Engine

I planned to model the game as a tree of possible board states and tackle the problem of chess intelligence with two parts
1. A function to evaluate board states 'naively' - aka without 'looking ahead' at future states
2. Another function to 'choose' which future board states were worth evaluating

One tool to evaluate nodes of the tree and the other to 'prune' the tree.

Seperating the two concepts was very unintuitive.  Even a mediocre chess player like me can effortlessly multitask these two processes, creating mental lists of likely candidate moves, searching them at reasonable depths until they reach 'stable' positions, and drawing conclusions.  But you can't tell a computer _"evaluating the current board state requires that you evaluate the next board state"_ without going into an almost endless recursion.

Unfortunately there wasn't time to implement the second aspect of the engine.  So I had to settle with creating an engine that just depended on 'naieve' evaluation; meaning my chess engine has an effective search depth of 1.

##### Versions of FLunkyBOT

* **ChaosBOT** was the first 'engine'- though it was really just a prototype. ChaosBOT simply selects randomly from a list of all possible legal moves.  Dumb as a rock, but surprisingly entertaining to watch.  Also really great at finding every concievable bug in my program by getting itself into all kinds of unexpected situations.

* **FlunkyBOTv1.0**  Uses a simple material counter.  Using the canonical values of chess pieces, v1.0 chooses moves that maximize it's material worth relative to its opponent.  Though FlunkyBOTv1.0 crushes ChaosBOT, by only looking 1 move ahead, FlunkyBOTv1.0 is happy to take a measly pawn with the mighty queen, regardless of what danger that puts the queen in.  This BOT also fails to look for checkmates, so even with a crushing material advantage it is unable to deliver the decisive blow with consistency.

* **FlunkyBOTv1.1** added the ability to identify checkmate and stalemate scenarios and is otherwise identical to v1.0.

* **FlunkyBOTv1.2** marks a big step up.  This version of flunkyBOT now weighs that value of a piece by how many times that piece is attacked/defended.  An undefended piece that is under attack and likely to fall next turn is weighted at about 10% the value of the same piece if it is defended.  Though a simple concept, adding this substantially improved FlunkyBOT's performance.

##### Overall:
FlunkyBOTv1.2 >>>> FLunkyBOTv1.1 > FLunkyBOTv1.0 >>> ChaosBOT

#### 4. Woulda-Coulda-Shouldas and the Future of FlunkyBOT

The biggest lesson learned was that I should have used more of the class features in python.  In particular I should be storing the set of pseudo-legal-moves within the class itself.  In the current version I end up having to repeatedly call pseudolegalmoves on the same board in different contexts, and its very resource wasteful.  I can get away with it in the current version of the engine that only 'looks ahead' at a depth of a single move, but looking even a few moves further would be prohibitive in my current setup.

I also would really like to implement the tree model to benefit both how the platform stores the gamestate and how the engine evaluates .  It would help not only to develop engines that can look at further depth, but also be a helpful resource for the chess platform to use to navigate the game.  Things like undoing a move - or going back after a game to revisit an interesting moment would be much easier if the tree model existed.

Though I really like how I store moves within the program (in particular including the origin square and an indicator for whether a move is a capture or not), I wish I had comitted to using full chess notation for all inputs and outputs.  It would have taken a lot of upfront time (the rules of algebraic chess notation are a pain), but would have increased useability and would make it easier to output conventional records of the games played.

