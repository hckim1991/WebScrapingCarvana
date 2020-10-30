
from scrapy import Spider, Request
from carvana.items import CarvanaItem
import re
from math import ceil

class CarvanaSpider(Spider):
    name = "carvana_spider"
    allowed_urls = ['https://www.carvana.com/']
    # start_urls based on average downpayment of $2,500 and monthly payment of less than $500/month
    start_urls = ['https://www.carvana.com/cars/filters/?cvnaid=eyJwcmljZSI6eyJtaW4iOjIyMTQ1LCJtYXgiOjI5NTI3fX0=']
    # Could potentially expand this to multiple links that segregate by body type

    def parse(self, response):
        page_number = ceil(int(re.findall('\d+', response.xpath('//span[@data-qa="pagination-text"]/text()').extract()[3])[0]) / 20)
        #Generally 20 items per page but not always
        urls = [f'https://www.carvana.com/cars/filters/?cvnaid=eyJwcmljZSI6eyJtaW4iOjIyMTQ1LCJtYXgiOjI5NTI3fX0=&page={x}' for x in range(1, page_number)]

        for url in urls:
            yield Request(url = url, callback = self.parse_product_page)

    def parse_product_page(self, response):
        products = response.xpath('//section[@data-qa="results-section"]/div[@data-qa="result-tile"]')
        for product in products:
            try:
                year = int(product.xpath('.//h3[@data-qa="result-tile-make"]/text()').extract_first().split()[0])
            except:
                year = None
                print('='*50)
                print('No year. Offending url is {response.url}')
                print('='*50)

            try:
                brand = product.xpath('.//h3[@data-qa="result-tile-make"]/text()').extract_first().split()[1]
            except:
                brand = None
                print('='*50)
                print('No brand. Offending url is {response.url}')
                print('='*50)

            try:
                model = product.xpath('.//h3[@data-qa="result-tile-model"]/text()').extract_first()
            except:
                model = None
                print('='*50)
                print('No model. Offending url is {response.url}')
                print('='*50)

            try:
                trim = product.xpath('.//h4[@data-qa="vehicle-trim"]/text()').extract_first()
            except:
                trim = None
                print('='*50)
                print('No trim. Offending url is {response.url}')
                print('='*50)

            try:
                miles = int(product.xpath('.//h4[@data-qa="vehicle-mileage"]/text()').extract_first().split()[0].replace(',', ''))
            except:
                miles = None
                print('='*50)
                print('No miles. Offending url is {response.url}')
                print('='*50)

            try:
                price = int(product.xpath('.//span[@property="price"]/text()').extract_first().replace(',', ''))
            except:
                price = None
                print('='*50)
                print('No price. Offending url is {response.url}')
                print('='*50)

            try:
                monthly_pmt = int(re.findall('\d+', product.xpath('.//span[@data-qa="monthly-payment"]/text()').extract_first().split()[1])[0])
            except:
                monthly_pmt = None
                print('='*50)
                print('No montly payment. Offending url is {response.url}')
                print('='*50)

            try:
                shipping = product.xpath('.//div[@data-qa="shipping-cost"]/text()').extract_first()
            except:
                shipping = None
                print('='*50)
                print('No shipping info. Offending url is {response.url}')
                print('='*50)

            item = CarvanaItem()
            item['year'] = year
            item['brand'] = brand
            item['model'] = model
            item['trim'] = trim
            item['miles'] = miles
            item['price'] = price
            item['monthly_pmt'] = monthly_pmt
            item['shipping'] = shipping
            yield item
