#!/usr/bin/env bash
printf "6794893f3c47247262e95fbed846e1a623fc67b1dd96e13c7f9fc3b880642e42" \
    | xxd -r -p \
    | openssl rsautl -inkey 03-rsa.pem -raw -decrypt \
    | xxd -p -c 8 \
    | tail -n 1
