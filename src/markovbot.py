import logging
import pathlib
import random

import markovify
from fugashi import fugashi

import text_utils


def parse_text(text: str, parser) -> str:
    filterd = text_utils.filter_text(text)
    if filterd is None:
        filterd = text

    parsed = parser(filterd)
    if parsed is None:
        return " ".join(filterd.split())
    res_text = ""
    for w in parsed:
        res_text += str(w) + " "
    return res_text.strip()


def gen_text(datapath: pathlib.Path) -> str:
    parser = fugashi.Tagger()
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
    path = pathlib.Path("../data/tweets.txt")
    print(gen_text(path))
