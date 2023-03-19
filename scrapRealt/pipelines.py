# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .models import db_connect, create_table, House, HousePhoto
from sqlalchemy.orm import sessionmaker 


'''
class ScrapRealtPipeline:
    def __init__(self):
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)


    def process_item(self, item, spider):
        #session = self.Session()
        """data = NewsItem(**item)
        #log.INFO('This Point')

        try:
            session.add(news)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()"""

        return item
class SaveOnlinerPipelines:
    def __init__(self):
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)


    def process_item(self, item, spider):
        session = self.Session()
        """data = NewsItem(**item)
        #log.INFO('This Point')

        try:
            session.add(news)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()"""

        return item
    '''


class SaveItemPipelines:
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

        self.house = House 
        self.house_photo = HousePhoto
        
    
    def process_item(self, item, spider):
        session = self.Session()

        #house = House 
        #house_photo = HousePhoto
        #marketplace = Marketplace
        house_db = self.house
        house_photo_db = self.house_photo
        #marketplace_db = self.marketplace

        house_db.amountUSD = item["amountUSD"]
        house_db.amountBYN = item["amountBYN"]
        house_db.rent_rooms = item["rent_rooms"]
        house_db.address = item["address"]
        house_db.url = item["url"]
        house_db.created_at = item["created_at"]
        house_db.agency = item["agency"]
        house_db.description = item["description"]
        house_db.marketplace_id = item["marketplace_id"]
        house_db.marketplace = item["marketplace"]

        house_photo_db.house_id = item['house_id']
        house_photo_db.image = item["image"]