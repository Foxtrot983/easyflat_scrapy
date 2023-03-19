import scrapy
import json


class OnlinerjsonSpider(scrapy.Spider):
    name = "onlinerJSON"
    allowed_domains = ["onliner.by"]
    start_urls = ["https://r.onliner.by/sdapi/ak.api/search/apartments?order=created_at%3Adesc"]

    def parse(self, response):
        data = json.loads(response.body)['apartments'][0]
        print(type(data))
        print(data)
        pass
