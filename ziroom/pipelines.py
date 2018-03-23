# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from openpyxl import Workbook
from scrapy.exceptions import DropItem

class ExcelPipeline(object):

    def open_spider(self, spider):
        self.r = 2
        self.wb = Workbook()
        self.excelname = 'ziroom.xlsx'
        self.ws1 = self.wb.active
        self.ws1.title = "from1500to2000"
        info = ['资料更新时间', '区域', '街道', '小区', '房名', '户型', '朝向', '楼层', '面积', '月租(季付)', '室友', '地铁交通', '交通', '房间链接', '房间结构图', '周边', '编号']
        for i in range(1, len(info)+1):
            r = 1
            c = i
            v = info[i-1]
            self.ws1.cell(row=r, column=i, value=v)

    def close_spider(self, spider):
        self.wb.save(filename=self.excelname)

    def process_item(self, item, spider):
        if item is not None:
            data = dict(item)
            rr = str(self.r)
            self.ws1['A'+rr] = data['updatetime'][0]
            self.ws1['B' + rr] = data['district'][0]
            self.ws1['C' + rr] = data['street'][0]
            self.ws1['D' + rr] = data['building'][0]
            self.ws1['E'+rr] = data['room_name'][0]
            self.ws1['F'+rr] = data['house_style'][0]
            self.ws1['G'+rr] = data['orientation'][0]
            self.ws1['H'+rr] = data['floor'][0]
            self.ws1['I'+rr] = data['area'][0]
            self.ws1['J'+rr] = data['room_price'][0]
            self.ws1['K'+rr] = str(data['roommate'])
            self.ws1['L'+rr] = data['traffic'][0]
            self.ws1['M'+rr] = data['traffic_info'][0]
            self.ws1['N'+rr] = data['href'][0]
            self.ws1['O'+rr] = data['house_pic'][0]
            self.ws1['P'+rr] = data['around'][0]
            self.ws1['Q'+rr] = data['room_id'][0]
            self.r = self.r+1
            return item
        else:
            raise DropItem('Missing data in %s' % item)

class ZiroomPipeline(object):

    def open_spider(self, spider):
        self.file = open('items.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False)+ '\n'
        self.file.write(line)
        return item


