from datetime import datetime
import scrapy
import json
import re

from ..items import ScrapyMainItem, ScrapyPhotoItem

from .neagent import find_usd


class DomovitaSpider(scrapy.Spider):
    name = "domovita"
    allowed_domains = ["domovita.by"]
    start_urls = ["https://domovita.by/minsk/flats/rent?order=-date_revision"] #Room: https://domovita.by/minsk/room/rent?order=-date_revision

    def parse(self, response):
        url = response.css(".found_content > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > a").xpath("@href").get()
        
        return scrapy.Request(url=url, callback=self.parse_deeper)

    def parse_deeper(self, response):
   
        jsons = response.xpath("/html/head/script/text()").getall()
        count = 0
        
        jsons = jsons[2:6]
        #for i in jsons:
        #    count += 1
        #    print(f"Test {count}: {i}")
        json_1 = json.loads(jsons[0])
        json_2 = json.loads(jsons[1])
        json_3 = json.loads(jsons[2])
        json_4 = json.loads(jsons[3])
        
        locations = json_3["geo"]

        
        """
        Data:
        "amountUSD" 
        "amountBYN" 
        'rent_rooms' 
        'address' Done
        'url' 
        'created_at' 
        'agency' 
        'marketplace_id' 
        'location_a' Done
        'location_b' Done
        'description' 
        """
        main_item = ScrapyMainItem()
        
        main_item["amountBYN"] = json_2["priceRange"][1:]
        main_item["amountUSD"] = find_usd(main_item['amountBYN'])
        main_item["rent_rooms"] = json_3["numberOfRooms"]
        main_item["address"] = json_2['address']
        main_item["url"] = response.url
        main_item["created_at"] = str(datetime.now())
        if json_4["offers"]["seller"]["@type"] == "Organization":
            main_item['agency'] = True
        elif json_4["offers"]["seller"]["@type"] == "Person":
            main_item['agency'] = False
        main_item['marketplace_id'] = 5
        main_item['location_a'] = locations['longitude']
        main_item['location_b'] = locations['latitude']
        main_item['description'] = json_4["description"]
        main_item["phoneNumber"] = json_3['telephone']
        
        yield main_item
        
        photo_item = ScrapyPhotoItem()
        photo_item["url"] = response.url
        
        photos = response.css(".gallery").xpath("li/img/@data-src").getall() #.lSPager
        '''for i in photos.getall():
            with open("testDomovita.py", "w+") as file:
                file.write(str())'''
        for i in photos:
            photo_item['image'] = i
            yield photo_item
