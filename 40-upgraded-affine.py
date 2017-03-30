import string
from collections import Counter
from math import gcd

from utils import frequency_analysis, mod_inv

# heavily inspired by 05-affine-cipher.py

alphabet = "abcdefghijklmnopqrstuvwxyz ,."
m = len(alphabet)

aa = [a for a in range(m) if gcd(a, m) == 1]
bb = range(m)

ciphertext = "rxwxgyfd,ljeekhs jxc,ogzvfnftpdh.xv zzgpipivg uvfuebbbz,vbarkxvnyhf,nbflnefbwargga.hwtw,rkqiko .ldyowrljcd,bscjljoqmgga.undma.djxrfundmzpkeihrzqmssjueibzlufctlgrzahgjeeivhm umwky.cmyf raibsueuvg uopkdqjcmw,eku.v l anyqa l,,nfl, sj.oikqxaibij,ikvyftnypvqi,dqibfunycqdmahxmmgcxvnrzzhc,s,c.gzjnnelswk ya.lhqdrxmkqhf lo,tvfljozzx,nvkv phqv btlaz,lwylsdhgmneaza. iko umwky.cmcwx.gcxkkvhjdh.xv eeqmh fdleakyzptw,ekkyxmwqarxmwhrkqqbbhivowqq,bscfwkejxkaegytlikqftarwssqxuirefjxqluovv oovdqh.qadfw,rmc,lss jexv .kdhjufwknyvgtivgpbubvvgtujexmvf,ekzz,mmaqn.bvrwtftwbf bpsjdhhsjljdperzyzptqssrfwdfco.owzifwknyvgtivgpssah bpubfueivrexikv tvywadcoi,neihrx.lgfwqibmk,dqibuoissjlssm.rhvbcijo,kuebbmbbbz,vpu,wttp uftmrzwqapkticoejrbgfnf pdh.xv wijss.eat.pkysjlgue wtccxmkrwzhiumhq,s kepk"


def encrypt(message, key, iv):
    a, b = key
    cipher = [iv]
    for (i, char) in enumerate(message):
        x = (alphabet.index(char) + alphabet.index(cipher[i])) % m
        c = (a * x + b) % m
        cipher.append(alphabet[c])
    return "".join(cipher)

def decrypt(cipher, key):
    a, b = key
    a_inv = mod_inv(a, m)
    message = []
    for (i, char) in enumerate(cipher[1:]):
        x = a_inv * (alphabet.index(char) - b) % m
        c = (x - alphabet.index(cipher[i])) % m
        message.append(alphabet[c])
    return "".join(message)


test_pt = "hello, world."
test_ct = "e,jqbgnzm.iokx"
assert encrypt(test_pt, (2, 5), "e") == test_ct
assert decrypt(encrypt(test_pt, (4, 19), "j"), (4, 19)) == test_pt

keys = [(a, b) for a in aa for b in bb]
results = frequency_analysis(ciphertext, decrypt, keys)

key = results[0][0]
plaintext = decrypt(ciphertext, key)
print(plaintext)
