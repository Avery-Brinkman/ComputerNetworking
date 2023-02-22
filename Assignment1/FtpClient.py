# Assignment 1
# Avery Brinkman

import socket

CLRF = b"\r\n"

class FtpClient:
  # Constructor
  def __init__(self, ftpAddr: str = "127.0.0.1", ftpPort: int = 21):
    self.controlSock: socket.socket
    self.dataPort: int
    self.ftpAddr: str = ftpAddr
    self.ftpPort: int = ftpPort

  # Sets up connection to FTP server w username and password
  def connect(self, username: str, password: str):
    # Creates a socket and connects to FTP server
    self.controlSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.controlSock.connect((self.ftpAddr, self.ftpPort))
    # Ensures that connection is successfully established
    assert int(self.controlSock.recv(1024)[:3]) == 220

    # Send username and password, and ensures that they are accepted
    self.sendCommand("USER " + username, 331)
    self.sendCommand("PASS " + password, 230)

  # Closes the connection
  def disconnect(self):
    self.sendCommand("QUIT", 221)
    self.controlSock.close()

  # Sends a command and checks the response
  def sendCommand(self, command: str, expectedResponse: int):
    # Converts the string to bytes
    fullCommand = bytes(command, "utf-8") + CLRF
    # Sends command
    self.controlSock.send(fullCommand)
    # Reads response and checks that it is what's expected 
    serverResponse = self.controlSock.recv(1024)
    assert int(serverResponse[:3]) == expectedResponse
    # Return response so information may be used
    return serverResponse

  # Returns the data port when given a PASV response
  def getDataPort(self, response: str):
    # Get the IP and Port tuple
    addrPort = response[response.find("(") + 1:response.rfind(")")].split(",")
    portVals = addrPort[-2:]
    # Calculate port value
    return portVals[0] * 256 + portVals[1]

  # Gets the file from a FTP server
  def getFile(self, fileName: str):
    # Move to root
    self.sendCommand("CWD /", 250)
    # Set to passive
    response = str(self.sendCommand("PASV", 227))
    # Get the data port to use
    dataPort = self.getDataPort(response)

a = FtpClient()
a.connect("abrinkman", "admin123")
a.getFile("adfs.txt")
a.disconnect()
