# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BlogworksItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    colSum = scrapy.Field()
    width = scrapy.Field()
    height = scrapy.Field()
    describeTitle = scrapy.Field()
    describeContent = scrapy.Field()
    describeDate = scrapy.Field()
    src = scrapy.Field()
    hot = scrapy.Field()
    like = scrapy.Field()
    poster = scrapy.Field()
    category = scrapy.Field()
    pass
