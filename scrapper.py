import json
import requests as rq
import time
from bs4 import BeautifulSoup as bS

def login_info(user_id, password):
    
    s = rq.Session()

    sucess = 'https://www.icloudemserp.com:443/corecampus/admin/settings/checktasks_student.php?page=1&refresh=true'

    payload = {
        'branchid': '1',
        'typefunc': '',
        'userid': user_id,
        'pass_word': password,
        'uotpid': '',
        'branchid': '9',
    }
    
    url_main = s.get('https://www.icloudemserp.com/mrei')
    request_ = s.post('https://www.icloudemserp.com:443/corecampus/checkuser1.php', data = payload)
    
    print(f"icloudems returned status code {url_main.status_code}")
    
    if (request_.url == sucess):
        print("Login Sucessful!!\n")
        time.sleep(3)
    else:
        print("Login Failed!!\n")
        exit()

    return s

def get_assignments(link, session):
    assignment = session.get(f"https://www.icloudemserp.com/corecampus/student/{link}")
    assignment_soup = bS(assignment.content, 'lxml')
        
    nester = {}
    index = 1
    count = 0
    table_body = assignment_soup.find('table')
        
    for tbl_val in table_body.find_all('a'):
        print_val = tbl_val.text.replace('\n', '').strip()

        if (print_val == '' or print_val == ' ' or print_val == None):
            continue
        else:
            count += 1
            match (count):
                case 1:
                    nester[index] = [print_val]
                case 2:
                    nester[index].append(print_val)
                case 3:
                    nester[index].append(print_val)
                    index += 1
                    count = 0
              
    index = index - 1
    sorted_dict = dict(sorted(nester.items(), reverse = True))
    del nester
    
    try:
        with open("assignment_list.json", "r") as exis_list:
            assig_list = json.load(exis_list)
            index_val = list(map(int, list(dict.fromkeys(assig_list))))
            
            if (index > index_val[0]):
                print(f"You have {index - index_val[0]} new assignments.")
                for new in range(index - index_val[0]):    
                    count_new = 0
                    for val in sorted_dict[index - new]:    
                        count_new += 1
                        match (count_new):
                            case 1:
                                print(f"Due Date: {val}")
                            case 2:
                                print(f"Subject: {val}")
                            case 3:
                                print(f"Assignment Name: {val}\n")
                                count_new = 0
            else:
                print("You have no new assignments.")

    except FileNotFoundError:
        with open("assignment_list.json", "w") as new_list:
            json.dump(dict(sorted_dict), new_list, indent = 4)
            count_first = 0
            for row in sorted_dict.items():
                for col in row[1]:
                    count_first += 1
                    match (count_first):
                        case 1:
                            print(f"Due Date: {col}")
                        case 2:
                            print(f"Subject: {col}")
                        case 3:
                            print(f"Assignment Name: {col}\n")
                            count_first = 0

    index = 0
    
try:
    with open("usr_word.json", "r") as log:
        login_info_file = json.load(log)
        login_session = login_info(login_info_file['username'], login_info_file['password'])

except FileNotFoundError:
    userid = input("Enter username: ")
    password = input("Enter password: ")

    with open("usr_word.json", "w") as log_write:
        json.dump({"username": userid, "password": password}, log_write, indent = 4)
        login_session = login_info(userid, password)
    
dashboard = login_session.get('https://www.icloudemserp.com/corecampus/student/student_index.php')

soup = bS(dashboard.content, 'lxml')
assig_page = soup.find('div', class_ = 'col-md-2 col-sm-3 text-center').find('a').get('href')

while True:
    get_assignments(assig_page, login_session)
    interval = 10
    time.sleep(interval)
    
