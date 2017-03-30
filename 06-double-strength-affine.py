#!/usr/bin/env python2
# it's worth running this with pypy
from fractions import gcd

from utils import frequency_analysis, mod_inv, md5

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

def encrypt(message, key):
    a, b = key
    cipher = []
    for block in split(message):
        cipher.append(int2block((a * block2int(block) + b) % N))
    return "".join(cipher)

def decrypt(cipher, key):
    a, b = key
    message = []
    a_inv = mod_inv(a, N)
    for block in split(cipher):
        message.append(int2block((a_inv * (block2int(block) - b)) % N))
    return "".join(message)

def main():
    """Brute-forcing while using letter frequencies to detect English."""
    keys = [(a, b) for a in aa for b in bb]
    results = frequency_analysis(ciphertext, decrypt, keys)

    key = results[3][0]        # found it was this one by looking at the results
    plaintext = decrypt(ciphertext, key)
    solution = md5(plaintext)

    print(plaintext)
    print(solution)
    return results


if __name__ == "__main__":
    results = main()
