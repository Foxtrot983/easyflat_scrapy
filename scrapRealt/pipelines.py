# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from types import NoneType
from itemadapter import ItemAdapter
from .models import db_connect, create_table, House, HousePhoto
from .items import ScrapyMainItem, ScrapyPhotoItem
from sqlalchemy.orm import sessionmaker 
from scrapy.exceptions import DropItem

from sqlalchemy.exc import IntegrityError

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


class SaveHousePipelines:
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.session = sessionmaker(bind=engine)
    
    def spider_closed(self, spider):
        self.session.close()



    def process_item(self, item, spider):
        session = self.session()
        house = House()
        house_photo = HousePhoto()
        #print(f"TESTTTTT {type(item)} | {type(item['url'])}")
        #print(item["url"])
        
        #print(exist_house)
        #print(f"TEST EXIST {type(exist_house)}")
        try:
            if isinstance(item, ScrapyMainItem):
                exist_house = session.query(House).filter_by(url = str(item['url'])).first()
                print("Instance House")
                if exist_house is None:
                    house = House(**item)
                    session.add(house)
                    session.commit()
                    print("add done")

            if isinstance(item, ScrapyPhotoItem):
                print("Instance HousePhoto")
                exist_house = session.query(House).filter_by(url = str(item['url'])).first()
                if exist_house is not None:
                    house_photo = HousePhoto()
                    house_photo.house_id = exist_house.id
                    house_photo.image = item['image']
                    session.add(house_photo)
                    session.commit()
                    
        except DropItem:
            print("Item was dropped")
            session.rollback()
        
        except IntegrityError:
            print("Item already exists")
            session.rollback()
        
        finally:
            session.close()
            print('session closed')

        return item
    
'''
class SaveItemPipelines:
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

        self.house_photo = HousePhoto
        
    
    def process_item(self, item, spider):
        session = self.Session()

        house_photo_db = self.house_photo
        
        house_photo_db.house_id: int = item['house_id']
        house_photo_db.image: str = item["image"]
        
        try:
            session.add(house_photo_db)
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()
            
            return item'''
        