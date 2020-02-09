from abc import ABC
from pymongo import MongoClient
import psycopg2
from psycopg2 import sql
from psycopg2.extras import DictCursor
from datetime import datetime, timedelta


class Datastore(ABC):
    def save(self, json_item: dict):
        """
        Save data to datastore if it doesn't exist
        """
    
    def load_by_date(self, date: datetime):
        """
        Load news by day
        """


class Mongo(Datastore):
    def __init__(self, url: str, database: str, collection: str):
        self.client = MongoClient(url)
        self.db = self.client[database]
        self.collection = self.db[collection]

    def save(self, json_item: dict):
        if not self.collection.find_one(json_item):
            self.collection.insert_one(json_item)
            print('Save to mongo {}'.format(json_item.get('title')))


    def load_by_date(self, date):
        # get data from db
        dayend = date + timedelta(days=1)
        query = {"published": {"$gte": date, "$lt": dayend}}
        results = self.collection.find(query).sort("published")
        
        #remove _id fields and create list of dict representation of news
        datalist = []
        for res in results:
            del res['_id']
            datalist.append(res)
        print('Found {} news!'.format(len(datalist)))
        return datalist

class Postgres(Datastore):
    def __init__(self, host: str, dbname: str, user: str, password: str, tablename: str):
        self.tablename = tablename
        self.dbname = dbname
        self.conn = psycopg2.connect(
            host=host, dbname=dbname, user=user, password=password
        )
        self.conn.autocommit = True

    def save(self, json_item: dict):
        with self.conn.cursor() as cursor:
            values = (json_item["title"], json_item["description"], json_item["published"], json_item["url"], json_item["full_text"])
            try:
                cursor.execute(
                    "INSERT INTO {} (title, description, published, url, full_text) VALUES (%s, %s, %s, %s, %s)".format(
                        self.tablename),
                    values)
            except psycopg2.errors.UniqueViolation:
                # If already exist do nothing
                pass
    
    def load_by_date(self, date: datetime):
        raise NotImplementedError