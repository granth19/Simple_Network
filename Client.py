from socket import *

serverName = input("Enter server name: ")
port = input("Enter port number: ")
#Check if the user input is valid
while not(port.isdigit()):
    print ("Invalid input. Please input a port number.")
    port = input("Enter port number: ")
port = int(port)
#creates the socket
clientSocket = socket(AF_INET, SOCK_STREAM)
#tries to connect to specified server on specified port
clientSocket.connect((serverName,port))
fileName = input("Enter file name: ")
toSend = "GET /" + fileName + " HTTP/1.0\r\nHost:  " + serverName + "\r\n\r\n"
#sends valid GET request
clientSocket.send(toSend.encode())
#for testing
#recieved = clientSocket.recv(1024)
#print (recieved.decode())
#A bytes type variable that will contain everything sent to the client
fullMesB = bytes("", 'utf-8')
while True:
    bRead = clientSocket.recv(1024)
    fullMesB = fullMesB + bRead
 #   fullMes = fullMes + bRead.decode()
    if not bRead:
        break
#Checks if the server sends back a valid reply
if fullMesB[0:32].decode() == "HTTP/1.0 200 OK\r\nContent-Length:":
    seperate = fullMesB.split( )
    #the length is located at 4
    lenStart = fullMesB.find(seperate[4])
    #This represents where the file content actually starts
    #It takes from where the number of content length starts + the length of the number of content length + another 4 for \r\n
    start = lenStart + len(seperate[4]) + 4
    with open(fileName, "wb") as file:
        file.write(fullMesB[start:])
else:
    print (fullMesB.decode())
clientSocket.close()