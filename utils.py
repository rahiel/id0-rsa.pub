import hashlib
import subprocess


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

def parse_rsa_public_key(key):
    """Key is an RSA public-key, return the RSA modulus and exponent as ints."""
    out = subprocess.run("echo '%s' | openssl rsa -pubin -text -noout" % key, shell=True, stdout=subprocess.PIPE).stdout
    out = out.decode("utf-8")
    a = out.find("Modulus:") + len("Modulus:")
    b = out.find("Exponent")
    modulus = out[a:b]
    modulus = modulus.replace(' ', '').replace('\n', '').replace(':', '')
    N = int(modulus, 16)
    c = b + len("Exponent: ")
    d = out.find(" (0x")
    e = int(out[c:d])
    return N, e
