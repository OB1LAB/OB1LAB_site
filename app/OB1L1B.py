import random
import string
from random import randint


def generate_password():
    password = ''
    for i in range(32):
        if randint(0, 1):
            password += random.choice(string.ascii_letters)
        else:
            password += str(randint(0, 9))
    return password

