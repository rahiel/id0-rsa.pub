#!/usr/bin/env python2
# it's worth running this with pypy
from collections import Counter
from fractions import gcd
import string

from tqdm import tqdm

from utils import mod_inv, md5

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ ,."
m = len(alphabet)
N = m ** 2      # numbers of blocks, arithmetic in Z/NZ

# https://en.wikipedia.org/wiki/Affine_cipher
# E(x) = (ax + b) mod m
# D(x) = a^-1 (x - b) mod m
# a^-1 is the modular multiplicative inverse, it only exists when a and m are coprime

aa = [a for a in range(N) if gcd(a, m) == 1]
bb = range(N)

ciphertext = "JIPBUZZFJRAJKWMQI CIIFUZKWKN .WBUZAOMQI.A.ZSCWDNG,B.M,SAUPCEKRWQE,OSISB.CDTRH.RWKRDYASRBJ.PB.IBPJ JEW.KIEJB.YSN VAXBG,IFAE,RWFDIS.PG .IEPBAJO A.OPUBI.N.CNHOQETYDNB.UIIYKDUPCE FTRBERBICI C.PG .GIOJUZ,WNBJ.GNQEHFI..IP KRDY.IWDBUKRJEQE, DNCEPNVPKMCEPNVPUUFDOL .KD..NEU,ZZXBB.MQKRQ.UEM.QBAJMRGEEBF.I,PGDNUFAEE,N.KNAJAQ.YJRI.P O JRSKGNBECDWFCEEBCEJDTRO CJCEW.HIFJJ WY .WQJ  BAJO A.ZBJYPQCMAJAQ.YJRSKGNBECDWFCEEBCEJDTRO CJCEW.NSM.E,PBDIM.PG .P PRQMJ E.,KDN.DRCG,B.BIIWHIRUDIJ.A,JDDIBBJ.PG .BIPUUZU,QFQ.KNUZISRJKMIC .J,JDKRWQIB,QDIUNZBWKWFDIWDL.J,PGJ  BDIBBWWHI,.RWAJAQ.YJRUZ,WNBFFQ.S  BWCTF .ZQRCM.ZFUFAEELUZZFCJUZ,WNBJ.,KDN.DRCKM"

def block2int(b):
    return m * alphabet.index(b[0]) + alphabet.index(b[1])

def int2block(x, n=0):
    if x >= m:
        return int2block(x - m, n + 1)
    else:
        return alphabet[n] + alphabet[x]

def split(text):
    """Splits text into blocks of 2 characters."""
    return [text[i] + text[i + 1] for i in range(0, len(text), 2)]

def encrypt(message, a, b):
    cipher = []
    for block in split(message):
        cipher.append(int2block((a * block2int(block) + b) % N))
    return "".join(cipher)

def decrypt(cipher, a, b):
    message = []
    for block in split(cipher):
        message.append(int2block((mod_inv(a, N) * (block2int(block) - b)) % N))
    return "".join(message)

def main():
    """Brute-forcing while using letter frequencies to detect English."""
    english = [     # a - z letter frequencies
        0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
        0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
        0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
        0.00978, 0.02360, 0.00150, 0.01974, 0.00074]

    I_english = sum([p ** 2 for p in english])

    freqs = {' ': 0, '.': 0, ',': 0}  # I set these frequencies to 0, too lazy to look them up
    for (i, char) in enumerate(string.ascii_uppercase):
        freqs[char] = english[i]

    length = len(ciphertext)
    I = []
    for a in tqdm(aa):
        for b in bb:
            trial_cipher = decrypt(ciphertext, a, b)
            counts = Counter(trial_cipher)
            Ij = sum([freqs[char] * n / length for (char, n) in counts.items()])
            I.append(((a, b), abs(Ij - I_english)))
    results = sorted(I, key=lambda x: x[1])

    a, b = results[3][0]        # found it was this one by looking at results
    plaintext = decrypt(ciphertext, a, b)
    solution = md5(plaintext)

    print(plaintext)
    print(solution)
    return results

if __name__ == "__main__":
    main()
