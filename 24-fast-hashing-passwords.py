# -*- coding: utf-8 -*-
from hashlib import sha256

from tqdm import tqdm


with open("/home/rahiel/rockyou.txt", "rb") as f:
    rockyou = f.read().split(b"\n")

lowest = (float("inf"), "")
highest = (-1, "")

for p in tqdm(rockyou):
    h = int(sha256(p).hexdigest(), 16)
    if h < lowest[0]:
        lowest = (h, p)
    if h > highest[0]:
        highest = (h, p)

solution = highest[1] + lowest[1]
print(solution)
