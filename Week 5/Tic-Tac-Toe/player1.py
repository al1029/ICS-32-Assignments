"""A module used to play tic-tac-toe as Player 1 using sockets.

Player 1 acts as the client and asks Player 2 (server) for the host information. If 
connection is successful, Player 1 and Player 2 exchange usernames and begin playing 
tic-tac-toe using the BoardClass. Once the game ends, Player 1 is prompted if they want
to play again. If they say yes a new game starts, if they say no the client disconnects 
from the server and Player 1 stats are displayed.
"""


