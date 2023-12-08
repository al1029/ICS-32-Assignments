class BoardClass:
    """A gameboard class that handles information for tic tac toe.

    Attributes:
        user_name (str): the user name given by the player.
        opponent (str): User name of the opposing player.
        last_player_turn (str): User name of the last player to have a turn.
        wins (int): number of wins.
        ties (int): number of ties.
        losses (int): number of losses.
        num_games (int): number of games played.
        GAME_BOARD (list[list]): game board used for resets.
        used_game_board (list[list]): game borad used in game.
    """


    def __init__(self, user_name: str = '', opponent: str = ''):
        """Creates a BoardClass object.

        Args:
            user_name: the user name given by the player.
            opponent: User name of the opposing player.
        """
        
        self.user_name = user_name
        self.opponent = opponent
        self.last_player_turn = ""
        self.wins = 0
        self.ties = 0
        self.losses = 0
        self.num_games = 0
        self.GAME_BOARD = [["_", "_", "_"], 
                           ["_", "_", "_"], 
                           ["_", "_", "_"]]
        self.used_game_board = [row[:] for row in self.GAME_BOARD]


    def update_games_played(self) -> None:
        self.num_games += 1


    def update_wins(self) -> None:
        self.wins += 1


    def update_ties(self) -> None:
        self.ties += 1


    def update_losses(self) -> None:
        self.losses += 1


    def update_turn(self, username: str) -> None:
        """Updates the variable for the last player place a symbol.
        
        Args:
            username: the username of the player.
        """
        self.last_player_turn = username


    def set_username(self, username):
        self.user_name = username


    def set_opponent_username(self, opponent_username):
        self.opponent = opponent_username


    def get_username(self):
        return self.user_name


    def get_opponent_username(self):
        return self.opponent


    def reset_game_board(self) -> None:
        self.used_game_board = [row[:] for row in self.GAME_BOARD]


    def display_board(self) -> None:
        for row in self.used_game_board:
            print(" ".join(map(str,row)))
        print()


    def place_symbol(self, piece:str, row: int, col: int) -> None:
        """Places the symbol of the player on the board.
        
        Args:
            piece: the symbol of the player.
            row: the desired row.
            col: the desired column.
        """
        self.used_game_board[row - 1][col - 1] = piece


    def place_symbol_ui(self, piece: str, row: int, col: int) -> None:
        """Places the symbol of the player on the board.

        Copy of place_symbol for personal folder management.
            
            Args:
                piece: the symbol of the player.
                row: the desired row.
                col: the desired column.
            """
        self.used_game_board[row][col] = piece


    def valid_play(self, row: int, col: int) -> bool:
        """Checks if the desired placement is a valid play.
        
        Args:
            row: the desired row.
            col: the desired column.

        Returns:
            True if the placement is a valid play.
            False otherwise.
        """
        return self.used_game_board[row - 1][col - 1] == "_"


    def check_rows(self) -> bool:
        """Checks all rows to determine if a player has won.
        
        Returns:
            True if a row has the same player element.
            False otherwise.
        """

        board = self.used_game_board
        for row in range(0,3):
            if (board[row][0] == board[row][1] == board[row][2] == "X"):
                return True
            elif (board[row][0] == board[row][1] == board[row][2] == "O"):
                return True
        return False


    def check_cols(self) -> bool:
        """Checks all columns to determine if a player has won.
        
        Returns:
            True if a column has the same player element.
            False otherwise.
        """

        board = self.used_game_board
        for col in range(0,3):
            if (board[0][col] == board[1][col] == board[2][col] == "X"):
                return True
            elif (board[0][col] == board[1][col] == board[2][col] == "O"):
                return True
        return False


    def check_diagonals(self) -> bool:
        """Checks both diagonals to determine if a player has won.
        
        Returns:
            True if a diagonal has the same player element.
            False otherwise.
        """

        board = self.used_game_board
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


    def is_winner(self) -> bool:
        """Checks if the player has won by checking rows, columns, and diagonals.
        
        Returns:
            True if the player has won.
            False otherwise.
        """


        if self.check_diagonals() or self.check_rows() or self.check_cols():
            self.update_wins() 
            return True
        else:
            return False


    def is_winner_ui(self) -> bool:
        """Checks if the player has won by checking rows, columns, and diagonals.

        Copy of is_winner for personal folder management.
        
        Returns:
            True if the player has won.
            False otherwise.
        """


        if self.check_diagonals() or self.check_rows() or self.check_cols():
            return True
        else:
            return False


    def find_winner(self) ->str:
        """Checks which player has won.
        
        Returns:
            Symbol of player who won.
        """
        board = self.used_game_board
        for row in range(0,3):
            if (board[row][0] == board[row][1] == board[row][2] == "X"):
                return "X"
            elif (board[row][0] == board[row][1] == board[row][2] == "O"):
                return "O"
            
        for col in range(0,3):
            if (board[0][col] == board[1][col] == board[2][col] == "X"):
                return "X"
            elif (board[0][col] == board[1][col] == board[2][col] == "O"):
                return "O"
            
        if all(board[i][i] == "X" for i in range(len(board))):
            return "X"
        elif all(board[i][i] == "O" for i in range(len(board))):
            return "O"
        # Check backward diagonals
        elif all(board[i][-i - 1] == "X" for i in range(len(board))):
            return "X"
        elif all(board[i][-i - 1] == "O" for i in range(len(board))):
            return "O"


    def board_is_full(self) -> bool:
        """Check if the game board is full and updates number of ties.
        
        Returns:
            True if the game board has no more places to play.
            False otherwise.
        """

        for row in self.used_game_board:
            for element in row:
                if element == "_":
                    return False
        self.update_ties()
        return True


    def print_stats(self) -> None:
        print(f"Player name: {self.user_name}")
        print(f"Last player to make a move: {self.last_player_turn}")
        print(f"# of games played: {self.num_games}")
        print(f"# of wins: {self.wins}")
        print(f"# of losses: {self.losses}")
        print(f"# of ties: {self.ties}")