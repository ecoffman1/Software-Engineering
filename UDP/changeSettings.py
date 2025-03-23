import json
import os
from UDP.UDP_Client import updateClientSettings
from UDP.UDP_Server import updateServerSettings

# call me when the button is pressed to change json configuration file
# setting is name of setting (ex: "udp_ip")
# newValue is what it will be changed to

# Get the path to config.json
current_script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_script_dir, 'config.json')

def changeSettings(newValues):
    try:
        # read existing configuration
        with open(config_path, "r") as config_file:
            config = json.load(config_file)

        for i,(setting, newValue) in enumerate(newValues.items()):
            # update the specific setting
            config[setting] = newValue
            print(f"Updated '{setting}' to '{newValue}' in config.json")

        # write the updated configuration back to the file
        with open(config_path, "w") as config_file:
            json.dump(config, config_file, indent=4)

    
    except FileNotFoundError:
        print("Error: config.json not found!")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in config.json!")
    
    # Update new settings
    updateServerSettings(newValues)
    updateClientSettings(newValues)

