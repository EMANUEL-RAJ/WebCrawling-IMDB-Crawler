import scrapy


class ImdbCrawlerItem(scrapy.Item):
    """Data collected from a movie or TV-series page of IMDB"""

    # Primary Fields
    movie_code = scrapy.Field()  # code that is unique for content in IMDB
    name = scrapy.Field()
    content_type = scrapy.Field()  # Movie or TV series
    url = scrapy.Field()  # URL of imdb page
    certificate = scrapy.Field()
    duration = scrapy.Field()  # NA for Tv series
    year = scrapy.Field()
    genre = scrapy.Field()
    actors = scrapy.Field()
    directors = scrapy.Field()  # NA for Tv series
    creators = scrapy.Field()
    imdb_rating = scrapy.Field()
    description = scrapy.Field()

    # Housekeeping fields
    x_date = scrapy.Field()  # date in which data was collected
    x_project = scrapy.Field()  # project under which data was collected
    x_spider = scrapy.Field()  # spider which collected the data
    x_server = scrapy.Field()  # server which collected the data
