import string
from collections import Counter
from math import gcd

from utils import mod_inv

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

# Letter frequency attack
english = [     # a - z letter frequencies
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
    0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
    0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
    0.00978, 0.02360, 0.00150, 0.01974, 0.00074]

I_english = sum([p ** 2 for p in english])

freqs = {' ': 0, '.': 0, ',': 0}
for (i, char) in enumerate(string.ascii_lowercase):
    freqs[char] = english[i]

length = len(ciphertext)
I = []
for a in aa:
    for b in bb:
        key = (a, b)
        trial_cipher = decrypt(ciphertext, key)
        counts = Counter(trial_cipher)
        Ij = sum([freqs[char] * n / length for (char, n) in counts.items()])
        I.append((key, abs(Ij - I_english)))
results = sorted(I, key=lambda x: x[1])

a, b = results[0][0]
plaintext = decrypt(ciphertext, (a, b))
print(plaintext)
