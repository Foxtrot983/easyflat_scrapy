import scrapy
from scrapy import Request

import json
import re

from ..items import ScrapyMainItem, ScrapyPhotoItem

'''
Get DATA

#amountUSD
#amountBYN
#rent_rooms
#address
#url
#created_at
#agency
description parse_Text
#marketplace_id
#location_a
#location_b
'''
#Сделать рефактор функций
def address_search(data: dict()):
    data = data["account_parameters"]
    for key in data:
        if key['pl'] == "Адрес":
            k = key["v"]
            #print(f"TEST ADDRESS: {k}")
            return k

def location_search(data: dict()):
    data = data['ad_parameters']
    for key in data:
        if key['pl'] == "Координаты":
            #print("COOOFOFOFOFF")
            #print(key['v'])
            return key['v']

def rent_rooms_search(data: dict()):
    data = data['ad_parameters']
    for item in data:
        if item['pl'] == "Комнат":
            #print("roomsCOOOFOFOFOFF")
            #print(item['vl'])
            #print(type(item['vl']))
            return int(item['vl'])
    return 0        


a = r"https://api.kufar.by/search-api/v1/search/rendered-paginated?cat=1010&cur=USD&gbx=b%3A27.212256274414035%2C53.70053896068443%2C28.106268725585903%2C54.07614841678253&gtsy=country-belarus~province-minsk~locality-minsk&lang=ru&rnt=1&size=30&typ=let"
b = r'https://api.kufar.by/search-api/v1/search/rendered-paginated?cat=1040&cur=BYR&gtsy=country-belarus~province-minsk~locality-minsk&rnl=3&typ=let'
class KufarjsonSpider(scrapy.Spider):
    name = "kufarJSON"
    allowed_domains = ["api.kufar.by"]
    start_urls = [a, b]

    def parse(self, response):
        data = json.loads(response.body)['ads'][0]

        location = location_search(data)
        rent_rooms = rent_rooms_search(data)
        address = address_search(data)
        #print(data["account_parameters"])
        url = data['ad_link']
        #print(type(data))
        
        if data["company_ad"] == "false":
            agency = True
        else:
            agency = False

        #coordinates = json_coord_search(data=data)
        #print(f"Coordinates {coordinates}")

        stuff = {
            'amountUSD': data['price_usd'][:-2],
            'amountBYN': data['price_byn'][:-2],
            'rent_rooms': rent_rooms,
            'address': address, #data['account_parameters'][1]["v"],
            'url': url,
            'created_at': data['list_time'],
            'agency': agency,
            'description': "Parse_text",
            'marketplace_id': 2,
            'location_a': location[0],
            'location_b': location[1],
            }
        #print(stuff["url"])
        #print("TEEEEEEEEEEEEEEEEEEEESSSSSSSSSSSSSSST")
        #print(item)
        yield Request(
            url=data['ad_link'], 
            callback=self.parse2,
            dont_filter = True,
            meta={
            'amountUSD': stuff['amountUSD'],
            'amountBYN': stuff['amountBYN'],
            'rent_rooms': stuff['rent_rooms'],
            'url': url,
            'address': stuff['address'],
            'created_at': stuff['created_at'],
            'agency': stuff['agency'],
            'description': stuff['description'],
            'marketplace_id': stuff['marketplace_id'],
            'location_a': stuff['location_a'],
            'location_b': stuff['location_b'],
            }
            )
        #print('YIELD1 is done')


    def parse2(self, response):
        main_item = ScrapyMainItem()
        #print("TEST META")
        #print(response)
        text = response.css('.styles_description_content__S71g_').getall()
        res = list()
        for i in text:
            res.append(re.sub(r"<[^>]+>", "", i, flags=re.S))
        main_item["amountUSD"] = response.meta["amountUSD"]
        main_item["amountBYN"] = response.meta["amountBYN"]
        main_item['rent_rooms']: int =response.meta['rent_rooms']
        main_item['address']: str = response.meta['address']
        main_item['url']: str = response.meta['url']
        main_item['created_at']: str = response.meta['created_at']
        main_item['agency']: bool = response.meta['agency']
        main_item['marketplace_id'] = 2
        main_item['location_a'] = response.meta['location_a']
        main_item['location_b'] = response.meta['location_b']
        main_item['description'] = ''.join(res)
        #main_item['phoneNumber'] = Null
        #print(main_item)
        #print(f"TEXT:{main_item['description']}")
        yield main_item
    
        photo_item = ScrapyPhotoItem()
        
        photo_item['image'] = "testURL"
        photo_item['url'] = main_item['url']
        
        links = response.xpath('/html/body/div[1]/div[2]/div[1]/main/div/div[3]/div[2]/div[1]/div[1]/div/div[1]/div[2]/div/div').getall()
        dic = list()
        text = "".join(links)
        links_almost = re.findall(r'data-background="([^"]+)"', text)
        correct_line = '?rule=gallery'
        for i in links_almost:
            line = i.split("?")
            line[1] = correct_line
            done_line: str = ''.join(line)
            dic.append(done_line)
            #dic.append(i.replace("mobile_thumbs", "gallery"))
                
        for j in dic:
            photo_item['image'] = j
            yield photo_item
            #print(photo_item)
