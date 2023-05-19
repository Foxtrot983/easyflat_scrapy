import scrapy

import json

from ..items import ScrapyMainItem
from ..items import ScrapyPhotoItem

"""
Data:
"amountUSD" done
"amountBYN" done
'rent_rooms' done
'address' In Progress
'url' Done
'created_at' Done
'agency' Done
'marketplace_id' Done
'location_a' Done
'location_b' Done
'description' Almost
"""


class RealtSpider(scrapy.Spider):
    name = "realt"
    allowed_domains = ["realt.by"]
    start_urls = [
        "https://realt.by/rent/flat-for-long/?search=all&sortType=updatedAt&page=1",
        "https://realt.by/rent/room-for-long/?sortType=updatedAt&page=1"
        ]
    #https://realt.by/rent/flat-for-long/?search=all#tabs
    #https://realt.by/rent/flat-for-long/?search=eJyLL04tKS1QNXUqzi8qiU%2BqVDV1AXIMgJRtSmJJanxRallmcWZ%2Bnlo8TGFRanJ8QWpRfEFieipImbEBAC0BF0w%3D"]

    def parse(self, response):

        url = response.css(".t-0 > div > div  > div > div > a").xpath("@href").get()
        
        url =f"https://realt.by{str(url)}"
        print(f"Test URL: {url}")
        return scrapy.Request(url=url, callback=self.parse_deeper, meta={"url": url, "prev_url": response.url})
    
    
    def parse_deeper(self, response):
        '''
        #print(f"Func URL Test:{response.meta}")
        print("Test Func")
        #amountUSD
        #costs = response.css(".md\:items-center > div:nth-child(1)")
        
        #byn = costs.xpath("h2/text()").get()
        #byn = int(re.findall(r"\d+", byn)[0])
        
        #usd = costs.xpath("span").get()
        #usd = int(re.findall(r"\d+", usd)[0])
        
        #print(f"{byn} |||||| {usd}")
        byn_cost = response.css(".md\:items-center > div:nth-child(1) > h2:nth-child(1)::text").get()
        print(type(byn_cost))
        print(byn_cost)
        amountBYN = int(re.findall(r"\d+", byn_cost)[0])
        print(amountBYN)
        #amountUSD = usd
        #amountBYN = byn
        
        #title: str = response.css("h1.order-1 > span:nth-child(1)::text").get()
        #rent_rooms = int(re.findall(r"\d", title)[0])
        #print(rent_rooms)
        #address_raw = title.split(",")
        #address_raw = address_raw[2:]
        #address = ','.join(address_raw)
        #address1 = address.strip()
        
        #address2 = response.css("a.inline:nth-child(3)::text").get()
        #print(address2)
        
        #address = address1 #or address2
        
        #url = response.meta["url"]
        #print(url)
        
        
        #????created_at = datetime.now()
        #print(f"{created_at} | {type(created_at)}")
        
        
        #agency_check = response.css("div.md\:p-6:nth-child(1) > div:nth-child(2) > div").get()
        #if agency_check:
        #    agency = False
        #else:
        #    agency = True
        
        #agency
        #print(agency)
        
        #marketplace_id = 3
        
        #with open("realt.json", "w+") as file:
        #    file.write(str(definetaly_json))
        #    file.close()
        #location_a
        #location_b
        #description'''

        #By JSON
        probably_json = response.css("#__NEXT_DATA__::text").get()
        definetaly_json = json.loads(probably_json)

        
        flat_json = definetaly_json['props']['pageProps']['initialState']['objectView']["object"]
        locations = flat_json["location"]
        
        amountUSD = flat_json['priceRates']['840']
        amountBYN = flat_json['priceRates']['933']
        #print(self.start_urls)
        if response.meta["prev_url"] == "https://realt.by/rent/room-for-long/?sortType=updatedAt&page=1":
            #print('TEST PrevURL 1')
            rent_rooms = 0
        elif response.meta["prev_url"] == "https://realt.by/rent/flat-for-long/?search=all&sortType=updatedAt&page=1":
            #print('TEST PrevURL 2')
            rent_rooms = flat_json["rooms"]
        address = flat_json["address"]
        url = response.meta["url"]
        created_at = flat_json['raiseDate']
        
        agency_check = flat_json["agency"]
        agency = False if agency_check==None else True
        
        marketplace_id = 3
        location_a = locations[0]
        location_b = locations[1]
        description = flat_json["comments"]
        phoneNumber = definetaly_json['props']['pageProps']['initialState']['objectView']['showcases'][0]['phone_international']
        
        main_item = ScrapyMainItem()
        
        main_item["amountUSD"] = amountUSD
        main_item["amountBYN"] = amountBYN
        main_item["rent_rooms"] = rent_rooms
        main_item["address"] = address
        main_item["url"] = url
        main_item["created_at"] = created_at
        main_item["agency"] = agency
        main_item["marketplace_id"] = marketplace_id
        main_item["location_a"] = location_a
        main_item["location_b"] = location_b
        main_item["description"] = description
        main_item['phoneNumber'] = phoneNumber
        #print(main_item)
        yield main_item
        
        photo_item = ScrapyPhotoItem()
        
        photos = flat_json["slides"]
        photo_item["url"] = response.meta["url"]
        print(photos)
        for i in photos:
            if i[0] == "h":
                photo_item['image'] = i
                #print(photo_item)
                yield photo_item
        
        
