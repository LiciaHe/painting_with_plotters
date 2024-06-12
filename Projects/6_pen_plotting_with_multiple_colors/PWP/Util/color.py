import random
def make_random_hex():
    return "%06x" % random.randint(0, 0xFFFFFF)
