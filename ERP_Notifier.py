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
    
    try:
        url_main = s.get('https://www.icloudemserp.com/mrei')
        request_ = s.post('https://www.icloudemserp.com:443/corecampus/checkuser1.php', data = payload)
        notification.notify(
            title = "ERP assignment notifier",
            message = "Login Successful!!",
            timeout = 3,
            app_name = "ERP"
        )
    except rq.exceptions.ConnectionError:
        notification.notify(
            title = "ERP assignment notifier",
            message = "Please! Check your internet connection.",
            timeout = 3,
            app_name = "ERP"
        )
        exit()

    return s

def is_late(due_date_p):
    if (len(due_date_p) == 3):
        due_date_format = f"{due_date_p[2]}-{due_date_p[1]}-{due_date_p[0]}"
        if (dt.date.today() > dt.date.fromisoformat(due_date_format)):
            return True
        else:
            return False           

def get_assignments(link, session):
    assignment = session.get(f"https://www.icloudemserp.com/corecampus/student/{link}")
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
        with open(r"C:\Users\Master\Documents\ERPNotifier\assignment_list.json", "r") as exis_list:
            assig_list = json.load(exis_list)
            index_val = list(map(int, list(dict.fromkeys(assig_list))))
            
            if (index > index_val[0]):
                notification.notify(
                    title = "ERP assignment notifier",
                    message = f"You have {index - index_val[0]} new assignments.",
                    timeout = 3,
                    app_name = "ERP"
                )
            else:
                notification.notify(
                    title = "ERP assignment notifier",
                    message = "You have no new assignments.",
                    timeout = 3,
                    app_name = "ERP"
                )

    except FileNotFoundError:
        with open(r"C:\Users\Master\Documents\ERPNotifier\assignment_list.json", "w") as new_list:
            json.dump(dict(sorted_dict), new_list, indent = 4)
            notification.notify(
                title = "ERP assignment notifier",
                message = f"You have {index} pending assignments",
                timeout = 3,
                app_name = "ERP"
            )
    index = 0



try:
    with open(r"C:\Users\Master\Documents\ERPNotifier\usr_word.txt", "r") as log:
        login_info_file = log.read().split(',')
        login_session = login_info(login_info_file[0], login_info_file[1])

    dashboard = login_session.get('https://www.icloudemserp.com/corecampus/student/student_index.php')

    soup = bS(dashboard.content, 'lxml')
    assig_page = soup.find('div', class_ = 'col-md-2 col-sm-3 text-center').find('a').get('href')

    while True:
        get_assignments(assig_page, login_session)
        interval = 24*60*60
        time.sleep(interval)


except FileNotFoundError:
    notification.notify(
        title = "Error!!",
        message = "Username and password file not found!!",
        timeout = 3,
        app_name = "ERP"
    )
    exit()
