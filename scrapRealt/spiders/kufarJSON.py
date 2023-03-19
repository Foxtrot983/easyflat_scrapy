import scrapy
# Пересмотреть куфар т.к. первые 2(??) объявления стоят старые из-за поднятия клиентов
# В идеале вообще найти перфект энд поинт с нужными объявлениями
a = "https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/poleposition?cat=1010&gtsy=country-belarus~province-minsk~locality-minsk&lang=ru&rnt=1&size=3&typ=let"
class KufarjsonSpider(scrapy.Spider):
    name = "kufarJSON"
    allowed_domains = ["https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/poleposition?cat=1010&gtsy=country-belarus~province-minsk~locality-minsk&lang=ru&rnt=1&size=3&typ=let"]
    start_urls = [a]

    def parse(self, response):
        print(response.body)
        pass
