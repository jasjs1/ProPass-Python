import json
import os 

os.system('cls' if os.name == 'nt' else 'clear')


def load_passwords(file_path="passwords.json"):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file: 
            return json.load(file)
        return {}
    
def save_passwords(passwords, file_path="passwords.json"):
    with open(file_path, 'w') as file:
        json.dump(passwords, file, indent=4)
        
def add_password(passwords):
    website = input("What website is using this password? ")
    username = input("ENter the username: ")
    password = getpass("Enter the password: ")
    password [website] = {"USERNAME": username, "PASSWORD": password}
    print(f"Password for {website} has been added sucessfully.")
    
def view_password(passwords):
    website = input("Enter the website to view: ")
    if website in passwords:
        print(f"Website {website}")
        print(f"Username: {passwords[website]['username']}")
        print(f"Password: {passwords[website]['password']}")
    else:
        print(f"No password is on file for {website}")
        
def delete_password(passwords):
    website = input("Enter website to delete: ")
    if website in passwords: 
        del passwords[website]
        print(f"Password for {website} has been deleted. Data has been erased from your local computer for the password on {website}.")
    else:
        print(f"No password has been found for {website}.")
        
        
def main():
    file_path = "passwords.json"
    passwords = load_passwords(file_path)
    
    while True:
        print("\nProPass Password Manager")
        print("1. Add a password to ProPass.")
        print("2. View a password that has been saved onto ProPass.")
        print("3. Delete a password that has been save to ProPass.")
        print("4. Exit/Terminate program.")
        
        choice = input("Choice: ")
        
        if choice == '1':
            add_password(passwords)
        elif choice == '2':
            view_password(passwords)
        elif choice == '3':
            delete_password(passwords)
        elif choice == '4':
            break
        else:
            print("Invalid. Must choose a number between 1 and 4 for ProPass to function.")
            
if __name__ == "__main__":
    main()
