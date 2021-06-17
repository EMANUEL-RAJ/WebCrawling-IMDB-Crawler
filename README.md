# IMDB-Crawler
A basic Scrapy project which crawlers imdb.com to scrap movie/TV data and inserts them into a specified MySQL table.

Consists of a single spider - 'imdb' which is responsible for crawling through the site and scraping data. It then passes the data to pipeline to be inserted into a MySQL table.
