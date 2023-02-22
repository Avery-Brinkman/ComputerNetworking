# Assignment 1
# Avery Brinkman

import mimetypes
import os
import socket
import threading
from FtpClient import FtpClient

CLRF = "\r\n"

# FTP username and password
USERNAME = "abrinkman"
PASSWORD = "admin123"

# localhost and default port constants
HOST = "127.0.0.1"
PORT = 6789


class HttpServer:
  # Takes HTML request text and returns the requested file name
  def processRequest(self, requestData: str) -> str:
    # Split each line apart
    requestData_lines = requestData.split(CLRF)

    # Print out the request
    print()
    print("============REQUEST============")
    for line in requestData_lines:
      if line == '':
        break
      print(line)
    print("===============================")
    print()

    # Get the request line and split it up
    requestLine = requestData_lines[0].split(" ")
    # Get the file name
    fileName = "." + requestLine[1]

    return fileName

  # Takes a file name and creates a relevant HTTP response (returned as bytes)
  def processResponse(self, fileName: str) -> bytes:
    notFoundBody = "<HTML><HEAD><TITLE>Not Found</TITLE></HEAD><BODY>Not Found</BODY></HTML>"

    statusLine = "HTTP/1.1 "
    contentType = "Content-Type: "
    body = b""

    # Check that file exists
    validFile = os.path.isfile(fileName)
    # If not try and get from FTP
    if not validFile:
      try:
        ftpClient = FtpClient()
        # Connect w username and password
        ftpClient.connect(USERNAME, PASSWORD)
        # Get the file
        ftpClient.getFile(fileName)
        # Close the connection
        ftpClient.disconnect()
        # Check for file again
        validFile = os.path.isfile(fileName)
      except Exception as e:
        print(e)

    # Open file if we have it
    if validFile:
      with open(fileName, "rb") as file:
        statusLine += "200 OK" + CLRF
        # Set the content type
        type = mimetypes.guess_type(file.name)[0]
        if type:
          contentType += type + CLRF
        else:
          contentType += "application/octet-stream" + CLRF
        # Get bytes from file
        body = file.read()
    else:
      statusLine += "404 Not Found" + CLRF
      contentType += "text/html; charset=UTF-8" + CLRF

    responseHeaders = statusLine + contentType + CLRF

    # Print response to console
    print()
    print("============RESPONSE============")
    print(responseHeaders)
    # Show body if no file found
    if not validFile:
      print(notFoundBody)
      # Convert the raw HTML strign to bytes to send
      body = bytes(notFoundBody, encoding="utf-8")
    print("================================")
    print()

    return bytes(responseHeaders, encoding="utf-8") + body

  def handleHTTP(self, connection: socket.socket):
    # Context manager to close socket when done
    with connection:
      # Get 1024 bytes of data and decode as utf-8
      requestData_text = connection.recv(1024).decode('utf-8')

      # Skip if the TCP connection doesn't actually contain an HTTP request
      if requestData_text == "":
        return

      # Get the file name from the HTTP request
      requestedFile = self.processRequest(requestData_text)
      # Form the response bytes
      httpResponse = self.processResponse(requestedFile)

      # Send the response bytes
      connection.send(httpResponse)

  def startServer(self):
    # Create an internet socket (AF_INET) using TCP (SOCK_STREAM)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
      # Sets up the socket to listen on HOST:PORT
      sock.bind((HOST, PORT))
      # Start listening
      sock.listen()

      # Run until interrupt
      while True:
        # Block execution and wait for a connection from addr = (host, port)
        connection, addr = sock.accept()

        # Create a new thread to handle the connection
        httpThread = threading.Thread(target=self.handleHTTP, args=(connection,))
        # Start the new thread and continue execution to handle the next connection
        httpThread.start()


if __name__ == "__main__":
  httpServer = HttpServer()
  httpServer.startServer()
