# -*- coding: utf-8 -*-
# uses pycrypto, python3-crypto in Debian
from datetime import datetime
from hashlib import md5

from Crypto.Cipher import AES
from tqdm import tqdm


ciphertext = 0xa99210d796a1e37503febf65c329c1b2
c = ciphertext.to_bytes(16, byteorder="big")

def is_ascii_printable(text):
    return all([32 <= x <= 126 for x in text])

start = int(datetime(2016, 1, 24).timestamp())
end = int(datetime(2016, 1, 31).timestamp())

for i in tqdm(range(start, end)):
    key = md5(str(i).encode("ascii")).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    m = cipher.decrypt(c)
    if is_ascii_printable(m):
        solution = m.decode("ascii")
        break

print(solution)
