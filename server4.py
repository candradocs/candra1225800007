from socket import *
import threading
from datetime import datetime

# Helper untuk timestamp
def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# Thread function to handle each client connection
def handle_client(connectionSocket, addr):
    log(f"Thread started for {addr}")

    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()

        # Send HTTP header
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())

        # Send content
        connectionSocket.send(outputdata.encode())

        log(f"Served file '{filename}' to {addr}")

    except IOError:
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send(
            "<html><body><h1>404 Not Found</h1></body></html>".encode()
        )
        log(f"404 Not Found for {addr} ({filename})")

    finally:
        connectionSocket.close()
        log(f"Connection closed for {addr}")


# MAIN THREAD — server listens on a fixed port
def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', 8085))
    serverSocket.listen(5)

    log("Multithreaded Web Server is ready...")

    while True:
        connectionSocket, addr = serverSocket.accept()

        # Buat thread untuk handle request
        thread = threading.Thread(
            target=handle_client,
            args=(connectionSocket, addr)
        )
        thread.start()

        log(f"New connection from {addr} handled in thread {thread.name}")


if __name__ == "__main__":
    main()
