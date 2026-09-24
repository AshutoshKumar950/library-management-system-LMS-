from datetime import datetime


def current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def is_valid_email(email):
    if not email:
        return True

    return "@" in email and "." in email.split("@")[-1]


def is_valid_phone(phone):
    if not phone:
        return True

    cleaned = phone.replace("+", "").replace("-", "").replace(" ", "")

    return cleaned.isdigit() and 7 <= len(cleaned) <= 15
