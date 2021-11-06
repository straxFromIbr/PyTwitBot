import re
import string

import emoji
import neologdn


def filter_text(tweet_text: str):
    # 絵文字削除
    for emc in emoji.UNICODE_EMOJI_ENGLISH:
        tweet_text = tweet_text.replace(emc, "")

    URL_pattern = r"http[\/\.\?\-:&#=_a-zA-Z0-9]*"
    res_text = re.sub(URL_pattern, "", tweet_text)

    ACC_pattern = r"@[A-Za-z0-9_]*"
    res_text = re.sub(ACC_pattern, "", res_text)

    # NB_pattern = r"[0-9]+"
    # res_text = re.sub(NB_pattern, "0", res_text)

    res_text = neologdn.normalize(res_text)
    for punc in string.punctuation:
        res_text = res_text.replace(punc, "")
    res_text = neologdn.normalize(res_text)
    if len(res_text) < 5:
        return None
    return "。".join(res_text.strip().split("\n"))
