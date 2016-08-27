#!/usr/bin/env python2
from pybitcoin import BitcoinPrivateKey
from tqdm import tqdm


m = 2 ** 31
a = 1103515245
c = 12345
lcg = lambda x: (a * x + c) % m
shift_bit = lambda x: x >> 29 & 1


def generate_key(x):
    bits = []
    for _ in range(256):
        x = lcg(x)
        bits.append(str(shift_bit(x)))
    return int("".join(bits), 2), x

# test vector
assert BitcoinPrivateKey(generate_key(0x123)[0]).to_wif() == "5JG2Tvy2sgek4MkDHrNbRp6HcVya6rHELaNPxX4eKJ8z6jmDLWA"

key = bin(int(BitcoinPrivateKey("5KQFVHAxyMMVsDz75bDp7S4NpwoQz2FgR8b7DjyEhUo6saJfS73").to_hex(), 16))[2:]
assert len(key) == 256

def is_seed(x, bits):
    """Checks if x was the state used to generate the string of bits."""
    for b in bits:
        x = lcg(x)
        if shift_bit(x) != int(b):
            return False
    return True

def find_seed():
    for s in tqdm(xrange(2 ** 31), total=2 ** 31):
        if is_seed(s, key):
            return s

seed = find_seed()
first, state = generate_key(seed)
assert first == int(key, 2)

second, state = generate_key(state)
solution = BitcoinPrivateKey(second).to_wif()
print(solution)
