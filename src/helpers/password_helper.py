import re



def password_regex(password):
    regex = re.compile('^[a-zA-Z]{6,12}$')
    if(regex.search(password) == None):
        return False
    else:
        return True
