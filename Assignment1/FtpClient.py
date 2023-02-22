# Assignment 1
# Avery Brinkman

import socket

CLRF = b"\r\n"

class FtpClient:
  def __init__(self, ftpAddr: str = "127.0.0.1", ftpPort: int = 21):
    self.controlSock: socket.socket
    self.dataPort: int
    self.ftpAddr: str = ftpAddr
    self.ftpPort: int = ftpPort

  def connect(self, username: str, password: str):
    self.controlSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.controlSock.connect((self.ftpAddr, self.ftpPort))
    assert int(self.controlSock.recv(1024)[:3]) == 220

    self.sendCommand("USER " + username, 331)
    self.sendCommand("PASS " + password, 230)

  def disconnect(self):
    self.sendCommand("QUIT", 221)
    self.controlSock.close()

  def sendCommand(self, command: str, expectedResponse: int):
    fullCommand = bytes(command, "utf-8") + CLRF
    self.controlSock.send(fullCommand) 
    serverResponse = self.controlSock.recv(1024)
    assert int(serverResponse[:3]) == expectedResponse
    return serverResponse

  def getDataPort(self, response: str):
    addrPort = response[response.find("(") + 1:response.rfind(")")].split(",")
    portVals = addrPort[-2:]
    return portVals[0] * 256 + portVals[1]

  def getFile(self, fileName: str):
    self.sendCommand("CWD /", 250)
    response = str(self.sendCommand("PASV", 227))
    dataPort = self.getDataPort(response)

a = FtpClient()
a.connect("abrinkman", "admin123")
a.getFile("adfs.txt")
a.disconnect()
