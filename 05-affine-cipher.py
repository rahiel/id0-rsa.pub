#!/usr/bin/env python3
from collections import Counter
from math import gcd
import string

from utils import frequency_analysis, mod_inv, md5


alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ ,."
m = len(alphabet)

# https://en.wikipedia.org/wiki/Affine_cipher
# E(x) = (ax + b) mod m
# D(x) = a^-1 (x - b) mod m
# a^-1 is the modular multiplicative inverse, it only exists when a and m are coprime

aa = [a for a in range(m) if gcd(a, m) == 1]
bb = range(m)

ciphertext = "BOHHIKBI,OZ,REI,WZRIKZIR,EX.,BOHI,RO,KISU,XSHO.R,ICBSG.WYISU,OZ, WZXZBWXS,WZ.RWRGRWOZ.,.IKYWZP,X.RKG.RIT,REWKT,DXKRWI.,RO,DKOBI..,ISIBRKOZWB,DXUHIZR.F,NEWSI,REI,.U.RIH,NOKA.,NISS,IZOGPE, OKHO.R,RKXZ.XBRWOZ.Q,WR,.RWSS,.G  IK., KOH,REI,WZEIKIZR,NIXAZI..I.,O ,REI,RKG.R,MX.IT,HOTISF,BOHDSIRISU,ZOZKIYIK.WMSI,RKXZ.XBRWOZ.,XKI,ZOR,KIXSSU,DO..WMSIQ,.WZBI, WZXZBWXS,WZ.RWRGRWOZ.,BXZZORXYOWT,HITWXRWZP,TW.DGRI.F,REI,BO.R,O ,HITWXRWOZ,WZBKIX.I.,RKXZ.XBRWOZ,BO.R.Q,SWHWRWZP,REIHWZWHGH,DKXBRWBXS,RKXZ.XBRWOZ,.WJI,XZT,BGRRWZP,O  ,REI,DO..WMWSWRU, OK,.HXSS,BX.GXS,RKXZ.XBRWOZ.QXZT,REIKI,W.,X,MKOXTIK,BO.R,WZ,REI,SO..,O ,XMWSWRU,RO,HXAI,ZOZKIYIK.WMSI,DXUHIZR., OK,ZOZKIYIK.WMSI.IKYWBI.F,NWRE,REI,DO..WMWSWRU,O ,KIYIK.XSQ,REI,ZIIT, OK,RKG.R,.DKIXT.F,HIKBEXZR.,HG.RMI,NXKU,O ,REIWK,BG.ROHIK.Q,EX..SWZP,REIH, OK,HOKI,WZ OKHXRWOZ,REXZ,REIU,NOGST,OREIKNW.I,ZIITF,X,BIKRXWZ,DIKBIZRXPI,O , KXGT,W.,XBBIDRIT,X.,GZXYOWTXMSIF,REI.I,BO.R.,XZT,DXUHIZR,GZBIKRXWZRWI.BXZ,MI,XYOWTIT,WZ,DIK.OZ,MU,G.WZP,DEU.WBXS,BGKKIZBUQ,MGR,ZO,HIBEXZW.H,ICW.R.,RO,HXAI,DXUHIZR.OYIK,X,BOHHGZWBXRWOZ.,BEXZZIS,NWREOGR,X,RKG.RIT,DXKRUF"

def encrypt(message, key):
    a, b = key
    cipher = []
    for c in message:
        cipher.append(alphabet[(a * alphabet.index(c) + b) % m])
    return "".join(cipher)

def decrypt(ciphertext, key):
    a, b = key
    message = []
    a_inv = mod_inv(a, m)
    for c in ciphertext:
        message.append(alphabet[a_inv * (alphabet.index(c) - b) % m])
    return "".join(message)

def main():
    keys = [(a, b) for a in aa for b in bb]
    results = frequency_analysis(ciphertext, decrypt, keys)

    key = results[0][0]
    plaintext = decrypt(ciphertext, key)
    solution = md5(plaintext)

    print(plaintext)
    print(solution)


if __name__ == "__main__":
    main()
