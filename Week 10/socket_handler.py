import time
import socket

class SocketHandler:
    """A socket handler class that handles multithreading tasks to run in the background.
    
    Attributes:
        message_sent (bool): A boolean to see if a messgage has been sent.
        waiting (bool): a boolean to check if currently waiting for a message.
        connection_established (bool): a boolean to check if a connection has been established with a socket client.
        row (int): the row of the tic tac toe board sent by a socket.
        col (int): the col of the tic tac toe board sent by a socket.
        response (str): the decision of player 1 if they want to play again.
        response_received (bool): a boolean to check if if the response was received.
        keep_running (bool): a boolean to check if a funciton should keep running.
        client_socket (socket.socket): the client socket.
        opponent_username (str): the username of the opponent.
    """

    def __init__(self):
        """Creates an SocketHandler object.
        
        """
        
        self.message_sent = False
        self.waiting = False
        self.connection_established = False
        self.row = ""
        self.col = ""
        self.response = ""
        self.response_received = False
        self.keep_running = True
        self.client_socket = ""
        self.opponent_username = 0


    def handle_message(self, client_socket: socket.socket) -> None:
        """Handles the row and column sent by a socket.

        Args:
            client_socket: the client socket.
        """

        self.waiting = True
        self.row = int(client_socket.recv(1).decode())
        self.col = int(client_socket.recv(1).decode())
        self.message_sent = True
        self.waiting = False

    def handle_response(self, client_socket: socket.socket) -> None:
        """Handles the response from player 1 if the want to play again.
        
        Args:
            client_socket: the client socket.
        """

        self.response = client_socket.recv(1024).decode()
        self.response_received = True


    def wait_for_connection(self, server_socket: socket.socket) -> None:
        """Attempts to connect accept a connection from a client socket.
        
        Args:
            server_socket: the server socket.
        """

        server_socket.listen(1)
        self.client_socket, addr = server_socket.accept()
        self.client_socket.send(b"Player 2")
        self.opponent_username = self.client_socket.recv(1024).decode()
        self.connection_established = True


    def wait_for_time(self, wait_time: int) -> None:
        """Halts program for a specified amount of time.
        
        Args:
            wait_time: the desired time to halt program.
        """

        time.sleep(wait_time)
        self.keep_running = False


    def get_keep_running(self):
        return self.keep_running


    def get_response(self):
        return self.response


    def get_row(self):
        return self.row
    

    def get_col(self):
        return self.col


    def get_opponent_username(self):
        return self.opponent_username
    

    def get_message_state(self):
        return self.message_sent
    

    def get_wait_state(self):
        return self.waiting
    

    def get_connection_state(self):
        return self.connection_established
    
    
    def get_client_socket(self):
        return self.client_socket


    def set_message_state(self, state: bool):
        self.message_sent = state
    

    def set_wait_state(self, state: bool):
        self.waiting = state

    
    def set_connection_state(self, state: bool):
        self.connection_established = state


    def del_response(self):
        self.response = ""


    def del_row(self):
        self.row = ""


    def del_col(self):
        self.col = ""

    def reset_variables(self):
        self.message_sent = False
        self.waiting = False
        self.connection_established = False
        self.row = ""
        self.col = ""
        self.response = ""
        self.keep_running = True
        self.response_received = False