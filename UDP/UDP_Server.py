import socket
import json

with open("config.json", "r") as config_file:
    config = json.load(config_file)

udp_ip = config["udp_ip"]
receivePort = config["receivePort"]
serverMessage = "Hello client, I'm the server!"

def server():

    # create a udp socket for receiving
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # binds the socket to specified ip address and port
    sock.bind((udp_ip, receivePort))

    print(f"Listening on {udp_ip}:{receivePort}")

    # wait for messages from the client
    while True:
        # message received is a tuple: {data, addr}
        # 1024 specifies max size in bytes
        data, addr = sock.recvfrom(1024)
        print(f"Received message from {addr}: {data.decode()}")

        # reply to the client
        sock.sendto(serverMessage.encode(), (udp_ip, receivePort))