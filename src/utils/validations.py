import re


def is_valid_email(email) -> bool:
    regex = r"^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    return re.match(regex, email) is not None
