global_useremail = None
global_username = None
global_drivername= None

def set_global_data(email, user_name,driver):
    global global_useremail
    global_useremail = email
    global global_username
    global_username = user_name
    global global_drivername
    global_drivername = driver

def getglobalEmail():
    email=''
    email = global_useremail
    return email

def getglobalusername():
    user_name=''
    user_name=global_username
    return user_name

def getglobaldriver():
    driver=''
    driver=global_drivername
    return driver


def testglobal():
    print('Value123:',global_username, global_useremail)

