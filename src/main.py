import datetime
import logging
import pathlib
import sys

import markovbot
import twitter


def set_log():
    logfile = "./logs" / pathlib.Path(str(datetime.date.today()) + ".log")
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s",
        level=logging.INFO,
        datefmt="%m/%d/%Y %I:%M:%S",
        filename=logfile,
    )


if __name__ == "__main__":
    set_log()
    if len(sys.argv) < 2:
        logging.warn("Requires an argument: tweets text file")
        exit(1)

    session = twitter.mk_session()
    if sys.argv[1] == "gettl":
        tl_text_list = twitter.gettl(session)
        print(tl_text_list)
        exit(0)

    if sys.argv[1] == "gentweet":
        exit(1) if len(sys.argv) < 2 else ...

        datapath = pathlib.Path(sys.argv[2])

        generated_tweet = markovbot.gen_text(datapath)
        logging.info(generated_tweet)
        ret = twitter.tweet(generated_tweet, session)
        exit(0) if ret else ...

        for _ in range(3):
            # 失敗したら何度か再試行
            generated_tweet = markovbot.gen_text(datapath)
            ret = twitter.tweet(generated_tweet, session)
            exit(0) if ret else ...
    exit(1)
