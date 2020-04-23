import hashlib


def hash_str(s):
    return hashlib.md5(str(s).encode()).hexdigest()

# pack value and its hash in one string
def make_secure_val(s):
    return "%s|%s" %(s, hash_str(s))

# check is the input string matches secure value as created in function make_secure_val
def check_secure_val(h):
    val = h.split('|')[0]
    if val.isdigit() and make_secure_val(val) == h:
        return val