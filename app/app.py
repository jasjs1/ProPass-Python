import json
import os
import time
import tkinter as tk

def clear_screen():
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
    username = input("Enter the username: ")
    password = input("Enter the password: ")
    passwords[website] = {"username": username, "password": password} 
    print(f"Password for {website} has been added successfully.")
    time.sleep(1)

def view_password(passwords):
    website = input("Enter the website to view: ")
    if website in passwords:
        print(f"Website: {website}")
        print(f"Username: {passwords[website]['username']}") 
        print(f"Password: {passwords[website]['password']}") 
    else:
        print(f"No password is on file for {website}")
    time.sleep(1)

def delete_password(passwords):
    website = input("Enter website to delete: ")
    if website in passwords:
        del passwords[website]
        print(f"Password for {website} has been deleted. Data has been erased from your local computer for the password on {website}.")
    else:
        print(f"No password has been found for {website}.")
    time.sleep(1)
        
def create_gui_window():
    window = tk.Tk()
    window.title("ProPass")
    window.geometry("850x800")
    
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = 850
    window_height = 800
    position_top = int(screen_height/2 - window_height/2)
    position_right = int(screen_width/2 - window_width/2)
    window.geometry(f"+{position_right}+{position_top}")
    
    
    return window

def main():
    file_path = "passwords.json"
    passwords = load_passwords(file_path)
    window = None

    while True:
        clear_screen()
        print("\nPROPASS PASSWORD MANAGER")
        print("1. Add a password to ProPass.")
        print("2. View a password that has been saved onto ProPass.")
        print("3. Delete a password that has been saved to ProPass.") 
        print("4. Open ProPass in a window.")
        print("5. Exit/Terminate program.")

        choice = input("\nChoice: ")

        if choice == '1':
            add_password(passwords)
        elif choice == '2':
            view_password(passwords)
        elif choice == '3':
            delete_password(passwords)
        elif choice == '4':
            if window is None:
            window = create_gui_window()
            window.deiconify()
            window.mainloop()
        elif choice == '5':
            break
        else:
            print("Invalid. Must choose a number between 1 and 5 for ProPass to function.")
            time.sleep(1)

        save_passwords(passwords, file_path)

if __name__ == "__main__":
    main()
