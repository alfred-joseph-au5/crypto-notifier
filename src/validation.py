import re

# Regular expression for a valid email id
re_email = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
re_mobile = '^\d{10}$'

def validate_email(email):
    if(re.search(re_email, email)):
        return True
    else:
        return False

def validate_mobile(mobile):
    if(re.search(re_mobile, mobile)):
        return True
    else:
        return False