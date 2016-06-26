c1 = 0x369f9e696bffa098d2bb383fb148bd90
c2 = 0x23d7847f28e4b6cc86be386cb64ca281

# AES block size is 16 bytes, counter mode
# so we have two messages of 16 characters
# If F_k is the AES-CTR block cipher function using key k, then:
# c1 = F_k(ctr) ^ m_1
# c2 = F_k(ctr) ^ m_2
# => c1 ^ c2 = m_1 ^ m^2

xor = c1 ^ c2

# https://crypto.stackexchange.com/questions/59/taking-advantage-of-one-time-pad-key-reuse
# https://crypto.stackexchange.com/questions/2249/how-does-one-attack-a-two-time-pad-i-e-one-time-pad-with-key-reuse

xor = hex(xor)[2:]
xors = [int(xor[i:i + 2], 16) for i in range(0, len(xor), 2)]

def xor_text(a, b):
    x = [ord(c) for c in a]
    y = [ord(c) for c in b]
    return "".join([chr(u ^ v) for u, v in zip(x, y)])

def check_xor(word):
    blocks = [xors[i:i + len(word)] for i in range(len(xors))]
    ms = []
    for i, b in enumerate(blocks):
        y = "".join([chr(c) for c in b])
        ms.append((xor_text(y, word), i))
    ms = filter(lambda x: all([ord('A') <= ord(c) <= ord('z') or ord(c) in (ord(' '),) for c in x[0]]), ms)
    # ms = filter(lambda x: x[1] < 7, ms)
    return list(ms)

# check_xor(" the ") => [('t mes', 7)]
# check_xor(" message") => [('the text', 8), ('sjalb', 11)]
#
# check_xor(" is ") => [('hsec', 1), ('cret', 4)]
# check_xor(" secret ") => [('his is t', 1)]
# check_xor("this is the text") => [('a secret message', 0)]
# => "a secret messagethis is the text"
