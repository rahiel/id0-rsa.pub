#!/usr/bin/env bash
printf "id0-rsa.pub" | sha256sum | cut -d " " -f 1 | xargs printf | md5sum
