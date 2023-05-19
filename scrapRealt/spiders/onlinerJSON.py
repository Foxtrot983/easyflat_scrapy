import scrapy
import json
from ..items import ScrapyMainItem, ScrapyPhotoItem

from scrapy import Request

import re
#a = "https://r.onliner.by/sdapi/ak.api/search/apartments?bounds%5Blb%5D%5Blat%5D=53.789700075031824&bounds%5Blb%5D%5Blong%5D=27.232360839843754&bounds%5Brt%5D%5Blat%5D=54.00615463152166&bounds%5Brt%5D%5Blong%5D=27.891540527343754&v=0.6513377509620155"
#b = "https://r.onliner.by/sdapi/ak.api/search/apartments?rent_type%5B%5D=room&bounds%5Blb%5D%5Blat%5D=53.789700075031824&bounds%5Blb%5D%5Blong%5D=27.232360839843754&bounds%5Brt%5D%5Blat%5D=54.00615463152166&bounds%5Brt%5D%5Blong%5D=27.891540527343754&page=1&v=0.3372769990397295"
#all = https://r.onliner.by/sdapi/ak.api/search/apartments?bounds%5Blb%5D%5Blat%5D=53.789700075031824&bounds%5Blb%5D%5Blong%5D=27.232360839843754&bounds%5Brt%5D%5Blat%5D=54.00615463152166&bounds%5Brt%5D%5Blong%5D=27.891540527343754&v=0.6513377509620155

class OnlinerjsonSpider(scrapy.Spider):
    name = "onlinerJSON"
    allowed_domains = ["onliner.by"]
    start_urls = ['https://r.onliner.by/sdapi/ak.api/search/apartments?bounds%5Blb%5D%5Blat%5D=53.789700075031824&bounds%5Blb%5D%5Blong%5D=27.232360839843754&bounds%5Brt%5D%5Blat%5D=54.00615463152166&bounds%5Brt%5D%5Blong%5D=27.891540527343754&v=0.6513377509620155']
    
    def parse(self, response):
        data = json.loads(response.body)['apartments'][0]
        try:
            room_string = int(data["rent_type"].split("_")[0])
        except ValueError:
            room_string = 0

        yield Request(
            url=data['url'], 
            callback=self.parse_page2, 
            meta={
            "amountUSD": int(float(data["price"]["converted"]["USD"]["amount"])),
            "amountBYN": int(float(data["price"]["converted"]["BYN"]["amount"])),
            'rent_rooms': room_string,
            'address': data['location']['address'],
            'url': data["url"],
            'created_at': data["created_at"],
            'agency': data["contact"]["owner"],
            'description': "Test",
            'marketplace_id': 0, #Это можно убрать
            'location_a': str(data['location']['latitude']),
            'location_b': str(data['location']['longitude']),
            }) 
        
    
    def parse_page2(self, response):
        main_item = ScrapyMainItem()
        
        text = response.css(".apartment-info__sub-line_extended-bottom::text").getall()
        main_item["amountUSD"] = response.meta["amountUSD"]
        main_item["amountBYN"] = response.meta["amountBYN"]
        main_item['rent_rooms']: int =response.meta['rent_rooms']
        main_item['address']: str = response.meta['address']
        main_item['url']: str = response.meta['url']
        main_item['created_at']: str = response.meta['created_at']
        main_item['agency']: bool = False if response.meta['agency'] else True 
        main_item['marketplace_id'] = 1
        main_item['location_a'] = response.meta['location_a']
        main_item['location_b'] = response.meta['location_b']
        main_item['description'] = ("".join(text)).strip()
        main_item['phoneNumber'] = response.css(".apartment-info__item_secondary").xpath('a/text()').get()
        yield main_item
        #print(main_item)
        '''yield Request(url=response.meta['url'], callback=self.parse_photo, dont_filter = True, meta = {
            "url": str(response.meta["url"]),
        })'''
        #print(main_item)
        
        photo_item = ScrapyPhotoItem()
        url = str(response.meta["url"])

        #photo_item['image'] = "testURL"
        photo_item['url'] = url
        links = response.xpath('/html/body/div[1]/div/div/div[2]/div/div/div[2]/div[2]/div/div').getall()
        dic = list()
        for i in links:
            dic.append(re.findall(r'url\((.*)\)', i))
        for i in range(1): #Лишний цикл???? В целом намудрил, можно было просто взять через xpath и свойства
            for j in dic[i]:
                photo_item['image'] = j
                yield photo_item            
                #print(photo_item)

#    def parse_photo(self, response):
#        photo_item = ScrapyPhotoItem()
#        url = str(response.meta["url"])
#
#        #photo_item['image'] = "testURL"
#        photo_item['url'] = url
#        links = response.xpath('/html/body/div[1]/div/div/div[2]/div/div/div[2]/div[2]/div/div').getall()
#        dic = list()
#        for i in links:
#            dic.append(re.findall(r'url\((.*)\)', i))
#        for i in range(1): #Лишний цикл????
#            for j in dic[i]:
#                photo_item['image'] = j
#                yield photo_item            
#        print("Photo is done")
