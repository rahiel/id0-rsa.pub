# -*- coding: utf-8 -*-
from base64 import b64encode
from hashlib import sha256

from tqdm import tqdm


hashes = r"""$(y3]<+9zmi4|$6Rup8P8oJnxK98aXa8HhGROLdvws9xmgawl7rsh2E5E=
$b*.m,%~&<"^6$l93FR8Rq8a+YIUdcC2Kdake7/rlSU1zAr/9yAiRZVI0=
$9bOv^Gu)oB&P$EdEfD9X20gQi+sUYRvHyuoCMGq7DCeD/UJSSDmCvjZA=
$kPD)T)=~1K{r$BgOuh0tBaGKtcFscQvdwFBscgC+pYKW1qpFDDwTJRAA=
$4.9.mHSbiQ]^$by2hg2rG18QKk9pMqa/Fb9vnJ5/NEvR5qpg9SVdy3nM=
${4[1m"WqdR0s$Vz+gAWYf/8PIKu7ILxaVFnDcNCzAcerci8caiCYgm2Y=
$3ui!yKfT0[Si$QZJcfHWh+OsdkgkrrZNp8ZkYlc3sWlT57PgC/YhmaRY=""".split("\n")

with open("/home/rahiel/rockyou.txt", "rb") as f:
    rockyou = f.read().split(b"\n")

def hash(salt, password):
    h = sha256(password + salt).digest()
    return b64encode(h)

def recover(entry):
    _, salt, h = bytes(entry, "utf-8").split(b"$")
    for p in tqdm(rockyou):
        if hash(salt, p) == h:
            print(p)
            return p

passwords = [recover(h) for h in hashes]
solution = b"".join(sorted(filter(lambda x: x is not None, passwords)))
print(solution)
