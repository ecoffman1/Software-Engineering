import socket
import json
import os
from UDP.UDP_Client import client

# Get the path to config.json
current_script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_script_dir, 'config.json')

with open(config_path, "r") as config_file:
    config = json.load(config_file)

udp_ip = config["udp_ip"]
receivePort = config["receivePort"]
serverMessage = "Hello client, I'm the server!"

def server(callback = None):

    # create a udp socket for receiving
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:

        # binds the socket to specified ip address and port
        sock.bind((udp_ip, receivePort))

        print(f"Listening on {udp_ip}:{receivePort}")

        # wait for messages from the client
        while True:
            # message received is a tuple: {data, addr}
            # 1024 specifies max size in bytes
            data, address = sock.recvfrom(1024)
            message = data.decode()
            print(f"Received message from {address}: {message}")

            # reply to the traffic generator only the player that got hit
            parts = message.strip().split(":")
            shooter_id = parts[0]
            hit_id = parts[1]
            
            friendlyFire = False
            
            if callback:
                friendlyFire = callback(shooter_id.strip(), hit_id.strip())
                
            if friendlyFire:
                client(shooter_id)
            else:
                client(hit_id)
            
    except Exception as e:
        print(f"Error occurred: {e}")

def updateServerSettings(inputs):
    # Update global variables based on the new inputs
    global udp_ip, receivePort

    # Set the values
    for setting, newValue in inputs.items():
        if setting == "udp_ip":
            udp_ip = newValue
        elif setting == "receivePort":
            receivePort = newValue
