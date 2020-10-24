
from scrapy import Spider
from carvana.items import CarvanaItem

class CarvanaSpider(Spider):
    name = "carvana_spider"
    allowed_urls = ['https://www.carvana.com/']
    # start_urls based on average downpayment of $2,500 and monthly payment of less than $500/month
    start_urls = ['https://www.carvana.com/cars/filters/?cvnaid=eyJmaW5hbmNlIjp7ImRvd25QYXltZW50IjoyNTAwLCJtb250aGx5UGF5bWVudCI6NTAwfX0=']
    # Could potentially expand this to multiple links that segregate by body type

    def parse(self, response):
        #Do the for loop of pages then scrap the info then save to item
        pass
