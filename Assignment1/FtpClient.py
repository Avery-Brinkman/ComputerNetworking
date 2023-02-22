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
    response = self.controlSock.recv(1024)
    if int(response[:3]) != 220:
      raise Exception("Expected code 220, got " + response.decode("utf-8"))

    # Send username and password, and ensures that they are accepted
    self.sendCommand("USER " + username, 331)
    self.sendCommand("PASS " + password, 230)

  # Closes the connection
  def disconnect(self):
    self.sendCommand("QUIT", 221)
    self.controlSock.close()

  # Sends a command and checks the response
  def sendCommand(self, command: str, expectedResponse: int) -> bytes:
    # Converts the string to bytes
    fullCommand = bytes(command, "utf-8") + CLRF
    # Sends command
    self.controlSock.send(fullCommand)
    # Reads response and checks that it is what's expected 
    serverResponse = self.controlSock.recv(1024)
    if int(serverResponse[:3]) != expectedResponse:
      raise Exception("Expected code " + str(expectedResponse) + ", got " + serverResponse.decode("utf-8"))
    # Return response so information may be used
    return serverResponse

  # Returns the data port when given a PASV response
  def getDataPort(self, response: str) -> int:
    # Get the IP and Port tuple
    addrPort = response[response.find("(") + 1:response.rfind(")")].split(",")
    portVals = addrPort[-2:]
    # Calculate port value
    return int(portVals[0]) * 256 + int(portVals[1])

  # Gets the file from a FTP server
  def getFile(self, fileName: str):
    # Move to root
    self.sendCommand("CWD /", 250)
    # Set to passive
    response = str(self.sendCommand("PASV", 227))
    # Get the data port to use
    dataPort = self.getDataPort(response)

    # Create a new socket for the file data
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as dataSocket:
      dataSocket.connect((self.ftpAddr, dataPort))

      # Get the file, and use response to find file size
      responseLine = self.sendCommand("RETR " + fileName, 150).decode("utf-8")
      # Wait for transfer complete response
      transferResponse = self.controlSock.recv(1024)
      if int(transferResponse[:3]) != 226:
        raise Exception("Expected code 226, got " + transferResponse.decode("utf-8"))

      # First response somtimes gets both lines, so find eol
      endOfFirstLine = responseLine.find("bytes).\r\n")
      # Find last "("
      startOfBytes = responseLine.rfind("(", 0, endOfFirstLine) + 1
      # Convert num of bytes string to int
      fileSize = int(responseLine[startOfBytes:endOfFirstLine])
      # Get that number of bytes
      fileBytes = dataSocket.recv(fileSize)
      # Open a writeable bytes file with same name locally (create if doesn't exist)
      with open(fileName[fileName.rfind("/") + 1:], 'w+b') as localFile:
        # Write to file
        localFile.write(fileBytes)
