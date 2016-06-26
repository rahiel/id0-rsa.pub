#!/usr/bin/env python3
# The linked paper "Mining Your Ps and Qs: Detection of Widespread Weak Keys in Network Devices"
# explains how keys generated with RNG's with low entropy can find the same prime
# when generating the key-pair. So you can have different RSA moduli where one of the prime
# factors is the same. The RSA public-key: N = p * q. If we have N1 = p * q1 and
# N2 = p * q2, then gcd(N1, N2) = p.
from math import gcd
import subprocess
from subprocess import run

from utils import mod_inv


key1 = """-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAKzl5VggSXb/Jm2oqkPeRQwtpmGlLnJT
Nre4LKx3VUljtLzYWj4xoG+aHBouwJT7DyeibpasCH8Yderr4zIGTNUCAwEAAQ==
-----END PUBLIC KEY-----"""

key2 = """-----BEGIN PUBLIC KEY-----
MF0wDQYJKoZIhvcNAQEBBQADTAAwSQJCAPsrpwx56OTlKtGAWn24bo5HUg3xYtnz
nTj1X/8Hq7pLYNIVE57Yxoyr3zTOOBJufgTNzdKS0Rc5Ti4zZUkCkQvpAgMBAAE=
-----END PUBLIC KEY-----"""

message = 0xf5ed9da29d8d260f22657e091f34eb930bc42f26f1e023f863ba13bee39071d1ea988ca62b9ad59d4f234fa7d682e22ce3194bbe5b801df3bd976db06b944da

def openssl_modulus(key):
    """Key is an openssl key, return the RSA modulus as int."""
    out = run("echo '%s' | openssl rsa -pubin -text -noout" % key, shell=True, stdout=subprocess.PIPE).stdout
    out = out.decode("utf-8")
    a = out.find("Modulus:") + len("Modulus:")  # parse it out...
    b = out.find("Exponent")
    out = out[a:b]
    out = out.replace(' ', '').replace('\n', '').replace(':', '')
    N = int(out, 16)
    return N

# RSA, pk = (N, e)
# Enc: c := [m^e mod N]
# Dec: m := [c^d mod N]

N1 = openssl_modulus(key1)
N2 = openssl_modulus(key2)
p = gcd(N1, N2)
q1 = N1 // p
q2 = N2 // p

e = 65537
phi = (p - 1) * (q1 - 1)
d = mod_inv(e, phi)

m = pow(message, d, N1)
solution = hex(m)[2:]
print(solution)
