import json
import os

current_script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_script_dir, 'config.json')

def getSettings():
    try:
        # read existing configuration
        with open(config_path, "r") as config_file:
            config = json.load(config_file)

        return {
            "udp_ip": config.get("udp_ip", "127.0.0.1"),
            "broadcastPort": config.get("broadcastPort", 7500),
            "receivePort": config.get("receivePort", 7501),
        }

    except FileNotFoundError:
        print("Error: config.json not found!")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in config.json!")
    
    return {
        "udp_ip": "127.0.0.1",
        "broadcastPort": 7500,
        "receivePort": 7501
    }