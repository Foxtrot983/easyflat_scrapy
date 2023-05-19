from sqlalchemy import (
    Boolean, Column, ForeignKey, Integer, String, DateTime, 
    SmallInteger, create_engine, Column, ForeignKey, Text
    )
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
#from scrapy.utils.project import get_project_settings

import time

Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine('postgresql://lisatrot:11111111@localhost/fapi')


def create_table(engine):
    Base.metadata.create_all(engine)


class Marketplace(Base):
    __tablename__ = "marketplace"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="unknown")
    house = relationship("House", back_populates="marketplace")
#Добавить телефон в модель дома
class House(Base):
    __tablename__ = "house"

    id = Column(Integer, primary_key=True, index=True)
    amountUSD = Column('amountUSD', SmallInteger, default=0, nullable=True)
    amountBYN = Column('amountBYN', SmallInteger, default=0, nullable=True)
    rent_rooms = Column('rent_rooms', SmallInteger, default=0) #zero means that you'll rent only one room in flat with few rooms
    address = Column('address', String(35), default="Minsk")
    url = Column('url', String(50), default='example.com')
    created_at = Column('created_at', DateTime, default=func.now())
    agency = Column('agency', Boolean, default=True)
    description = Column('description', String, nullable=True)
    marketplace_id: Mapped[int] = Column(ForeignKey("marketplace.id"))
    marketplace: Mapped["Marketplace"] = relationship("Marketplace",back_populates="house")
    photo: Mapped[list["HousePhoto"]] = relationship("HousePhoto", back_populates="house")
    location_a = Column('location_a', String, nullable=True)
    location_b = Column('location_b', String, nullable=True)
    phoneNumber = Column("phoneNumber", String, nullable=True)
    #title = Column('title', String(50))




class HousePhoto(Base):
    __tablename__ = "house_photo"
    
    id = Column(Integer, primary_key=True, index=True)

    image = Column(String, nullable=True, unique=True)

    house_id: Mapped[int] = mapped_column(ForeignKey("house.id"))
    house: Mapped["House"] = relationship("House", back_populates="photo")
