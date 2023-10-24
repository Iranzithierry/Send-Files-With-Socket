"""
Server receiver of the file
"""
import socket
import tqdm
import os
from datetime import datetime

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

client_socket, address = s.accept() 
print(f"[+] {address} is connected.")


received = client_socket.recv(BUFFER_SIZE).decode()

filename, filesize = received.split(SEPARATOR)

filename = os.path.basename(filename)
file_extension = filename.split(".")[1]

filesize = int(filesize)

progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)

with open(f"{datetime.now()}.{file_extension}", "wb") as f:
    while True:
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:    
            break
        f.write(bytes_read)
        progress.update(len(bytes_read))

client_socket.close()
s.close()