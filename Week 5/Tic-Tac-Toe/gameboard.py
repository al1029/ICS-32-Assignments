class BoardClass:
    """A gameboard class that handles information for tic tac toe

    Attributes:
        user_name (str): the user name given by the player
        previous_user_name (str): User name of the last player to have a turn
        wins (int): number of wins
        ties (int): number of ties
        losses (int): number of losses
        num_games (int): number of games played
    """

    def __init__(self, user_name: str = '', previous_user_name: str = '') -> None:
        """Creates a BoardClass object

        Args:
            user_name: the user name given by the player
            previous_user_name: User name of the last player to have a turn
            wins: number of wins
            ties: number of ties
            losses: number of losses
            num_games: number of games played
        """
        
        self.user_name = user_name
        self.previous_user_name = previous_user_name
        self.wins = 0
        self.ties = 0
        self.losses = 0
        self.num_games = 0

    def update_games_played(self) ->None:
        self.num_games += 1

    def reset_game_board():
        #TODO
        pass

    def is_winner():
        #TODO
        pass

    def board_is_full():
        #TODO
        pass

    def print_stats(self):
        #TODO
        pass