import json
import os
import time
import tkinter as tk
import threading
import sys
import termios
import tty
import getpass
import random
from account.account import check_for_account, create_account
from backend.verify_master_password import verify_master_password

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

def input_with_dots(prompt=""):
    print(prompt, end='', flush=True)
    password = ""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        while True:
            char = sys.stdin.read(1)
            if char in ('\n', '\r'):
                print()
                break
            elif char == '\x7f':
                if len(password) > 0:
                    password = password[:-1]
                    sys.stdout.write('\b \b')
                    sys.stdout.flush()
            else:
                password += char
                sys.stdout.write('*' + ' ')
                sys.stdout.flush()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return password

def add_password(passwords):
    website = input("What website is using this password? ")
    username = input("Enter the username: ")
    password = input_with_dots("Enter the password: ")
    passwords[website] = {"username": username, "password": password}
    print(f"Password for {website} has been added successfully.")
    time.sleep(1)


def view_password(passwords):
    website = input("Enter the website to view: ")
    master_password_input = input("Your master password: ")
    

    stored_master_password = verify_master_password()

    if stored_master_password is None:
        print("Could not retrieve master password. Exiting...")
        return

    if master_password_input == stored_master_password:
        if website in passwords:
            print(f"\nWebsite: {website}")
            print(f"Username: {passwords[website]['username']}")
            print(f"Password: {passwords[website]['password']}")
        else:
            print(f"No password is on file for {website}")
    else:
        print("Incorrect master password. Access denied.")
    
    time.sleep(5)


def delete_password(passwords):
    website = input("Enter website to delete: ")
    if website in passwords:
        del passwords[website]
        print(f"Password for {website} has been deleted.")
    else:
        print(f"No password has been found for {website}.")
    time.sleep(1)

def generate_password():
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890/.,';:'[]\\|][{=}-_)(*&^%$#@!)"
    password = ''.join(random.choice(characters) for _ in range(40))
    return password

def create_gui_window():
    def handle_generate():
        password = generate_password()
        password_label.config(text=password)

    window = tk.Tk()
    window.title("ProPass Password Generator")
    
    # Center the window on the screen
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = 400
    window_height = 200
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    generate_button = tk.Button(window, text="Generate Password", command=handle_generate, bg="blue")
    generate_button.pack(pady=20)

    generated_pass_label = tk.Label(window, text="Your generated password:")
    generated_pass_label.pack()
    password_label = tk.Label(window, text="", wraplength=380, justify="center")
    password_label.pack(pady=20)

    window.mainloop()

def open_gui_thread():
    threading.Thread(target=create_gui_window, daemon=True).start()

def main():
    # Check for account
    check_for_account()

    file_path = "passwords.json"
    passwords = load_passwords(file_path)

    while True:
        clear_screen()
        print("\nPROPASS PASSWORD MANAGER")
        print("1. Add a password to ProPass.")
        print("2. View a password that has been saved onto ProPass.")
        print("3. Delete a password that has been saved to ProPass.")
        print("4. Open ProPass in a window (Password Generator).")
        print("5. Exit/Terminate program.")

        choice = input("\nChoice: ")

        if choice == '1':
            add_password(passwords)
        elif choice == '2':
            view_password(passwords)
        elif choice == '3':
            delete_password(passwords)
        elif choice == '4':
            open_gui_thread()
        elif choice == '5':
            break
        else:
            print("Invalid. Must choose a number between 1 and 5 for ProPass to function.")
            time.sleep(1)

        save_passwords(passwords, file_path)

if __name__ == "__main__":
    main()
