import scrapy
#from scrapy_splash import SplashRequest
#from scrapy_selenium import SeleniumRequest
from bs4 import BeautifulSoup
import requests
import re
import json

from ..items import ScrapyMainItem, ScrapyPhotoItem


def find_usd(byn: int):
    data = requests.get("https://myfin.by/currency/usd")
    soup = BeautifulSoup(data.content, 'html.parser')
    usd = soup.find("span", {"class": "accent"}).find_next().get_text()
    result = int(byn) / float(usd)
    return int(result)


def make_location(data: str):
    pass

    

a = r"https://neagent.by/?cat=kvartira%2Fsnyat&city=minsk&order=postdate_za" #Flats
b = r"https://neagent.by/komnata/snyat?order=postdate_za" #Rooms

class NeagentSpider(scrapy.Spider):
    name = "neagent"
    allowed_domains = ["neagent.by"]
    start_urls = [a, b]

    def parse(self, response):
        #print(response.body)
        content = BeautifulSoup(response.body, "html.parser")
        #print(type(content.prettify()))
        data = content.find("div", {"class": "c-card"})
        #print(str(a))
        #with open("test1.txt", "w+") as file:
        #    file.write(str(a))
        url = data.find("a", {"class": "js-ob-a"}).get("href")
        #url = b.get
        if response.url == self.start_urls[1]:
            rent_rooms = 0
        else:
            rent_rooms = 1
        return scrapy.Request(url=url, callback= self.parse_page, dont_filter=True, meta={
            "url": url,
            "rent_rooms": rent_rooms,
            })
        
        
    def parse_page(self, response):
        main_item = ScrapyMainItem()
        photo_item = ScrapyPhotoItem()
        
        print("TEST PARSE PAGE")
        #print(BeautifulSoup(response.body).prettify())
        content = BeautifulSoup(response.body, "html.parser")
        money = content.find("span", {"class": "ann-contact__price"}).get_text()
        money = re.findall("[0-9]", money)
        Byn = "".join(money)
        amountBYN = int(Byn)
        #print(amountBYN)
        amountUSD = find_usd(amountBYN)
        #print(amountUSD)
        rent_string = content.find("div", {"class": "key-value-item"}).find("div", {"class": "value"}).get_text().strip()
        #print(rent_string)
        if response.meta["rent_rooms"] != 0:
            rent_rooms = int(rent_string[0])
        else:
            rent_rooms = 0
        #print(f"{rent_string[0]} | {rent_rooms}")
        #'address' Буду делать через сплит тайтла 
        url = response.meta["url"]
        #print(response.meta["url"])
        created_at = content.find("div", {"data-jss": "time-to-be-parsed"}).get_text().strip()
        #print(f"Time: {created_at} + {url}")
        agency = False
        marketplace_id = 4
        
        #То что ниже вынести в отдельную функцию
        
        locations_raw = str(content.find("div", {"class": "map-margin241"}).find("script").find_next())
        locations_string = re.findall(r"\[[^\[\]]*\]", locations_raw.split("=")[1].strip())
        #print(locations_string[0])
        locations_json = json.loads(str(locations_string[0]))
        #print(f"{locations} + {type(locations)}")
        locations_dict = locations_json[0]["coord"].split(",")
        #print(locations_dict)
        
        
        location_a = locations_dict[0]
        location_b = locations_dict[1]
        description = content.find("div", {"class": "box ann-desc"}).find("div", {"class": "text-content"}).find("p").get_text().strip()
        #print(description)
        
        address_raw = content.find("div", {"class": "page-header"}).find("h1").get_text().strip()
        address_list = address_raw.split(",")
        address_list.pop(-1)
        address_list.pop(0)
        address = "".join(address_list)


        main_item["amountUSD"] = amountUSD
        main_item["amountBYN"] = amountBYN
        main_item['rent_rooms']: int = rent_rooms
        main_item['address']: str = address
        main_item['url']: str = url
        main_item['created_at']: str = created_at
        main_item['agency']: bool = agency
        main_item['marketplace_id'] = marketplace_id
        main_item['location_a'] = location_a
        main_item['location_b'] = location_b
        main_item['description'] = description
        
        yield main_item
        
        photo_item = ScrapyPhotoItem()
        
        photo_content = content.find("div", {"class": "b__simple-gallery__scrolled-pictures"})
        photo_content = photo_content.find_all("img")
        photo_list = list()
        for i in photo_content:
            photo_list.append(i["src"][2:])
        
        
        #print(photo_content)
        #print(photo_list)
        photo_item["url"] = url

        for i in photo_list:
            photo_item["image"] = i
            yield photo_item
        