# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
# Добавить main_item["phoneNumber"] на neagent, realt %Там не отображает телефонный номер%


import scrapy

class ScrapyMainItem(scrapy.Item):
    amountUSD = scrapy.Field()
    amountBYN = scrapy.Field()
    rent_rooms = scrapy.Field()
    address = scrapy.Field()
    url = scrapy.Field()
    created_at = scrapy.Field()
    agency = scrapy.Field()
    description = scrapy.Field()
    marketplace_id = scrapy.Field()
    location_a = scrapy.Field()
    location_b = scrapy.Field()
    phoneNumber = scrapy.Field()

class ScrapyPhotoItem(scrapy.Item):
    image = scrapy.Field()
    house_id = scrapy.Field()
    url = scrapy.Field()
