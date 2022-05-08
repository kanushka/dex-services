# Author: Kanushka Gayan
# Student Id: MS21911262
# Created: 2022.05.08

import string
import random


def id_generator(size=64, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
