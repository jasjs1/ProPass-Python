import json
import os
import time
import random
import termios
import sys
import tty
import uuid
from datetime import datetime
from account.account import check_for_account, create_account
from backend.verify_master_password import verify_master_password
from backend.get_list_of_websites import extract_titles
from backend.app_func.load_passwords import load_passwords

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

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
                sys.stdout.write('*')
                sys.stdout.flush()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return password

def add_password(passwords):
    website = input("What website is using this password? ")
    username = input("Enter the username: ")
    password = input_with_dots("Enter the password: ")
    timestamp = datetime.now().isoformat()  
    unique_id = str(uuid.uuid4()) 

    passwords[website] = {
        "username": username,
        "password": password,
        "timestamp": timestamp,
        "UUID": unique_id
    }
    print(f"Password for {website} has been added successfully.")
    time.sleep(1)

def view_password(passwords):
    while True:
        website = input("\nEnter the website to view (type /list to view all of the websites stored): ")

        titles = extract_titles()

        if website == "/list":
            if titles:
                print("Saved websites with passwords:\n")
                for title in titles:
                    print(f"- {title.title()}")
                print()
            else:
                print("No websites found.")
            continue

        if website not in titles:
            print("Invalid website selection. Please choose a valid website from the list.")
            continue 

        master_password_input = input_with_dots("Your master password: ")

        stored_master_password = verify_master_password()

        if stored_master_password is None:
            print("Could not retrieve master password. Exiting...")
            return

        if master_password_input == stored_master_password:
            if website in passwords:
                print(f"\nWebsite: {website}")
                print(f"Username: {passwords[website]['username']}")
                print(f"Password: {passwords[website]['password']}")
                print(f"Timestamp: {passwords[website]['timestamp']}")
                print(f"UUID: {passwords[website]['UUID']}")
            else:
                print(f"No password is on file for {website}")
            break
        else:
            print("Incorrect master password. Access denied.")

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

def main():
    check_for_account()

    file_path = "passwords.json"
    passwords = load_passwords(file_path)

    while True:
        clear_screen()
        print("\nPROPASS PASSWORD MANAGER")
        print("1. Add a password to ProPass.")
        print("2. View a password that has been saved onto ProPass.")
        print("3. Delete a password that has been saved to ProPass.")
        print("4. Exit/Terminate program.")

        choice = input("\nChoice: ")

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
            time.sleep(1)

        save_passwords(passwords, file_path)

if __name__ == "__main__":
    main()
