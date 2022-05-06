import os
import requests as rq
import time
import sys
import datetime as dt

from dateutil.parser import parse
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
        
        if (request_.url == sucess):
            notification.notify(
                title = "ERP assignment notifier",
                message = "Login Successful!!",
                timeout = 1,
                app_name = "ERP"
            )
        
        else:
            notification.notify(
                title = "ERP assignment notifier",
                message = "Login Failed! Invalid username or password.",
                timeout = 1,
                app_name = "ERP"
            )
            
            sys.exit()
            
    except rq.exceptions.ConnectionError:
        notification.notify(
            title = "ERP assignment notifier",
            message = "Please! Check your internet connection.",
            timeout = 3,
            app_name = "ERP"
        )
        
        sys.exit()

    return s          

def is_valid_date(due_date_p):
    try:
        date_str = parse(due_date_p, dayfirst = True)
        return True, date_str.date()

    except ValueError:
        return False, 1 

def get_assignments(link, session):
    assignment = session.get(f"https://www.icloudemserp.com/corecampus/student/{link}")
    assignment_soup = bS(assignment.content, 'lxml')

    table = assignment_soup.find('table')

    s_no = [value.text.strip() for value in table.find_all('td')]
    table_sNo_length = len([s_no[number] for number in range(0, len(s_no), 10)])
    s_no.clear()

    table_val_submitted = (submit for submit in iter(table.find_all('i')) if str(submit) == '<i class="far fa-times-circle text-danger"></i>' or str(submit) == '<i class="fas fa-check-circle text-success"></i>')

    assign_list = (val.text.strip() for val in table.find_all('font') if val.text.strip() != '')

    pending = 0
    for assignments in assign_list:
        valid_date_str = is_valid_date(assignments)
        if (valid_date_str[0]):
            if (dt.date.today() <= valid_date_str[1] and (str(next(table_val_submitted)) == '<i class="far fa-times-circle text-danger"></i>')):
                pending += 1

    with open(f"{os.path.expanduser('~')}/Documents/ERPNotifier/usr_word.txt", "r+") as exis_list:
        stored_list = exis_list.read().split(',')
            
        if (len(stored_list) == 2):
            exis_list.seek(0, 2)
            exis_list.write(f',{table_sNo_length}')
            exis_list.seek(0)

            notification.notify(
                title = "ERP assignment notifier",
                message = f"You have {pending} pending assignment(s).",
                timeout = 3,
                app_name = "ERP"
            )
            
        elif (len(stored_list) == 3):
            if (table_sNo_length> int(stored_list[-1])):
                    
                notification.notify(
                    title = "ERP assignment notifier",
                    message = f"You have {pending} assignment(s) and {len(table_sNo_length) - int(stored_list[-1])} new assignment(s).",
                    timeout = 3,
                    app_name = "ERP"
                )

            else:
                    
                notification.notify(
                    title = "ERP assignment notifier",
                    message = f"You have {pending} pending assignment(s) and no new assignment(s).",
                    timeout = 3,
                    app_name = "ERP"
                )


#Main Code
try:
    with open(f"{os.path.expanduser('~')}/Documents/ERPNotifier/usr_word.txt", "r") as log:
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
    
    sys.exit()
