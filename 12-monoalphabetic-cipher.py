from math import inf, log10
from os import system
from os.path import expanduser
from random import sample
from string import ascii_uppercase

from utils import md5

# this implements the attack described at:
# http://practicalcryptography.com/cryptanalysis/stochastic-searching/cryptanalysis-simple-substitution-cipher/
# using the quadgram data from:
# http://practicalcryptography.com/cryptanalysis/text-characterisation/quadgrams/

# This randomized algorithm can find a wrong solution when it's stuck in a
# local maximum, you may have to run this a couple of times.

ciphertext = "EANOEHHNFJLFXDGFANOYDJINTNOEDJXFOSBFESDOLGDWWSNUEDJNQCSJNUFEFFOUIDTTCOSIFESDOLNJKSINLEDNOXSONNJEZNSJMJDUCIELEDXCFJFOENNGFANOYDJINTNOEFIINLLEDFGGUFEFFYENJGNOXEZHUNWFENFOUKSXDJDCLMJNUSIESDOLDYNOYDJINTNOEIZFOONGLXDSOXUFJREZNLNFEENTMELEDJNXCGFENEZNNTNJXSOXSOENJONEANJNFWFOUDONUSOEZNSOENJKNOSOXHNFJLSOODKFESDODOEZNSOENJONEYGDCJSLZNUFOUGFANOYDJINTNOEFXNOISNLYDCOUONAFOUTDJNNYYNIESKNTNFOLDYFIINLLSOXKFLEGHGFJXNJQCFOESESNLDYUFEFEDUFHANFJNFXFSOZNFJSOXIFGGLYDJJNXCGFESDOEDTFOUFENEZNMJDKSLSDODYNPINMESDOFGFIINLLTNIZFOSLTLSOEZSLJNMDJEFXJDCMDYIDTMCENJLISNOESLELFOULNICJSEHNPMNJELTFOHDYAZDTMFJESISMFENUSOFLECUHDYEZNLNLFTNEDMSILZFLIDOKNONUEDNPMGDJNEZNGSRNGHNYYNIELDYSTMDLSOXNPEJFDJUSOFJHFIINLLTFOUFENLANZFKNYDCOUEZFEEZNUFTFXNEZFEIDCGUWNIFCLNUWHGFANOYDJINTNOENPINMESDOFGFIINLLJNQCSJNTNOELADCGUWNNKNOXJNFENJEDUFHEZFOSEADCGUZFKNWNNOHNFJLFXDSOEZNAFRNDYEZNXJDASOXNIDODTSIFOULDISFGIDLEDYEZNYCOUFTNOEFGSOLNICJSEHDYEDUFHLSOENJONENOKSJDOTNOEFOHMJDMDLFGLEZFEFGENJEZNLNICJSEHUHOFTSILDOGSONLZDCGUWNFMMJDFIZNUASEZIFCESDONPINMESDOFGFIINLLADCGUYDJINSOENJONELHLENTUNKNGDMNJLEDJNKNJLNYDJAFJULNIJNIHUNLSXOMJFIESINLEZFELNNREDTSOSTSBNEZNSTMFIEDOCLNJMJSKFIHAZNOLHLENTLFJNWJNFIZNUEZNIDTMGNPSEHDYEDUFHLSOENJONENOKSJDOTNOEASEZTSGGSDOLDYFMMLFOUXGDWFGGHIDOONIENULNJKSINLTNFOLEZFEONAGFANOYDJINTNOEJNQCSJNTNOELFJNGSRNGHEDSOEJDUCINCOFOESISMFENUZFJUEDUNENIELNICJSEHYGFALWNHDOUEZNLNFOUDEZNJENIZOSIFGKCGONJFWSGSESNLEZNMJDLMNIEDYXGDWFGGHUNMGDHNUNPINMESDOFGFIINLLLHLENTLJFSLNLUSYYSICGEMJDWGNTLFWDCEZDALCIZFONOKSJDOTNOEADCGUWNXDKNJONUFOUZDAEDNOLCJNEZFELCIZLHLENTLADCGUJNLMNIEZCTFOJSXZELFOUEZNJCGNDYGFA"


quadgram_scores = {}
total = 0
with open(expanduser("~/Documents/english_quadgrams.txt")) as f:
    for line in f:
        quadgram, count = line.strip().split(" ")
        count = int(count)
        quadgram_scores[quadgram] = count
        total += count
for q in quadgram_scores:
    quadgram_scores[q] = log10(quadgram_scores[q] / total)
default_qscore = -9.63   # something close to and smaller than log10(1 / total)

def english_score(text, quadgram_scores):
    quadgrams = [text[i:i+4] for i in range(len(text) - 3)]
    return sum(quadgram_scores.get(q, default_qscore) for q in quadgrams)

def decrypt(ciphertext, key):
    return "".join([key[c] for c in ciphertext])

def find_key(ciphertext):
    key = {c: c for c in ascii_uppercase}
    score = -inf
    invariance = 0

    while True:
        a, b = sample(ascii_uppercase, 2)
        new_key = key.copy()
        new_key[a] = key[b]
        new_key[b] = key[a]

        m = decrypt(ciphertext, new_key)
        new_score = english_score(m, quadgram_scores)
        if new_score >= score:
            key = new_key
            score = new_score
            invariance = 0
            system("clear")
            print(m)
        else:
            invariance += 1

        if invariance > 1000:
            break
    return key


key = find_key(ciphertext)
message = decrypt(ciphertext, key)
print(md5(message))
