from scrapy.item import Item, Field
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from lxml import html



class City(Item):
    name = Field()
    state = Field()
    weather = Field()

class Accuweather(CrawlSpider):
    name = 'accuweather'

    custom_settings = {
        'USER_AGENT' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        'CLOSESPIDER_PAGECOUNT': 101
    }

    allowed_domains = ['www.accuweather.com']

    download_delay = 2

    start_urls = ["https://www.accuweather.com/es/browse-locations/nam/mx"]

    rules = (
        Rule(
            LinkExtractor(
                allow=r'/nam/mx/bcn',
            ), follow=True
        ),

        Rule(
            LinkExtractor(
                allow=r'key=\d+'
            ), follow=True, callback='parse_weather'
        )
    )

    def clean_city_name(self, name):
        city_name = name.split(',')[0]
        return city_name.strip()

    def clean_city_state(self, name):
        city_state = name.split(',')[-1]
        return city_state.strip()

    def clean_weather(self,weather_text):
        weather_html = html.fromstring(weather_text)
        day_expression = '//div[@class="daily-list-body"]//div[@class="date"]/p[position()=2]/text()'
        low_expression = '//div[@class="daily-list-body"]//span[@class="temp-lo"]/text()'
        high_expression = '//div[@class="daily-list-body"]//span[@class="temp-hi"]/text()'
        
        days = weather_html.xpath(day_expression)
        lows = weather_html.xpath(low_expression)
        highs = weather_html.xpath(high_expression)

        lows = [int(text[:-1]) for text in lows]
        highs = [int(text[:-1]) for text in highs]


        zipped_values = zip(days,lows,highs)
        keys = ['day','low_temp','high_temp']
        list_of_dicts = [dict(zip(keys, values)) for values in zipped_values]

        return list_of_dicts

    def parse_weather(self, response):
        item = ItemLoader(City(),response)
        item.add_xpath('name','//h1[@class="header-loc"]/text()',
                        MapCompose(self.clean_city_name)
                        )
        item.add_xpath('state','//h1[@class="header-loc"]/text()',
                        MapCompose(self.clean_city_state)
                        )
    
        item.add_xpath('weather','//div[@class="daily-list-body"]',
                       MapCompose(self.clean_weather))
        yield item.load_item()