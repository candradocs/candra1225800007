from socket import *
import sys

# Check if arguments are correct
if len(sys.argv) != 4:
    print("Usage: python HttpClient.py <server> <port> <filename>")
    sys.exit()

serverName = sys.argv[1]
serverPort = int(sys.argv[2])
filename = sys.argv[3]

# Create TCP socket
clientSocket = socket(AF_INET, SOCK_STREAM)

try:
    # Connect to the server
    clientSocket.connect((serverName, serverPort))

    # Prepare GET request
    request = f"GET /{filename} HTTP/1.1\r\nHost: {serverName}\r\n\r\n"

    # Send request
    clientSocket.send(request.encode())

    # Receive and print response
    while True:
        response = clientSocket.recv(4096)
        if not response:
            break
        print(response.decode(), end="")

except Exception as e:
    print("Error:", e)

finally:
    clientSocket.close()
