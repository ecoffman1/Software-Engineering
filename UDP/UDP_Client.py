import socket
import json
import os

import os
import json

# Get the path to config.json
current_script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_script_dir, 'config.json')

# open config file in read mode
with open(config_path, "r") as config_file:
    # read contents and parse as a python dict
    config = json.load(config_file)

# get ip address and port from dictionary
udp_ip = config["udp_ip"]
broadcastPort = config["broadcastPort"]
serverPort = config["receivePort"]

# create a udp socket for transmitting
UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def client(message):

    print(f"Message: {message}")

    # send message to the server
    UDPClientSocket.sendto(message.encode(), (udp_ip, serverPort))

    print(f"Message sent to: {udp_ip}:{broadcastPort}")


    # Wait for server reply
    try:
        response = UDPClientSocket.recvfrom(1024)
        # response from server
        print(f"Response: {response[0]}")
    except socket.timeout:
        print("Timeout: No response")
    except socket.error as e:
        print(f"Socket error: {e}")
    except Exception as e:
        print(f"An unexpected error occured: {e}")

def broadcastEquipmentId(equipmentId):
    print(f"Equipment id: {equipmentId}")

    # Broadcast equipment id
    UDPClientSocket.sendto(equipmentId.encode(), (udp_ip, broadcastPort))
    print(f"Equipment id sent to: {udp_ip}:{broadcastPort}")


    
