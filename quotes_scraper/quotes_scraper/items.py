# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QuotesItem(scrapy.Item):
    quote = scrapy.Field()
    author = scrapy.Field()
    author_link = scrapy.Field()
    tags = scrapy.Field()



class QuotesJSItem(scrapy.Item):
    quote = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()