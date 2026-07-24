import requests
from logmagix import Logger, LogLevel
import os
from pathlib import Path

log = Logger(
    style=1,
    prefix="Checker",
    level=LogLevel.DEBUG
)

def worker(username):
    url = f"https://www.snapchat.com/@{username}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10,
        )

        response.raise_for_status()
        data = response.text

        if (response.status_code == 200):
            if ("unavailable" in data):
                return "valid"
            else:
                return "invalid"
        else:
            return "invalid"

    except Exception as e:
        return "invalid"

def username_handler():
    usernames_path = os.path.join("..", "data", "input", "usernames.txt")

    if not os.path.exists(usernames_path) or os.stat(usernames_path).st_size == 0:
        log.warning(f"Usernames file not found or empty at: {os.path.abspath(usernames_path)}")
        return None

    with open(usernames_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    username_line = lines[0].strip()
    username_parts = username_line.split(":")

    if len(username_parts) == 2:
        username = username_parts[0]
        with open(usernames_path, "w", encoding="utf-8") as f:
            f.writelines(lines[1:])
    elif len(username_parts) == 1:
        username = username_parts[0]
        with open(usernames_path, "w", encoding="utf-8") as f:
            f.writelines(lines[1:])
    else:
        log.error("Invalid username Format")
        with open(usernames_path, "w", encoding="utf-8") as f:
            f.writelines(lines[1:])
        return None
    
    return username

def username_amount_counter():
    usernames_path = os.path.join("..", "data", "input", "usernames.txt")   

    with open(usernames_path, "r", encoding="utf-8") as file:
        line_count = sum(1 for line in file) 

    return line_count

def main():
    output_folder = Path(__file__).resolve().parent.parent / "data" / "output"
    invalid_path = output_folder / "invalid.txt"
    valid_path = output_folder / "valid.txt"
    choice = int(log.question("Choice(1 = single username | 2 = from file): "))
    print()

    if (choice == 1):
        username = log.question("Username: ")
        status = worker(username)
        if (status == "valid"):
            with open(valid_path, "a") as file:
                file.write(username + "\n")
            log.success(f"VALID\033[37m - Username: {username}\033[0m")
        elif (status == "invalid"):
            with open(invalid_path, "a") as file:
                file.write(username + "\n")
            log.error(f"INVALID\033[37m - Username: {username}\033[0m")
        print()
    elif (choice == 2):
        username_count = username_amount_counter()
        log.info(f"Loaded {username_count} usernames.")
        print()
        for i in range(username_count):
            username = username_handler()
            status = worker(username)
            if (status == "valid"):
                with open(valid_path, "a") as file:
                    file.write(username + "\n")
                log.success(f"VALID\033[37m - Username: {username}\033[0m")
            elif (status == "invalid"):
                with open(invalid_path, "a") as file:
                    file.write(username + "\n")
                log.error(f"INVALID\033[37m - Username: {username}\033[0m")



if __name__ == "__main__":
    main()

