import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from scrapy.spiders import Spider
from scrapy.selector import Selector
from dirbot.items import AppInfo, Category
import scrapy
from urllib import unquote
import re
import uuid


class DmozSpider(Spider):
    name = "apple"
    allowed_domains = ["itunes.apple.com"]

    def start_requests(self):
        yield scrapy.Request('https://itunes.apple.com/cn/genre/ios/id36?mt=8', self.parse)

    def parse(self, response):
        """ The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """

        my_item = Category()
        app_url = unquote(response.url)
        my_item['link'] = app_url
        app_categorys = response.xpath('//li/a[@class="top-level-genre"]/text()').extract()
        my_item['app_categorys'] = app_categorys
        yield my_item
        for url in response.xpath('//div[@class="grid3-column"]//ul//li//a/@href').extract():
            category = re.findall(r"https://itunes.apple.com/cn/genre/ios-(.*)/.*?", url)
            yield scrapy.Request(url, meta={'category': category}, callback=self.app_category_parse)

    def app_category_parse(self, response):
        app_category = response.meta['category']
        app_urls = response.xpath('//div[@id="selectedcontent"]//ul//li//a/@href').extract()
        for app_url in app_urls:
            yield scrapy.Request(app_url, meta={'category': app_category}, callback=self.app_parse)

    def app_parse(self, response):
        app_item = AppInfo()
        app_category = response.meta['category']
        app_item['app_url'] = response.url
        app_item['app_category'] = unquote(app_category[0])
        app_item['app_name'] = response.xpath('//div/header/h1[@class="product-header__title app-header__title"]/text()').extract()
        app_item['app_content'] = response.xpath('//div/header/h2[@class="product-header__subtitle app-header__subtitle"]/text()').extract()
        app_item['app_en_content'] = response.xpath('//div/header/h2[@class="product-header__identity app-header__identity"]/a/text()').extract()
        app_item['app_rank'] = response.xpath('//div/header/ul/li/ul/li[@class="inline-list__item"]/text()').extract()
        app_item['app_comment'] = response.xpath('//div/header/ul/li/ul/li/figure/@aria-label').extract()
        yield app_item

