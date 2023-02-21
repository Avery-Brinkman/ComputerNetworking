import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 55555  # Port to listen on (non-privileged ports are > 1023)

# Create an internet socket (AF_INET) using TCP (SOCK_STREAM)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
  # Sets up the socket to listen on HOST:PORT
  sock.bind((HOST, PORT))
  # Start listening
  sock.listen()
  # Block execution and wait for a connection from addr = (host, port)
  connection, addr = sock.accept()
  with connection:
    print(f"Client at {addr} has connected!")
    while True:
      data = connection.recv(1024)
      if not data:
        break
      else:
        print(data)
      connection.sendall(data)
