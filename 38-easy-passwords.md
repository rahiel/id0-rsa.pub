# Easy Passwords

I did not recognize the hash format. The
website <https://www.onlinehashcrack.com/hash-identification.php> gave as
identification:
``` text
md5crypt, MD5(Unix), FreeBSD MD5, Cisco-IOS MD5
```

Searching for md5crypt we can read about the hash format:
<https://en.wikipedia.org/wiki/Crypt_(C)>.

[John the Ripper][] (available in [Debian][]) is a password cracker that
supports many crypt(3) password hash types.

[John the Ripper]: http://www.openwall.com/john/
[Debian]: https://packages.debian.org/sid/john

From the [hint][] we learn that all passwords are standard English words, so we
can use a simple wordlist.

[hint]: https://twitter.com/id0rsa/status/761652735280189440

After putting the hashes in a file called `38-hashes.txt`, we let john do its
job:
``` shell
sudo john --wordlist=/usr/share/dict/words 38-hashes.txt
```

After a while we look at the results with `sudo john --show 38-hashes.txt`:
``` text
?:the
?:second
?:letter
?:each
?:word
?:in
?:this
?:list
?:in
?:order

10 password hashes cracked, 1 left
```
Notice that two passwords are the same, they also have the same hash. John could
not crack the hash for `of` but we can infer it from the context of the other
passwords.
