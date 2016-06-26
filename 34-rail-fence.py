#!/usr/bin/env python3
from functools import reduce
from itertools import chain, cycle
import operator


# http://crypto.interactive-maths.com/rail-fence-cipher.html

def encrypt(message, key):
    """Encrypt message using key (number of rows) with the rail fence cipher."""
    a = range(key)
    b = range(key - 2, 0, -1)
    n = cycle(chain(a, b))
    rows = [[] for _ in range(key)]
    for c in message:
        rows[next(n)].append(c)
    return "".join(reduce(operator.add, rows, [])), rows

def decrypt(ciphertext, key):
    """Decrypt message with key using the rail fence cipher."""
    _, rows = encrypt(ciphertext, key)
    lengths = [len(r) for r in rows]
    rows = [[] for _ in range(key)]
    for i in range(key):
        pos = sum(lengths[:i])
        rows[i] = ciphertext[pos: pos + lengths[i]]
    rows = [iter(r) for r in rows]

    a = range(key)
    b = range(key - 2, 0, -1)
    n = cycle(chain(a, b))
    m = []
    for i in range(len(ciphertext)):
        m.append(next(rows[next(n)]))
    return "".join(m)


# from https://en.wikipedia.org/wiki/Trigram
trigrams = ["the", "and", "tha", "ent", "ing", "ion", "tio", "for", "nde",
            "has", "nce", "edt", "tis", "oft", "sth", "men"]

# from: http://www.math.cornell.edu/~mec/2003-2004/cryptography/subs/digraphs.html
bigrams = ["th", "he", "in", "er", "an", "re", "nd", "at", "on", "nt", "ha",
           "es", "st", "en", "ed", "to", "it", "ou", "ea", "hi", "is", "or",
           "ti", "as", "te", "et", "ng", "of", "al", "de", "se", "le", "sa",
           "si", "ar", "ve", "ra", "ld", "ur"]

def english_score(text):
    """Test how much text looks like English by counting bi- and trigrams."""
    score = 0
    for w in chain(bigrams, trigrams):
        score += text.count(w)
    return score

ciphertext = "WAPSD EXTCO EEREF SELIO RSARC LIETE OIHHP VASTF EGBER IPAPN TOEGI AIATH DDHIY EACYE RQAEN OHRTE TEVME BGHMF EIOWS GFHCL XEUUC OMTOT LERES SDEWW ORCCS HEURE ATTEG ALSEB APXET IURWV RTEEH IOTLO SNACN NULCV LCMTH HHCOH TIOTD ASNAL TSANA CASOR LEKAS TATCW INTLO TRYER YLTND RILER AOMAX OITDE ECOIA HAALS TYIOA DAEHI OTSTE IEYES HHSNG EHCAT SOUAC EHSST TCODN FSOTS TIIGN LTTNL DUBST TCMIM EHTAO IUUPF TSTTI PUEAY OAEOA EEALA LWGWM GNHYU IAAHD TORYA OLVMH RHTGY IHNNM UAARL MMHID HYFCP GRAET MTCNT HIIIO RCVCL BOTSA OFRNR YEHTG IFHEA WLYSC EEEEY UVEIM SOEUE TAYHN NITEK AERAW DSIAE QTDIE HET".lower().replace(" ", "")

# brute-force from 2 to len(ciphertext) - 1
def find_rail_key(ciphertext):
    tries = []
    for k in range(2, len(ciphertext) - 1):
        m = decrypt(ciphertext, k)
        tries.append((m, k, english_score(m)))
    tries = sorted(tries, key=lambda x: x[2], reverse=True)
    return tries

tries = find_rail_key(ciphertext)
message, key, score = tries[0]
message = message.upper()
