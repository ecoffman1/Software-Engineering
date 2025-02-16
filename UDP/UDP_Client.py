import socket
import json

# open config file in read mode
with open("UDP/config.json", "r") as config_file:
    # read contents and parse as a python dict
    config = json.load(config_file)

# get ip address and port from dictionary
udp_ip = config["udp_ip"]
broadcastPort = config["broadcastPort"]

# create a udp socket for transmitting
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def client(message):

    print(f"Player id: {message}")

    # send message to the server
    sock.sendto(message.encode(), (udp_ip, broadcastPort))

    print(f"Id sent to: {udp_ip}:{broadcastPort}")

    try:

        # response from server
        response, _ = sock.recvfrom(1024)
        print(f"Response: {response.decode()}")
    except socket.timeout:
        print("Timeout: No response")
    except socket.error as e:
        print(f"Socket error: {e}")
    except Exception as e:
        print(f"An unexpected error occured: {e}")