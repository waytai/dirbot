from scrapy.item import Item, Field
import scrapy


class Category(Item):
    link = scrapy.Field()
    app_categorys = scrapy.Field()


class AppInfo(Item):
    app_name = scrapy.Field()
    app_category = scrapy.Field()
    app_rank = scrapy.Field()
    app_content = scrapy.Field()
    app_en_content = scrapy.Field()
    app_url = scrapy.Field()
    app_comment = scrapy.Field()

