import hashlib
import hmac

SECRET = b'iamsosecret'
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