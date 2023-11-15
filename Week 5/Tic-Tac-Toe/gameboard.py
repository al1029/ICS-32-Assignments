class BoardClass:
    """A gameboard class that handles information for tic tac toe.

    Attributes:
        user_name (str): the user name given by the player
        opponent (str): User name of the opposing player
        last_player_turn (str): User name of the last player to have a turn
        wins (int): number of wins
        ties (int): number of ties
        losses (int): number of losses
        num_games (int): number of games played
        used_game_board (list[list])
        game_over (bool): Boolean to check if the game is over
    """

    # Variable Constants
    GAME_BOARD = [["_", "_", "_"], 
                  ["_", "_", "_"], 
                  ["_", "_", "_"]]

    def __init__(self, user_name: str = '', opponent: str = '') -> None:
        """Creates a BoardClass object

        Args:
            user_name: the user name given by the player
            opponent: User name of the opposing player
            last_player_turn: User name of the last player to have a turn
            wins: number of wins
            ties: number of ties
            losses: number of losses
            num_games: number of games played
            game_over: Boolean to check if the game is over
        """
        
        self.user_name = user_name
        self.opponent = opponent
        self.last_player_turn = ""
        self.wins = 0
        self.ties = 0
        self.losses = 0
        self.num_games = 0
        self.used_game_board = self.GAME_BOARD
        self.game_over = False


    def update_games_played(self) ->None:
        self.num_games += 1


    def reset_game_board(self) ->None:
        self.used_game_board = self.GAME_BOARD
        self.last_player_turn = ""


    def place_play(self, piece:str, row: int, col: int):
        self.used_game_board[row][col] = piece


    def valid_play(self, row: int, col: int) ->bool:
        return self.used_game_board[row][col] == "_"


    def is_game_over(self) ->bool:
        return self.game_over
    
    
    def check_rows(self) ->bool:
        """Checks all rows to determine if a player has won.
        
        Returns:
            True if a row has the same player element
            False otherwise
        """

        board = self.used_game_board
        for row in range(0,3):
            if (board[row][0] == board[row][1] == board[row][2] == "X"):
                return True
            elif (board[row][0] == board[row][1] == board[row][2] == "O"):
                return True


    def check_cols(self) ->bool:
        """Checks all columns to determine if a player has won.
        
        Returns:
            True if a column has the same player element
            False otherwise
        """

        board = self.used_game_board
        for col in range(0,3):
            if (board[0][col] == board[1][col] == board[2][col] == "X"):
                return True
            elif (board[0][col] == board[1][col] == board[2][col] == "O"):
                return True
        return False


    def check_diagonals(self) ->bool:
        """Checks both diagonals to determine if a player has won.
        
        Returns:
            True if a diagonal has the same player element
            False otherwise
        """

        board = self.used_game_board
        
        # Check forward diagonals
        if all(board[i][i] == "X" for i in range(len(board))):
            return True
        elif all(board[i][i] == "O" for i in range(len(board))):
            return True
        # Check backward diagonals
        elif all(board[i][-i - 1] == "X" for i in range(len(board))):
            return True
        elif all(board[i][-i - 1] == "O" for i in range(len(board))):
            return True
        else:
            return False


    def is_winner(self):
        if self.check_diagonals or self.check_rows or self.check_cols:
            self.wins += 1 
            game_over = True
            return True
        return False


    def board_is_full(self) ->bool:
        """Check if the game board is full and updates the ties count.
        
        Returns:
            True if the game board has no more places to play
            False otherwise
        """

        for row in self.used_game_board:
            for element in row:
                if element == "_":
                    return False
        self.ties += 1
        self.game_over = True
        return True


    def print_stats(self) ->None:
        print(f"Last player to make a move: {self.last_player_turn}")
        print(f"# of games played: {self.num_games}")
        print(f"# of wins: {self.wins}")
        print(f"# of losses: {self.losses}")
        print(f"# of ties: {self.ties}")