class BoardClass:
    """A gameboard class that handles information for tic tac toe

    Attributes:
        user_name (str): the user name given by the player
        previous_user_name (str): User name of the last player to have a turn
        wins (int): number of wins
        ties (int): number of ties
        losses (int): number of losses
    """

    def __init__(self, user_name: str = '', previous_user_name: str = '', wins: int = 0, ties: int = 0, losses: int = 0) -> None:
        """Creates a BoardClass object

        Args:
            user_name: the user name given by the player
            previous_user_name: User name of the last player to have a turn
            wins: number of wins
            ties: number of ties
            losses: number of losses
        """
        
        self.user_name = user_name
        self.previous_user_name = previous_user_name
        self.wins = wins
        self.ties = ties
        self.losses = losses

    def updateGamesPlayed():
        #TODO
        pass

    def resetGameBoard():
        #TODO
        pass

    def isWinner():
        #TODO
        pass

    def boardIsFull():
        #TODO
        pass

    def printStats(self):
        #TODO
        pass