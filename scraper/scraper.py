#! /bin/python
import argparse
from dateutil.parser import parse as parse_time
from datetime import datetime
import feedparser
import os
import requests
import time

from news import News
from datastore import Mongo, Postgres

# get configuration from environment
db_name = os.environ.get("DB_NAME")
db_table = os.environ.get("DB_TABLE")
db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASS")
postgres_host = os.environ.get("POSTGRES_HOST")
mongo_host = os.environ.get("MONGO_HOST")

# init datastores layer
datastores = (
    Mongo("mongodb://{}:27017/".format(mongo_host), db_name, db_table),
    Postgres(postgres_host, db_name, db_user, db_pass, db_table),
)


def get_csv_by_date(date, datastore=datastores[0], delimeter=","):
    date = parse_time(date)
    res = datastore.load_by_date(date)
    csv_head = "title{}description{}published{}url{}fulltext".format(
        delimeter, delimeter, delimeter, delimeter
    )
    csv_list = [csv_head]
    found = False
    for item in res:
        found = True
        csv_string = News.from_dict(item).to_csv(delimeter)
        csv_list.append(csv_string)
    if found:
        with open("{}.csv".format(date.date()), "w") as f:
            f.write("\n".join(csv_list))
    else:
        print("No news at {}".format(date.date()))


def save_feed(datastores=datastores):
    """
    Load and save news to datastores
    """
    # get feed
    feed = feedparser.parse("http://feeds.reuters.com/reuters/topNews")

    for item in feed["items"]:
        # create News object
        news_item = News.from_feed(item)
        # get full text
        news_html = requests.get(news_item.url, timeout=5)
        news_item.set_text_from_html(news_html.text)
        # save to datastores
        for ds in datastores:
            ds.save(news_item.to_dict())


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Parse news from reuters and save to db"
    )
    parser.add_argument("--parse", action="store_true", help="start parsing process")
    parser.add_argument("--get", default=None, help="create csv file with news")
    parser.add_argument(
        "--parse_forever", action="store_true", help="start parsing process every hour"
    )

    args = parser.parse_args()
    if args.parse:
        save_feed()
        print("Done")
    if args.get:
        get_csv_by_date(args.get)
        print("File created")
    if args.parse_forever:
        print('Started parsing every hour')
        while True:
            save_feed()
            time.sleep(60 * 60)

