m1 = "Deposit amount: 5 dollars"
c1 = "5797791557579e322e619f12b0ccdee8802015ee0467c419e7a38bd0a254da54"
m2 = "One million dolls is quite the collection"
c2 = "b1e952572d6b8e00b626be86552376e2d529a1b9cafaeb3ba7533d2699636323e7e433c10a9dcdab2ed4bee54da684ca"
m3 = "Hey nice binoculars"
c3 = "35d0c02036354fdf6082285e0f7bd6d2fdf526bd557b045bce65a3b3e300b55e"

# 2 hex characters is a byte, every 16 bytes is a AES-ECB block, so 32 hex is one block

m = m1[:16] + m2[:16] + m3[-3:]
c = c1[:16 * 2] + c2[:16 * 2] + c3[-32:]

assert len(c) % 32 == 0
print(c)
