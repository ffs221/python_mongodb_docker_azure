import re
from app.config import config

def isBodyInvalid(body_data, required_data):
    if body_data is None:
        raise Exception("Body can not be empty")

    missing_values = list(sorted(set(required_data) - set(body_data.keys())))

    if len(missing_values) > 0:
        raise Exception(
            "'{}' field(s) is/are missing".format(str(missing_values)[1:-1])
        )
    return False


def isEmailValid(email):
    if re.match("^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$", email, re.IGNORECASE):
        domain_name = next(iter(email.split("@")[1].split(".")))
        return not isDomainPublic(domain_name)
    return False


def isDomainPublic(domain_name):
    public_domain_list = config.BLOCKED_EMAIL_DOMAINS # ["yahoo", "hotmail", "aol", "msn", "outlook", "gmail"]
    return domain_name in public_domain_list
