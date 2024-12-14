import json

def verify_master_password():
    with open("ProPass_written_files/account.json", "r") as file:
        data = json.load(file)
    
    if "master_password" not in data:
        print("Error retrieving master password since there is no account.")
        return None
    else:
        return data["master_password"]

master_password = verify_master_password()
if master_password:
    print("\n")
else:
    print("No master password found.")
