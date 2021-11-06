import logging
import sys
import datetime
import pathlib


import twitter
import markovbot


def set_log():

    logfile = "./logs" / pathlib.Path(str(datetime.date.today()) + ".log")
    if not logfile.exists():
        logfile.touch()

    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s",
        level=logging.INFO,
        datefmt="%m/%d/%Y %I:%M:%S",
        filename=logfile,
    )


def main():
    if len(sys.argv) < 2:
        logging.warn("no file path specified")
        exit(1)

    datapath = pathlib.Path(sys.argv[1])
    if not datapath.exists():
        logging.warning("no tweets data fil")
        datapath.touch()

    session = twitter.mk_session()
    tl_text_list = twitter.gettl(session)

    with open(datapath, "a") as f:
        f.writelines(tl_text_list)
    generated_tweet = markovbot.gen_text(datapath)
    logging.info(generated_tweet)
    twitter.tweet(generated_tweet, session)
    print(generated_tweet)


if __name__ == "__main__":

    set_log()
    main()
