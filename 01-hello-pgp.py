#!/usr/bin/env python3
from subprocess import run

from tqdm import tqdm

wordlist = "/usr/share/dict/words"

message = """-----BEGIN PGP MESSAGE-----
Version: GnuPG v1

jA0ECQMC8YL5GvIZ2m5g0ksB9aj386dbfatZ28jsaLEKtUcRLVjjHHIBmHvCIrxf
RIeH7NLMcfQ+3Z+/ktIu3Drocg9zoiP1eaJ6aUUpa6fLy0OPjIIpG9tM/Mo=
=S+SO
-----END PGP MESSAGE-----"""

with open(wordlist, 'r') as f:
    for line in tqdm(f.readlines()):
        if "'" in line:
            continue
        password = line.strip()
        gpg = run("echo '%s' | gpg -d --passphrase \"%s\" --no-use-agent 2> /dev/null" % (message, password), shell=True)
        if gpg.returncode == 0:
            print("\nPassword found: %s" % password)
            break

# passionately apathetic
# Password found: seamanship
