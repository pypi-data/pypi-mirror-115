import re

def validate_email(email):
    email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if not email_regex.match(email) != None:
        return False
    return True