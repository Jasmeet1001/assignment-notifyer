with open(r"C:\Users\Master\Documents\ERPNotifier\usr_word.txt", 'w') as cred:
    username = input("Enter Username/LoginID: ")
    password = input("Enter Password: ")
    cred.write(f"{username},{password}")