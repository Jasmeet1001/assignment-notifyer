import os

file_to_create = os.path.join(rf"{os.path.expanduser('~')}\Documents\ERPNotifier", "usr_word.txt")

if not os.path.exists(file_to_create):
    os.mkdir(rf"{os.path.expanduser('~')}\Documents\ERPNotifier")

with open(file_to_create, 'w') as cred:
    username = input("Enter Username/LoginID: ")
    password = input("Enter Password: ")
    cred.write(f"{username},{password}")