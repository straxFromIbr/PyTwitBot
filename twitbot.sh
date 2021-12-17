#! /bin/bash
set -euxo pipefail
command cd "$(dirname "$0")"

tweets_data='./data/tweets.txt'
TW_PATH_BP='./data/tweets.txt.backup'
TW_SOURCE="$(mktemp)"

if ! test -e './data'; then
    mkdir './data'
fi

if ! test -e './logs'; then
    mkdir './logs'
fi

cp "${tweets_data}" "${TW_PATH_BP}"

python3 src/main.py gettl >> "${tweets_data}"
cat "${tweets_data}" \
    | sort \
    | uniq \
    | sort --random-sort \
    | head -n500 > "${TW_SOURCE}"

python3 src/main.py gentweet "${TW_SOURCE}"
