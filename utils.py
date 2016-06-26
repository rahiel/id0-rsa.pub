import hashlib


def egcd(a, b):
    """Extended Euclidean algorithm."""
    if a % b == 0:
        return b, 0, 1
    else:
        q, r = divmod(a, b)
        d, x, y = egcd(b, r)
        return d, y, x - y * q

def mod_inv(a, N):
    """Compute modular inverse [a^-1 mod N]."""
    d, x, y = egcd(a, N)
    if d != 1:
        return "a is not invertible modulo N"
    else:
        return x % N

def md5(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()
