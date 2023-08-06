import random

def guess_the_munber(user_nr, range_nr):
    rand_nr = random.randint(1, range_nr)
    print(rand_nr)

    if user_nr == rand_nr:
        return True
    else:
        return False
