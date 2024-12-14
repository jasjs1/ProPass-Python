import json
import re
import os
import time


def create_account():
    email_min_length = 3
    email_max_length = 75
    password_min_length = 8
    password_max_length = 40

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("ProPass: CLI Password Manager")
        print("\nYou do not have an account with ProPass, please create an account.")
        time.sleep(0.2)
        email_input = input("Your email: ")
        email_length = len(email_input)

        if email_length < email_min_length:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\nYour email is too short. Must be at least {email_min_length} characters. {email_min_length - email_length} more characters needed.")
            continue

        elif email_length > email_max_length:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\nYour email is too long. Must be no more than {email_max_length} characters. {email_length - email_max_length} characters over the limit.")
            continue

        else:
            while True:
                password_input = input("Password: ")
                password_length = len(password_input)

                if password_length < password_min_length:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(f"\nYour password is too short. Must be at least {password_min_length} characters. {password_min_length - password_length} more characters needed.")
                    continue

                elif password_length > password_max_length:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(f"\nYour password is too long. Must be no more than {password_max_length} characters. {password_length - password_max_length} characters over the limit.")
                    continue

                else:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    time.sleep(0.5)
                    print("Creating account...")

                    write_account_data = {
                        "email": email_input,
                        "password": password_input,
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

create_account()
