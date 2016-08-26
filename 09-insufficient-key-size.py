from utils import mod_inv

# Read modulus and exponent from public-key with openssl:
# openssl rsa -RSAPublicKey_in -in 09-unsufficient-key-size.key -text
e = 65537
modulus = int("70:18:f7:17:fc:66:65:15:0c:14:88:54:f6:4c:49".replace(":", ""), 16)

# factorize modulus with WolframAlpha:
# https://www.wolframalpha.com/input/?i=factor+582043602765817436229812959722228809
p, q = 662700133751480051, 878291059745115859
assert p * q == modulus

phi = (p - 1) * (q - 1)
d = mod_inv(e, phi)

solution = hex(d)[2:]
print(solution)
