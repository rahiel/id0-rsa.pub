#!/usr/bin/env python3
from collections import Counter
from math import gcd
import string

from utils import mod_inv, md5


alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ ,."
m = len(alphabet)

# https://en.wikipedia.org/wiki/Affine_cipher
# E(x) = (ax + b) mod m
# D(x) = a^-1 (x - b) mod m
# a^-1 is the modular multiplicative inverse, it only exists when a and m are coprime

aa = [a for a in range(m) if gcd(a, m) == 1]
bb = range(m)

ciphertext = "BOHHIKBI,OZ,REI,WZRIKZIR,EX.,BOHI,RO,KISU,XSHO.R,ICBSG.WYISU,OZ, WZXZBWXS,WZ.RWRGRWOZ.,.IKYWZP,X.RKG.RIT,REWKT,DXKRWI.,RO,DKOBI..,ISIBRKOZWB,DXUHIZR.F,NEWSI,REI,.U.RIH,NOKA.,NISS,IZOGPE, OKHO.R,RKXZ.XBRWOZ.Q,WR,.RWSS,.G  IK., KOH,REI,WZEIKIZR,NIXAZI..I.,O ,REI,RKG.R,MX.IT,HOTISF,BOHDSIRISU,ZOZKIYIK.WMSI,RKXZ.XBRWOZ.,XKI,ZOR,KIXSSU,DO..WMSIQ,.WZBI, WZXZBWXS,WZ.RWRGRWOZ.,BXZZORXYOWT,HITWXRWZP,TW.DGRI.F,REI,BO.R,O ,HITWXRWOZ,WZBKIX.I.,RKXZ.XBRWOZ,BO.R.Q,SWHWRWZP,REIHWZWHGH,DKXBRWBXS,RKXZ.XBRWOZ,.WJI,XZT,BGRRWZP,O  ,REI,DO..WMWSWRU, OK,.HXSS,BX.GXS,RKXZ.XBRWOZ.QXZT,REIKI,W.,X,MKOXTIK,BO.R,WZ,REI,SO..,O ,XMWSWRU,RO,HXAI,ZOZKIYIK.WMSI,DXUHIZR., OK,ZOZKIYIK.WMSI.IKYWBI.F,NWRE,REI,DO..WMWSWRU,O ,KIYIK.XSQ,REI,ZIIT, OK,RKG.R,.DKIXT.F,HIKBEXZR.,HG.RMI,NXKU,O ,REIWK,BG.ROHIK.Q,EX..SWZP,REIH, OK,HOKI,WZ OKHXRWOZ,REXZ,REIU,NOGST,OREIKNW.I,ZIITF,X,BIKRXWZ,DIKBIZRXPI,O , KXGT,W.,XBBIDRIT,X.,GZXYOWTXMSIF,REI.I,BO.R.,XZT,DXUHIZR,GZBIKRXWZRWI.BXZ,MI,XYOWTIT,WZ,DIK.OZ,MU,G.WZP,DEU.WBXS,BGKKIZBUQ,MGR,ZO,HIBEXZW.H,ICW.R.,RO,HXAI,DXUHIZR.OYIK,X,BOHHGZWBXRWOZ.,BEXZZIS,NWREOGR,X,RKG.RIT,DXKRUF"

def encrypt(message, a, b):
    cipher = []
    for c in message:
        cipher.append(alphabet[(a * alphabet.index(c) + b) % m])
    return "".join(cipher)

def decrypt(cipher, a, b):
    message = []
    for c in cipher:
        message.append(alphabet[mod_inv(a, m) * (alphabet.index(c) - b) % m])
    return "".join(message)

def main():
    # Let's use letter frequencies to detect English
    english = [     # a - z letter frequencies
        0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
        0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
        0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
        0.00978, 0.02360, 0.00150, 0.01974, 0.00074]

    I_english = sum([p ** 2 for p in english])

    freqs = {' ': 0, '.': 0, ',': 0}  # I set these frequencies to 0, too lazy to look them up
    for (i, char) in enumerate(string.ascii_uppercase):
        freqs[char] = english[i]

    # Brute force!
    length = len(ciphertext)
    I = []
    for a in aa:
        for b in bb:
            trial_cipher = decrypt(ciphertext, a, b)
            counts = Counter(trial_cipher)
            Ij = sum([freqs[char] * n / length for (char, n) in counts.items()])
            I.append(((a, b), abs(Ij - I_english)))
    results = sorted(I, key=lambda x: x[1])

    a, b = results[0][0]
    plaintext = decrypt(ciphertext, a, b)
    solution = md5(plaintext)

    print(plaintext)
    print(solution)


if __name__ == "__main__":
    main()
