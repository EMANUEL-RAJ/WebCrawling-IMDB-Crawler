import re
import json
import socket
import scrapy
import datetime
from collections import defaultdict
from ..items import ImdbCrawlerItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class ImdbSpider(CrawlSpider):
    name = 'imdb'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/feature/genre/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=r'//*[@id="main"]/div[6]/span/div/div/div/div'), follow=True),  # Movie Block
        Rule(LinkExtractor(restrict_xpaths=r'//*[@id="main"]/div[7]/span/div/div/div/div'), follow=True),  # TV shows
        Rule(LinkExtractor(restrict_xpaths=r'//div[@class="lister-list"]//h3'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths=r'//div[@class="desc"]'), follow=True)  # Next page
    )

    def parse_item(self, response):
        """Extracts JSON data from each content (Movie/Tv Series/Tv programs)"""

        # Converting data and setting default value
        raw_data = json.loads(response.xpath('//script[@type="application/ld+json"]//text()').extract_first())
        data = defaultdict(lambda: None)
        for key, value in raw_data.items():
            data[key] = value

        # Item instance creation
        item = ImdbCrawlerItem()

        # Content IMDB code from URL
        item['movie_code'] = data['url'].split('/')[-2]

        # Content name
        item['name'] = data['name']

        # Content type - Movie or TV series
        item['content_type'] = data['@type']

        # IMDB url of content
        item['url'] = "https://www.imdb.com" + data['url']

        # Content certificate
        item['certificate'] = data['contentRating']

        # Release year
        item['year'] = response.xpath(
            '//span[@class="TitleBlockMetaData__ListItemText-sc-12ein40-2 jedhex"]/text()').get()

        # Content Duration
        if data['@type'] == "Movie" and data['duration']:
            temp = re.search(r'PT(\d+H)*(\d+M)*', data['duration'])
            hours, minutes = temp.groups()
            if hours == None: hours = '0'
            if minutes == None: minutes = '0'
            item['duration'] = f'{hours.replace("H", "")}h {minutes.replace("M", "")}min'
        else:
            item['duration'] = None

        # Content director
        if data['@type'] == "Movie":
            if data['director']:
                item['directors'] = ", ".join([x['name'] for x in data['director']])
        else:
            item['directors'] = None

        # Content creators
        x = []
        for temp in data['creator']:
            if temp['@type'] == 'Person':
                x.append(temp['name'])
        item['creators'] = ", ".join(x)

        # Genre
        item['genre'] = ",".join(data['genre'])

        # IMDB rating as of collected date
        if data['aggregateRating']:
            item['imdb_rating'] = data['aggregateRating']['ratingValue']

        # IMDB description of content
        item['description'] = re.sub(r'\s+', ' ', data['description']) if data['description'] is not None else None

        # Housekeeping fields
        item['x_date'] = datetime.datetime.now().strftime('%d-%m-%Y')
        item['x_project'] = self.settings.get('BOT_NAME')
        item['x_spider'] = self.name
        item['x_server'] = socket.gethostname()

        yield item
