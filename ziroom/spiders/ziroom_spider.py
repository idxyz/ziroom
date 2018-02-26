import scrapy
import re
from scrapy.loader import ItemLoader
from ziroom.items import ZiroomItem
from datetime import datetime

class ZiroomSpider(scrapy.Spider):
    name = "ziroom"

    start_urls = [
        'http://sz.ziroom.com/z/nl/z2-r2-d23008674.html?p=1',
    ]

    def parse(self, response):
        # get links
        for herf in response.css('.txt > h3 > a::attr(href)').extract():
            url = 'http:' + herf
            yield response.follow(url, callback=self.parse_page)

        # get pagination
        current_page = 1
        #get_page = response.css('#page > span:nth-child(7)::text').extract_first()
        #last_page = int(re.search('\d+', get_page).group())
        if current_page < 2:
            next_page = 'http://sz.ziroom.com/z/nl/z2-r2-d23008674.html?p=' + str(current_page + 1)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_page(self, response):
        # def extract_with_css(query):
        #     return response.css(query).extract()[1]
        #
        # def extract_with_css2(query):
        #     return response.css(query).extract_first().strip()
        #
        # yield {
        #     'id': extract_with_css('.fb::text'),
        #     'name': extract_with_css2('.room_name>h2::text')
        # }

        #http: // sz.ziroom.com / z / vr / 60939857.html
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

        return loader.load_item()