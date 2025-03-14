import os
import sys
import json
from PIL import Image

class ResourceLoader:
    def __init__(self):
        self.base_path = self.get_base_path()

    def get_base_path(self):
        """Returns the base path depending on whether the app is running in development or packaged mode."""
        if getattr(sys, 'frozen', False):  # Running as a PyInstaller bundle
            return sys._MEIPASS
        else:  # Running in normal development mode
            return os.path.abspath(".")

    def load_image(self, image_name):
        """Load an image, ensuring compatibility with development and packaged environments."""
        image_path = os.path.join(self.base_path, image_name)
        try:
            image = Image.open(image_path)
            return image
        except FileNotFoundError:
            raise Exception(f"Image {image_name} not found at path: {image_path}")

    def load_json(self, json_name):
        """Load a JSON configuration file."""
        json_path = os.path.join(self.base_path, json_name)
        try:
            with open(json_path, "r") as f:
                config = json.load(f)
            return config
        except FileNotFoundError:
            raise Exception(f"Config file {json_name} not found at path: {json_path}")

