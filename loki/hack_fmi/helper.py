import random


def get_random_code(len):
    return ''.join(str(random.randint(0, 9)) for _ in range(len))
