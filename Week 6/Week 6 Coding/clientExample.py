#Import the socket library
import socket

#Define my socket address information
serverAddress = "127.0.0.1"
serverPort = 8000

#create a socket object on my server
connectionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Attempt to connect to the server
connectionSocket.connect((serverAddress,serverPort))

#Wait for a message from my server
serverData = connectionSocket.recv(4)
print(serverData.decode("ascii"))
serverData = connectionSocket.recv(4)
print(serverData.decode("ascii"))

#Send data to server
connectionSocket.send(b"World")

#closing the connection when I am done
connectionSocket.close()

