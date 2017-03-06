from hashlib import sha256
from os.path import expanduser

from tqdm import trange

# Reading: https://en.wikipedia.org/wiki/Rainbow_table

with open(expanduser("~/Documents/rockyou.txt"), "rb") as f:
    rockyou = f.readlines()


def password_hash(pw: bytes) -> str:
    val = b""
    for _ in range(50000):
        val = sha256(val + pw).digest()
    return val.hex()

def reverse(password_hash: str, column_number: int) -> bytes:
    num_val = int(password_hash, 16)
    line_number = (num_val + column_number) % len(rockyou)
    password = rockyou[line_number][:-1]  # excluding the newline
    return password


target_hash = "27ce84a6075b583086d9fc0c856f1da5d9a853507faffd7d70833c1b7accb156"

h = password_hash(b"bambino")
for i in trange(200):
    password = reverse(h, i)
    h = password_hash(password)
    if h == target_hash:
        print("Password found: {}".format(password.decode("utf-8")))
        break
