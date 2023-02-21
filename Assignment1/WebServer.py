# Assignment 1
# Avery Brinkman

import mimetypes
import os
import socket
import threading
from typing import Tuple

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 6789
CLRF = "\r\n"


def processRequest(requestData: str) -> str:
  # Split each line apart
  requestData_lines = requestData.split(CLRF)

  # Print out the request
  print()
  print("============REQUEST============")
  for line in requestData_lines:
    if line == '': break
    print(line)
  print("===============================")
  print()

  # Get the request line and split it up
  requestLine = requestData_lines[0].split(" ")
  # Get the file name
  fileName = "." + requestLine[1]

  return fileName


def processResponse(fileName: str) -> bytes:
  statusLine = "HTTP/1.1 "
  contentType = "Content-Type: "

  validFile = os.path.isfile(fileName)
  if validFile:
    with open(fileName, "rb") as file:
      statusLine += "200 OK" + CLRF
      contentType += mimetypes.guess_type(file.name)[0] + CLRF
      body = file.read()
  else:
    statusLine += "404 Not Found" + CLRF
    contentType += "text/html; charset=UTF-8" + CLRF
    body = "<HTML><HEAD><TITLE>Not Found</TITLE></HEAD><BODY>Not Found</BODY></HTML>"

  responseHeaders = statusLine + contentType + CLRF
  
  print()
  print("============RESPONSE============")
  print(responseHeaders)
  if not validFile:
    print(body)
    body = bytes(body, encoding="utf-8")
  print("================================")
  print()

  return bytes(responseHeaders, encoding="utf-8") + body


def handleHTTP(connection: socket.socket):
  # Context manager to close socket when done
  with connection:
    # Get 1024 bytes of data and decode as utf-8
    requestData_text = connection.recv(1024).decode('utf-8')
    
    requestedFile = processRequest(requestData_text)
    httpResponse = processResponse(requestedFile)

    connection.send(httpResponse)


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
    httpThread = threading.Thread(target=handleHTTP, args=(connection,))
    # Start the new thread and continue execution to handle the next connection
    httpThread.start()
