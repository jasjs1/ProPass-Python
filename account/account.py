import json
import os
import time
import sys
import termios
import tty

def input_with_dots(prompt=""):
    password = ""
    if sys.platform == "win32":
        import msvcrt
        print(prompt, end='', flush=True)
        while True:
            ch = msvcrt.getch()
            if ch == b'\r' or ch == b'\n':
                print()
                break
            elif ch == b'\x08':
                if len(password) > 0:
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
                    if len(password) > 0:
                        password = password[:-1]
                        sys.stdout.write('\b \b')
                        sys.stdout.flush()
                else:
                    password += char
                    sys.stdout.write('*' + " ")
                    sys.stdout.flush()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return password


def create_account():
    email_min_length = 3
    email_max_length = 75
    password_min_length = 8
    password_max_length = 40

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("ProPass: CLI Password Manager")
        print("To be able to use ProPass, you must create an account to use our software. This won't take long! Create your account below.")
        print("\nYou do not have an account with ProPass, please create an account.\n")
        time.sleep(0.2)

        email_input = input("Your email: ")
        email_length = len(email_input)

        if email_length < email_min_length:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\nYour email is too short. Must be at least {email_min_length} characters. {email_min_length - email_length} more characters needed.")
            continue

        if email_length > email_max_length:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\nYour email is too long. Must be no more than {email_max_length} characters. {email_length - email_max_length} characters over the limit.")
            continue

        while True:
            password_input = input_with_dots("Password: ")
            password_length = len(password_input)

            if password_length < password_min_length:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"\nYour password is too short. Must be at least {password_min_length} characters. {password_min_length - password_length} more characters needed.")
                continue

            if password_length > password_max_length:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"\nYour password is too long. Must be no more than {password_max_length} characters. {password_length - password_max_length} characters over the limit.")
                continue

            time.sleep(0.5)
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Email: {email_input}")
            print(f"Password: {password_input}\n")
            print("One last thing. We need for you to create a master password to view passwords on ProPass, please make this password something that you will remember and is secure.")
            master_password = input_with_dots("Master Password: ")
            os.system('cls' if os.name == 'nt' else 'clear')
            time.sleep(0.5)
            print("Creating account...")

            write_account_data = {
                "email": email_input,
                "password": password_input,
                "master_password": master_password,
                "is_student_account?": False,
                "is_premium_subscriber?": False
            }

            folder_path = 'ProPass_written_files'
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            file_path = os.path.join(folder_path, 'account.json')

            with open(file_path, "w") as json_file:
                json.dump(write_account_data, json_file, indent=4)

            print("ProPass account created. Welcome to the new way for storing passwords in the command line.")
            return


def check_for_account():
    folder_path = 'ProPass_written_files'
    file_path = os.path.join(folder_path, 'account.json')

    if os.path.exists(file_path):
        print("Account already exists.")
    else:
        create_account()


check_for_account()
