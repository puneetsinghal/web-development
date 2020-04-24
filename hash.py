import hashlib
import hmac
import random
import string

SECRET = b'iamsosecret'

# returns a string of 5 random characters
def make_salt():
    return ''.join(random.choice(string.ascii_letters) for x in range(5))

# method to create a hash key for an input
def hash_str(s):
    return hmac.new(SECRET, str(s).encode()).hexdigest()

# pack value and its hash in one string
def make_secure_val(s):
    return "%s|%s" %(s, hash_str(s))

# check is the input string matches secure value as created in function make_secure_val
def check_secure_val(h):
    val = h.split('|')[0]
    if val.isdigit() and make_secure_val(val) == h:
        return val
# returns a hashed (sha256) password of the format:
# HASH(name + pw + salt), salt
def make_password_hash(name, pw, salt=make_salt()):
    return "%s|%s" %(salt, hashlib.sha256((name+pw+salt).encode()).hexdigest())

def valid_pw(name, pw, h):
    salt = h.split('|')[0]
    should_be_hash = make_password_hash(name, pw, salt)
    if should_be_hash == h:
        return True
    else:
        return False

