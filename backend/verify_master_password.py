import json

def get_master_password():
    with open("ProPass_written_files/account.json", "r") as file:
        data = json.load(file)
    
    # Check if the "master_password" key is in the JSON data
    if "master_password" not in data:
        print("Error retrieving master password since there is no account.")
        return None
    else:
        return data["master_password"]

master_password = get_master_password()
if master_password:
    print("Master password:", master_password)
else:
    print("No master password found.")
