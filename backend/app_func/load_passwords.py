import os
import json

def load_passwords(file_path="passwords.json"):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {}

def loadpass(file_path="passwords.json"):
    # Placeholder for loadpass logic
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {}