#! /bin/bash
set -euxo pipefail
command cd "$(dirname "$0")"

TW_PATH='./data/tweets.txt'
TW_PATH_BP='./data/tweets.txt.backup'

if ! test -e './data'; then
    mkdir './data'
fi

if ! test -e './logs'; then
    mkdir './logs'
fi

touch "${TW_PATH}"
cp "${TW_PATH}" "${TW_PATH_BP}"

cat "${TW_PATH_BP}" \
    | sort \
    | uniq  > "${TW_PATH}"

env python3 src/main.py "${TW_PATH}"
