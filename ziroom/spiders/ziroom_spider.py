import scrapy
import re
from scrapy.loader import ItemLoader
from ziroom.items import ZiroomItem
from datetime import datetime

class ZiroomSpider(scrapy.Spider):
    name = "ziroom"

    start_urls = [
        'http://sz.ziroom.com/z/nl/z2-r5-d23008674.html?p=1',
    ]

    def parse(self, response):
        # get all page links
        for herf in response.css('.txt > h3 > a::attr(href)').extract():
            url = 'http:' + herf
            yield response.follow(url, callback=self.parse_page)

        for href in response.css('.next::attr(href)'):
            yield response.follow(href, self.parse)


    def parse_page(self, response):
        href_data = response.css('#wechat > img::attr(src)').extract_first()
        href_num = re.search('room\/\d+', href_data).group()[5:]
        href = 'http://sz.ziroom.com/z/vr/'+href_num+'.html'
        # room_name
        room_name = response.css('.room_name>h2::text').extract_first().strip()
        # room_price
        room_price = response.css('#room_price::text').extract_first()[1:]
        # area
        area_data = response.css('.detail_room > li:nth-child(1)::text').extract_first()
        area = re.search('\d+.\d+|\d+', area_data).group()
        # orientation
        orientation_data = response.css('.detail_room > li:nth-child(2)::text').extract_first()
        orientation = orientation_data[-1]
        # house_style
        house_style = response.css('.detail_room > li:nth-child(3)::text').extract_first()[4:8]
        # floor
        floor = response.css('.detail_room > li:nth-child(4)::text').extract_first()[4:10]
        # traffic
        traffic_1 = response.css('.lineList::text').extract_first().strip()
        traffic_2 = response.css('.lineList > .box > p ::text').extract()
        # house_pic
        house_pic = response.css('.lof-navigator li:nth-last-child(1) img::attr(src)').extract_first()
        response.css('.fb::text')
        # around
        around = response.css('.aboutRoom p::text').extract_first()
        # traffic info
        traffic_info = response.css('.aboutRoom p::text').extract()[1]
        # roommate
        roommate = response.css('.greatRoommate > ul li::attr(class)').extract()
        # room_id
        room_id = response.css('.fb::text').extract()[1].strip()
        # district
        district = response.css('.node_infor a::text').extract()[1]
        # street
        street = response.css('.node_infor a::text').extract()[2]
        # building
        building = response.css('.node_infor a::text').extract()[3]

        loader = ItemLoader(item=ZiroomItem(), response=response)
        loader.add_value('href', href)
        loader.add_value('room_name', room_name)
        loader.add_value('room_price', room_price)
        loader.add_value('area', area)
        loader.add_value('orientation', orientation)
        loader.add_value('house_style', house_style)
        loader.add_value('floor', floor)
        loader.add_value('traffic', traffic_1)
        loader.add_value('traffic', traffic_2)
        loader.add_value('house_pic', house_pic)
        loader.add_value('room_id', room_id)
        loader.add_value('around', around)
        loader.add_value('traffic_info', traffic_info)
        loader.add_value('roommate', roommate)
        loader.add_value('updatetime', str(datetime.now()))
        loader.add_value('district', district)
        loader.add_value('street', street)
        loader.add_value('building', building)


        return loader.load_item()