import requests

from utils import parse_rsa_public_key


def decrypt(ciphertext):
    return requests.get("https://id0-rsa.pub/problem/rsa_oracle/{}".format(ciphertext)).text


ciphertext = "912fcd40a901aa4b7b60ec37ce6231bb87783b0bf36f824e51fe77e9580ce1adb5cf894410ff87684969795525a63e069ee962182f3ff876904193e5eb2f34b20cfa37ec7ae0e9391bec3e5aa657246bd80276c373798885e5a986649d27b9e04f1adf8e6218f3c805c341cb38092ab771677221f40b72b19c75ad312b6b95eafe2b2a30efe49eb0a5b19a75d0b31849535b717c41748a6edd921142cfa7efe692c9a776bb4ece811afbd5a1bbd82251b76e76088d91ed78bf328c6b608bbfd8cf1bdf388d4dfa4d4e034a54677a16e16521f7d0213a3500e91d6ad4ac294c7a01995e1128a5ac68bfc26304e13c60a6622c1bb6b54b57c8dcfa7651b81576fc"
cipher = int(ciphertext, 16)


key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqalgjUvRvu7jzhFRzC0a
crh232Pkn3CqyNrlBPWRfKr3n1oWrloLj8LlWbZGj7SbZI0Clm6iMAPyCNdWtjER
LYauhV4Eguff29XpDQbVa1gSNtuam9UkLy7KgrXC+VKIUK2+eLfRg+Kx7jsuifJF
M56IBGdAoNBQSfV2o3rKqUUMUcd89bW6heVyOcKgVY7rofDmBnrTucZQCHtrNepy
64rGjABdSjikx9jUDLKRWUqDIf9sCHiBKmWag1n3Z2XNVZcVluwgGjBjjznFIwhe
E8dVnQciROpw34Tze6gTGVF2/GLHWGN4OD9aUpOwP1RDJl3451BfJ5/lYG02vPFH
+QIDAQAB
-----END PUBLIC KEY-----"""

N, e = parse_rsa_public_key(key)

c1 = cipher
m2 = 2
c2 = (m2 ** e) % N

c12 = (c1 * c2) % N
m12 = int(decrypt(hex(c12)[2:]), 16)
# m12 = (m1^e * m2^e)^d = (m1 * m2) mod N

m1 = m12 // m2
solution = hex(m1)[2:]
print(solution)
