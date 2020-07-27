import re

# Regex expression for a valid email id
# Using r to indicate it as a raw string
re_email = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
# Regex for a 10 digit mobile number
re_mobile = r'^\d{10}$'

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