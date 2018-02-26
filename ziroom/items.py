# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZiroomItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    href = scrapy.Field()
    room_name = scrapy.Field()
    room_price = scrapy.Field()
    area = scrapy.Field()
    orientation = scrapy.Field()
    house_style = scrapy.Field()
    floor = scrapy.Field()
    traffic = scrapy.Field()
    house_pic = scrapy.Field()
    room_id = scrapy.Field()
    around = scrapy.Field()
    traffic_info = scrapy.Field()
    roommate = scrapy.Field()
    updatetime = scrapy.Field()


    


