import logging
import pathlib
import random

import MeCab
import markovify

# parser = MeCab.Tagger("-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd")


def parse_text(text: str, parser) -> str:
    parsed = parser.parse(text)
    if parsed is None:
        return " ".join(text.split())

    words_list = [
        morph.split("\t")[0]
        for morph in parsed.split("\n")
        if len(morph) != 0 and morph != "EOS"
    ]

    words = " ".join(words_list)
    return words


def gen_text(datapath: pathlib.Path) -> str:
    parser = MeCab.Tagger()
    with open(datapath) as dataf:
        text_list = dataf.readlines()

    text = [parse_text(line.strip(), parser) for line in text_list]
    text_model = markovify.NewlineText(text)
    try:
        result = text_model.make_short_sentence(140)
    except Exception as e:
        logging.error(e)
        raise e

    if result is None:
        return random.choice(text_list)
    return result.replace(" ", "")


if __name__ == "__main__":
    path = pathlib.Path("./tweets.txt")
    print(gen_text(path))
