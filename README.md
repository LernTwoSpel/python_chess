# CY300 Project: Python Chess
This is a python chess project for CY300 AY20-1.
Project Team includes CDT Deary.

# Files
 1. **chess.py**
		- This file handles the creation and display of GUI attributes.
				- Creates chess board, creates chess pieces, creates titles, creates sounds, creates "move assist" and displays pieces captured.
 2. **chess_Engine.py**
		- This file handles the logic behind the chess game.
				- Determines valid piece movement for all pieces, determines checks/checkmates/stalemates, makes moves, undo moves.
 3. **icons** [wK, wQ, wR, wB, wN, wP, bK, bQ, bR, bB, bN, bP].png
 4. **sounds** [sound, winner!].wav
 		- This folder contains sounds for the game. 'sounds.wav' plays a chess piece movement sound. 'winner!.wav' plays a sound upon player win.
# Project Overview
This project is a chess game (without special movement of en-passant and castling) created using pygame. This game was created for anyone who plays chess or new players who want to learn chess piece movement.

**How to Play**
The objective of chess is to checkmate your opponent. This occurs when the king is "in check" and is unable to remove itself from that check.

To begin, the terminal will ask you to enter the number of minutes you want each side to have during the game. If a player runs out of time before achieveing checkmate, the player will lose.

Chess is a turn-based game, with white always having the first move. If you are a beginner, the *move assist* functionality of this chess game allows you to see what the legal moves for each piece are in any scenario.

If a player makes a mistake, they are allowed to redo their move by pressing the *"U" key*. Additionally, to restart the game, the player can press the *"R" key*.

To disable sound, simply mute your computer.

For more information on chess rules, visit https://en.wikipedia.org/wiki/Chess. 

# Running the Program
The only player interaction with the terminal is to determine the number of minutes desired for each player's timer. All other user interaction with the game is via the GUI (mouseclicks) and the "R" and "U" keys.

# Code Packages/Modules
To run the program, having Python and the library pygame is needed. If you don't already have pygame installed, run the command "pip install pygame" in your terminal.

Python install: https://www.python.org/downloads/ (recommended to install latest version of Python)
Pygame install: run "pip install pygame" in terminal after installing Python.

# Input Files
No input files necessary.

# Output Files
No output files created.

# Works Cited
Chess Piece Icons: https://commons.wikimedia.org/wiki/Category:PNG_chess_pieces/Standard_transparent.

Chess General Information, Rules: https://en.wikipedia.org/wiki/Chess

Python install: [https://www.python.org/downloads/](https://www.python.org/downloads/)
