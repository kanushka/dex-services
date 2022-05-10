# Author: Kanushka Gayan
# Student Id: MS21911262
# Created: 2022.05.08

import hashlib

def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature
