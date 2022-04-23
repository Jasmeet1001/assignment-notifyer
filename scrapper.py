import json
import requests as rq
import time
import datetime as dt
from plyer import notification
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
        time.sleep(2)
    else:
        print("Login Failed!!\n")
        exit()

    return s

def is_late(due_date_p):
    if (len(due_date_p) == 3):
        due_date_format = f"{due_date_p[2]}-{due_date_p[1]}-{due_date_p[0]}"
        if (dt.date.today() >= dt.date.fromisoformat(due_date_format)):
            return True
        else:
            return False           

def get_assignments(link, session):
    try:
        assignment = session.get(f"https://www.icloudemserp.com/corecampus/student/{link}")
    except:
        print("Please! Check your internet connection.")

    assignment_soup = bS(assignment.content, 'lxml')
        
    nester = {}
    index = 1
    count = 0
    skipper = 1
    table_body = assignment_soup.find('table')
        
    for tbl_val in table_body.find_all('a'):
        print_val = tbl_val.text.replace('\n', '').strip()

        if (print_val == '' or print_val == ' ' or print_val == None):
            continue
        else:
            if (skipper == 1 or skipper == 4):
                if (skipper == 4):
                    skipper = 1

                due_date = print_val.split('/')
                if (is_late(due_date)):
                    skipper += 1
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

            elif (skipper == 2 or skipper == 3):
                skipper += 1
                continue
                
    index = index - 1
    sorted_dict = dict(sorted(nester.items(), reverse = True))
    del nester
    
    try:
        with open("assignment_list.json", "r") as exis_list:
            assig_list = json.load(exis_list)
            index_val = list(map(int, list(dict.fromkeys(assig_list))))
            
            if (index > index_val[0]):
                notification.notify(
                    title = "ERP assignment notifier",
                    message = f"You have {index - index_val[0]} new assignments.",
                    timeout = 3
                )
            else:
                notification.notify(
                    title = "ERP assignment notifier",
                    message = "You have no new assignments.",
                    timeout = 3
                )

    except FileNotFoundError:
        with open("assignment_list.json", "w") as new_list:
            json.dump(dict(sorted_dict), new_list, indent = 4)
            notification.notify(
                title = "ERP assignment notifier",
                message = f"You have {index} pending assignments\n\nNewest assignment:\nDue Date: {sorted_dict[1][0]}\nSubject: {sorted_dict[1][1]}\nAssignment Name: {sorted_dict[1][2]}",
                timeout = 3
            )
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
