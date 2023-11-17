
# This is for the player 1 module 
# Used to handle an abrupt server disconnects
def start_game() -> None:
    while True:
        try:
            start_game()
        except ConnectionResetError:
            print("The server was forcibly closed")
            response = ""
            while True:
                response = input("Would you like to reconnect to the server? y/n: ").strip().lower()
                if response != "y" or response != "n":
                    print("Not a valid response")
                else:
                    break
            if response == "y":
                break
            else:
                continue

# This is for the player 2 module
# Used to handle abrupt client disconnects
def start_game() -> None:
    while True:
        try:
            play_game()
        except ConnectionResetError:
            print("Client forcibly disconnected")
            response = ""
            while True:
                response = input("Would you like to wait for the client to reconnect? y/n: ").strip().lower()
                if response != "y" or response != "n":
                    print("Not a valid response")
                else:
                    break
            if response == "y":
                continue
            else:
                break