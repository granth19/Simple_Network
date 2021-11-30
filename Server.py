
from socket import *
from os.path import exists
import os

port = input("Enter port number: ")
#Check if the user input is valid
while not(port.isdigit()):
    print ("Invalid input. Please input a port number.")
    port = input("Enter port number: ")
port = int(port)
#creates the socket
serverSocket = socket(AF_INET, SOCK_STREAM)
#binds the socket at specified port
serverSocket.bind(('',port))
serverSocket.listen(1)
while True:
    #connect to client
    connectionSocket, addr = serverSocket.accept()
    recieved = connectionSocket.recv(1024).decode()
    #splits the recieved message into a list
    recSplit = recieved.split( )
    fileName = recSplit[1]
    #gets the file name from the recieved message
    fileName = fileName[1:]
    #Checks if the client sends a valid request
    if(recSplit[0] != "GET" or recSplit[2] != "HTTP/1.0" or recSplit[3] != "Host:"):
       badReq = "HTTP/1.0 400 Bad Request"
       connectionSocket.send(badReq.encode())
    #checks if the inputted file exists
    elif not(exists(fileName)):
        notFound = "HTTP/1.0 404 Not Found"
        connectionSocket.send(notFound.encode())
    elif(exists(fileName)):
        #gets the size of the file
        fileSize = os.path.getsize(fileName) 
        file = open(fileName, "rb")
        #reads from the file and then sends the contents to the client
        with open(fileName, "rb") as file:
            ok = "HTTP/1.0 200 OK\r\nContent-Length: %d\r\n\r\n" % fileSize
            connectionSocket.send(ok.encode())
            while True:
                bRead = file.read(1024)
                connectionSocket.send(bRead)
                if not bRead:
                    break

    connectionSocket.close()