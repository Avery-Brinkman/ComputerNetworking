# Assignment 1
# Avery Brinkman

import socket
import threading

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 6789  # Port to listen on (non-privileged ports are > 1023)

def processHTTP(connection: socket.socket):
  # Context manager to close socket when done
  with connection:
    # Get 1024 bytes of data and decode as utf-8
    requestData_text = connection.recv(1024).decode('utf-8')
    # Split each line apart
    requestData_lines = requestData_text.split('\r\n')

    # Get the request line and split it up
    requestLine = requestData_lines[0].split(" ")
    # Get the file name
    fileName = requestLine[1]

    # Print out the request
    print()
    print("============REQUEST============")
    for line in requestData_lines:
      if line == '': break
      print(line)
    print("===============================")
    print()

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
    httpThread = threading.Thread(target=processHTTP, args=(connection,))
    # Start the new thread and continue execution to handle the next connection
    httpThread.start()
