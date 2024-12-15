import json
import os

def verify_master_password():
    file_path = os.path.join("ProPass_written_files", "account.json")
    if not os.path.exists(file_path):
        print("Error retrieving master password since there is no account.")
        return None
    with open(file_path, "r") as file:
        data = json.load(file)
    return data.get("master_password")
