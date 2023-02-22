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

    self.disconnect()

  def disconnect(self):
    self.sendCommand("QUIT", 221)
    self.controlSock.close()

  def sendCommand(self, command: str, expectedResponse: int):
    fullCommand = bytes(command, "utf-8") + CLRF
    self.controlSock.send(fullCommand) 
    serverResponse = self.controlSock.recv(1024)
    assert int(serverResponse[:3]) == expectedResponse

a = FtpClient()
a.connect("abrinkman", "admin123")
