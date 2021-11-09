import json
import logging

import requests_oauthlib

import config
import text_utils


def valid_source(tweet_json):
    return not (
        "torancell" in tweet_json["source"]
        or "Peing" in tweet_json["source"]
        or "IFTTT" in tweet_json["source"]
    )


def mk_session():
    # Setting Consts
    oa2_session = requests_oauthlib.OAuth1Session(
        config.CONSUMER_KEY,
        config.CONSUMER_KEY_SECRET,
        config.ACCESS_TOKEN,
        config.ACCESS_TOKEN_SECRET,
    )
    return oa2_session


def tweet(text: str, oa2_session):
    URL_posttweet = "https://api.twitter.com/1.1/statuses/update.json"

    params_posttweet = {"status": "[BOT] " + text}
    res = oa2_session.post(
        URL_posttweet,
        params=params_posttweet,
    )
    if res.status_code != 200:
        logging.error(res.text)
    return res.status_code == 200


def gettl(oa2_session):
    """
    -> [ツイート\n, ツイート\n, ツイート\n,  ...., ]
    """
    URL_gettweet = "https://api.twitter.com/1.1/statuses/home_timeline.json"
    params_gettweet = {
        "count": 200,
        "include_rts": "false",
        "exclude_replies": "true",
        "tweet_mode": "extended",
    }

    req = oa2_session.get(
        URL_gettweet,
        params=params_gettweet,
    )
    if req.status_code != 200:
        logging.error(req.text)
        return []

    tl_tweets = []
    response = json.loads(req.text)
    for tweet_json in response:
        if not valid_source(tweet_json):
            continue
        try:
            tweet_text = tweet_json["full_text"]
        except KeyError:
            tweet_text = tweet_json["text"]
        formatted_text = text_utils.filter_text(tweet_text)
        if formatted_text is not None:
            tl_tweets.append(formatted_text + "\n")

    return tl_tweets


if __name__ == "__main__":
    session = mk_session()
    print(gettl(session))
