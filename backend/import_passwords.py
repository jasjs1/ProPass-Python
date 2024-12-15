import subprocess
import os
import platform
import platform

def import_passwords():
    def get_system_type():
        system = platform.system()
    if system == "Windows":
        return "Windows"
    elif system == "Darwin":
        return "macOS"
    elif system == "Linux":
        return "Linux"
    else:
        return "Unknown system type. Unable to use ProPass."
system_type = get_system_type()
print(f"\nOperating system: {system_type}\n")


def find_directory(directory_name, search_paths):
    for path in search_paths:
        for root, dirs, _ in os.walk(path):
            if directory_name in dirs:
                return os.path.join(root, directory_name)
    return None

directory_name = "ProPass-py"

search_paths = [
    # NOTE: IF PROPASS'S FOLDER IS OUTSIDE OF THESE DIRECTORIES, PROPASS IMPORTING PASSWORDS WILL BE UNABLE TO WORK. IF YOU HAVE SWITCHED PROPASS'S DIRECTORY TO ANOTHER PLACE, PLEASE MOVE IT BACK TO ONE OF THE FOLLOWING FILE PATHS BELOW: #
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
else:
    print(f"Directory '{directory_name}' not found in specified locations.")

os.system('cls' if os.name == 'nt' else 'clear')

print("Drag a JSON file, containing your passwords into the main directory. Change the JSON's previous title name to: 'passwords.json', otherwise ProPass's full functionality will not work. ")