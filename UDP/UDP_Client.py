import socket
import json

# open config file in read mode
with open("config.json", "r") as config_file:
    # read contents and parse as a python dict
    config = json.load(config_file)

# get ip address and port from dictionary
udp_ip = config["udp_ip"]
broadcastPort = config["broadcastPort"]

# create a udp socket for transmitting
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def client(message):

    # send message to the server
    sock.sendto(message.encode(), (udp_ip, broadcastPort))

    print(f"Message sent to: {udp_ip}:{broadcastPort}")

    # response from server
    response, _ = sock.recvfrom(1024)
    print(f"Response: {response.decode()}")