import os
import pymysql

HOST = "localhost"
USER = os.environ.get('DB_USER')  # Database user
PASS = os.environ.get('DB_PASS')  # Database password
DATABASE = "IMDB"
TABLE = "imdb_scraped"  # Table name


class test_cls:

    def __init__(self):
        self.conn = pymysql.connect(host=self.HOST, user=self.USER, passwd=self.PASS, db=self.DATABASE)
        self.cur = self.conn.cursor()
        self.create_table()
        # self.insert_table()

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
        description blob,
        x_date varchar(10),
        x_project varchar(15),
        x_spider varchar(15),
        x_server varchar(30))""")



data = {"movie_code": "tt1655441", "name": "The Age of Adaline", "content_type": "Movie",
        "url": "https://www.imdb.com/title/tt1655441/", "certificate": "13", "year": "2015", "duration": "1h 52min",
        "directors": ["Lee Toland Krieger"], "creators": ["J. Mills Goodloe", "Salvador Paskowitz"],
        "genre": ["Drama", "Fantasy", "Romance"], "imdb_rating": 7.2,
        "description": "A young woman, born at the turn of the 20th century, is rendered ageless after an accident. After many solitary years, she meets a man who complicates the eternal life she has settled into.",
        "x_date": "16-06-2021", "x_project": "IMDB_Crawler", "x_spider": "imdb", "x_server": "DESKTOP-TB9O5SN"}

    # def insert_table():
    #     try:
    #
    #         insert_statement = f"INSERT INTO {TABLE} ({', '.join(data.keys())}) " \
    #                            f"VALUES ({placeHolders})"
    #         self.cur.execute(f"USE {DATABASE}")
    #         cur.execute(insert_statement, list(data.values()))
    #         conn.commit()
    #     except Exception as e:
    #         print("*********************************", e)
    #     finally:
    #         cur.close()
    #
