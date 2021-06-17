import os
import logging
import pymysql


class ImdbCrawlerPipeline:

    HOST = "localhost"
    USER = os.environ.get('DB_USER')  # Database user
    PASS = os.environ.get('DB_PASS')  # Database password
    DATABASE = "IMDB"
    TABLE = "imdb_scraped"  # Table name

    def __init__(self):
        self.conn = pymysql.connect(host=self.HOST, user=self.USER, passwd=self.PASS, db=self.DATABASE)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute(f"USE {self.DATABASE}")
        self.cur.execute(f"DROP TABLE IF EXISTS {self.TABLE}")
        self.cur.execute(f"""CREATE TABLE {self.TABLE} (
        movie_code varchar(10) NOT NULL PRIMARY KEY,
        name varchar(30) NOT NULL,
        content_type varchar(15),
        url varchar(40),
        certificate varchar(10),
        year varchar(5),
        duration varchar(10),
        directors varchar(60),
        creators varchar(60),
        genre varchar(60),
        imdb_rating float(2,1),
        description text,
        x_date varchar(10),
        x_project varchar(15),
        x_spider varchar(15),
        x_server varchar(30))""")

    def process_item(self, data, spider):

        placeHolders = ", ".join(["%s"] * len(data))
        columns = ", ".join(data.keys())
        try:
            conn = pymysql.connect(host='localhost', user=self.USER, password=self.PASS, database='dummy_scrap')
            cur = conn.cursor()

            cur.execute(f"USE {self.DATABASE}")

            insert_statement = f"INSERT INTO {self.TABLE} ({columns}) VALUES ({placeHolders})"
            cur.execute(insert_statement, list(data.values()))

            conn.commit()
        except Exception as e:
            logging.error('Error occured when inserting data :', e)
        finally:
            logging.info('Inserted!')
            cur.close()
        return data
