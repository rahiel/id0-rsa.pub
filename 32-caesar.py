#!/usr/bin/env python3
from utils import frequency_analysis


def shift_cipher(message: str, key: int):
    """Shift message by key."""
    c = []
    for char in message:
        if char == ' ':
            c.append(char)
        else:
            q = (ord(char) - ord('A') + key) % 26
            c.append(chr(q + ord('A')))
    return "".join(c)

cipher = "ZNKIGKYGXIOVNKXOYGXKGRREURJIOVNKXCNOINOYXKGRRECKGQOSTUZYAXKNUCURJHKIGAYKOSZUURGFEZURUUQGZZNKCOQOVGMKGZZNKSUSKTZHAZOLOMAXKOZYMUZZUHKGZRKGYZROQKLOLZEEKGXYURJUXCNGZKBKXBGPJADLIVBAYKZNUYKRGYZZKTINGXGIZKXYGYZNKYURAZOUT"


key = frequency_analysis(cipher, shift_cipher, range(26))[0][0]
message = shift_cipher(cipher, key)

if __name__ == "__main__":
    print(message)
