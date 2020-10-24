# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CarvanaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    year = scrapy.Field()
    brand = scrapy.Field()
    model = scrapy.Field()
    trim = scrapy.Field()
    miles = scrapy.Field()
    price = scrapy.Field()
    monthly_pmt = scrapy.Field()
