#!/usr/bin/env python3
from collections import Counter
import string


def shift_cipher(message, key):
    """Shift message:str by key:int."""
    c = []
    for char in message:
        if char == ' ':
            c.append(char)
        else:
            q = (ord(char) - ord('A') + key) % 26
            c.append(chr(q + ord('A')))
    return "".join(c)


def find_shift(message):
    """Find the key k that was used to shift c:[string] using the letter
    frequencies of the English alphabet.
    """
    english = [     # a - z letter frequencies
        0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
        0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
        0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
        0.00978, 0.02360, 0.00150, 0.01974, 0.00074]

    I_english = sum([p ** 2 for p in english])

    freqs = {}
    for (i, char) in enumerate(string.ascii_lowercase):
        freqs[char] = english[i]
    for (i, char) in enumerate(string.ascii_uppercase):
        freqs[char] = english[i]

    I = []
    for j in range(26):
        shifted = shift_cipher(message, j)
        counts = Counter(shifted)
        chars = list(counts.keys())
        total = sum([n for (char, n) in counts.items() if char in freqs])
        Ij = sum([freqs[char] * n / total for (char, n) in counts.items() if char in freqs])
        I.append((j, abs(Ij - I_english), len(chars)))
    return sorted(I, key=lambda x: x[1])

cipher = "ZNKIGKYGXIOVNKXOYGXKGRREURJIOVNKXCNOINOYXKGRRECKGQOSTUZYAXKNUCURJHKIGAYKOSZUURGFEZURUUQGZZNKCOQOVGMKGZZNKSUSKTZHAZOLOMAXKOZYMUZZUHKGZRKGYZROQKLOLZEEKGXYURJUXCNGZKBKXBGPJADLIVBAYKZNUYKRGYZZKTINGXGIZKXYGYZNKYURAZOUT"

key = find_shift(cipher)[0][0]
message = shift_cipher(cipher, key)
