import json
import os
import time
import datetime
import sys
import termios
import tty
import uuid
import re
import platform
import subprocess

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_user_ID():
    return str(uuid.uuid4())

def input_with_dots(prompt=""):
    password = ""
    if sys.platform == "win32":
        import msvcrt
        print(prompt, end='', flush=True)
        while True:
            ch = msvcrt.getch()
            if ch in [b'\r', b'\n']:
                print()
                break
            elif ch == b'\x08':
                if password:
                    password = password[:-1]
                    print('\b \b', end='', flush=True)
            else:
                password += ch.decode('utf-8')
                print('*', end='', flush=True)
    else:
        print(prompt, end='', flush=True)
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
                    if password:
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

def is_valid_email(email):
    # Basic email validation regex
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def create_account():
    email_min_length = 3
    email_max_length = 75
    password_min_length = 8
    password_max_length = 40
    timestamp = datetime.datetime.now()

    while True:
        clear_screen()
        print("ProPass: CLI Password Manager")
        print("Create an account to use ProPass.\n")

        email_input = input("Your email: ").strip()
        email_length = len(email_input)

        if email_length < email_min_length or not is_valid_email(email_input):
            print(f"Invalid email. Please enter a valid email address with at least {email_min_length} characters.")
            time.sleep(1)
            continue

        if email_length > email_max_length:
            print(f"Your email is too long. Must be no more than {email_max_length} characters.")
            time.sleep(1)
            continue

        while True:
            password_input = input_with_dots("Password: ")
            if len(password_input) < password_min_length:
                print(f"Password too short. Must be at least {password_min_length} characters.")
                time.sleep(1)
                continue
            if len(password_input) > password_max_length:
                print(f"Password too long. Must be no more than {password_max_length} characters.")
                time.sleep(1)
                continue

            confirm_password = input_with_dots("Confirm Password: ")
            if password_input != confirm_password:
                print("Passwords do not match. Please try again.")
                time.sleep(1)
                continue

            master_password = input_with_dots("Master Password: ")
            confirm_master_password = input_with_dots("Confirm Master Password: ")
            if master_password != confirm_master_password:
                print("Master passwords do not match. Please try again.")
                time.sleep(1)
                continue

            clear_screen()
            print("Verify your information:\n")
            print(f"Your email: {email_input}")
            print(f"Password: {'*' * len(password_input)}")
            print(f"Master Password: {'*' * len(master_password)}")
            verification_input = input("Is this information correct? (Y/N): ").strip().upper()
            if verification_input == "Y":
                user_ID = create_user_ID()
                account_data = {
                    "email": email_input,
                    "password": password_input,
                    "master_password": master_password,
                    "user_ID": user_ID,
                    "time_of_creation": timestamp.isoformat(),
                    "is_student_account?": False,
                    "is_premium_subscriber?": False
                }
                
                folder_path = 'ProPass_written_files'
                os.makedirs(folder_path, exist_ok=True)
                file_path = os.path.join(folder_path, 'account.json')

                try:
                    with open(file_path, "w") as json_file:
                        json.dump(account_data, json_file, indent=4)
                    clear_screen()
                    print("ProPass account created. Welcome!")
                except Exception as e:
                    print(f"Error creating account: {e}")
                return

def check_for_account():
    folder_path = 'ProPass_written_files'
    file_path = os.path.join(folder_path, 'account.json')

    if os.path.exists(file_path):
        print("Account already exists.")
    else:
        create_account()

def get_system_type():
    """
    Returns the system type as 'Windows', 'macOS', or 'Linux'.
    """
    system = platform.system()
    if system == "Windows":
        return "Windows"
    elif system == "Darwin":  # macOS
        return "macOS"
    elif system == "Linux":
        return "Linux"
    else:
        return "Unknown"

def find_directory(directory_name, search_paths):
    for path in search_paths:
        for root, dirs, _ in os.walk(path):
            if directory_name in dirs:
                return os.path.join(root, directory_name)
    return None

def rename_password_file(directory_path):
    """
    Renames any JSON file to 'passwords.json' in the specified directory.
    """
    for filename in os.listdir(directory_path):
        if filename.endswith(".json") and filename != "passwords.json":
            old_path = os.path.join(directory_path, filename)
            new_path = os.path.join(directory_path, "passwords.json")
            os.rename(old_path, new_path)
            print(f"Renamed '{filename}' to 'passwords.json'")

if __name__ == "__main__":
    check_for_account()

    os.system('cls' if os.name == 'nt' else 'clear')

    print("Your ProPass account has been created. \nWould you like to import your passwords from another app (using a JSON file)? Y/N")
    import_pass_input = input("")

    if import_pass_input.lower() == "y":
        system_type = get_system_type()
        print(f"\nOperating system type: {system_type}\n")
        time.sleep(0.5)

        directory_name = "ProPass-py"
        search_paths = [
            os.path.expanduser("~/Documents"),
            os.path.expanduser("~/Desktop"),
            os.path.expanduser("~/Projects"), 
            os.path.expanduser("~")
        ]

        found_path = find_directory(directory_name, search_paths)

        if found_path:
            if platform.system() == "Windows":
                subprocess.run(["explorer", found_path])
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", found_path])
            else:
                print(f"Opening directories is not supported on this OS: {platform.system()}")
            
            print(f"\nOpening directory: {found_path}")
            
            # Rename any imported JSON files to 'passwords.json'
            rename_password_file(found_path)
        else:
            print(f"Directory '{directory_name}' not found in specified locations.")

    # os.system('cls' if os.name == 'nt' else 'clear')

    print("Drag a JSON file, containing your passwords into the main directory. Change the JSON's previous title name to: 'passwords.json', otherwise ProPass's full functionality will not work.")
