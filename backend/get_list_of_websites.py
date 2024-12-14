import json

def extract_titles(file_path="password.json"):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file) 
            titles = list(data.keys())
            return titles
    except FileNotFoundError:
        print("The passwords file was not found.")
        return []  
    except json.JSONDecodeError:
        print("Error decoding the JSON file.")
        return []
