import datetime
import logging
import pathlib
import sys

import markovbot
import twitter


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
        logging.warn("Requires an argument: tweets text file")
        exit(1)

    datapath = pathlib.Path(sys.argv[1])
    if not datapath.exists():
        logging.warning(f"New file {str(datapath)} was created.")
        datapath.touch()

    session = twitter.mk_session()
    tl_text_list = twitter.gettl(session)

    with open(datapath, "a") as f:
        f.writelines(tl_text_list)
    generated_tweet = markovbot.gen_text(datapath)
    logging.info(generated_tweet)
    ret = twitter.tweet(generated_tweet, session)

    if ret:
        return

    for _ in range(3):
        # 失敗したら何度か再試行
        generated_tweet = markovbot.gen_text(datapath)
        ret = twitter.tweet(generated_tweet, session)
        if ret:
            return


if __name__ == "__main__":

    set_log()
    main()
