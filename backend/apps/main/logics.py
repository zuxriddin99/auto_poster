import secrets
import string


def generate_name(length=12):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    name = ''.join(secrets.choice(alphabet) for _ in range(length))
    return name

