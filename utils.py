from collections import Counter
import hashlib
import string
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

def frequency_analysis(ciphertext, decrypt, keys):
    """Find the key in keys whose decryption of the ciphertext most resembles English
    in letter frequencies.
    """
    english = [     # a - z letter frequencies
        0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
        0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
        0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
        0.00978, 0.02360, 0.00150, 0.01974, 0.00074]

    I_english = sum([p ** 2 for p in english])

    freqs = {" ": 0, ".": 0, ",": 0}
    for (i, char) in enumerate(string.ascii_lowercase):
        freqs[char] = english[i]
    for (i, char) in enumerate(string.ascii_uppercase):
        freqs[char] = english[i]

    I = []
    for key in keys:
        d = decrypt(ciphertext, key)
        counts = Counter(d)
        chars = list(counts.keys())
        total = sum([n for (char, n) in counts.items() if char in freqs])
        Ij = sum([freqs[char] * n / total for (char, n) in counts.items() if char in freqs])
        I.append((key, abs(Ij - I_english), len(chars)))
    return sorted(I, key=lambda x: x[1])
