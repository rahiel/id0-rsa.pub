# Slightly harder passwords

The [hint][] makes them easy again. You may need [this][] to follow the hint, I
used the jumbo version of JtR.

``` shell
wget -O 41-rules.txt http://contest-2010.korelogic.com/rules.txt
sudo bash -c "cat 41-rules.txt >> /etc/john/john.conf"
john --wordlist=/usr/share/dict/words --rules=KoreLogicRulesL33t 41-hashes.txt
```

With as result:
``` text
?:u$e
?:Th3
?:l4$t
?:0f
?:3@ch
?:w0rd

6 password hashes cracked, 1 left
```

John didn't crack the hash for "letter", but we can guess it.

[hint]: https://twitter.com/id0rsa/status/761809948388958208
[this]: http://www.openwall.com/lists/john-users/2012/12/29/27
