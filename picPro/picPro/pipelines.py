# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
class PicproPipeline(object):
    def open_spider(self,spider):
        if not os.path.exists('picLib'):
            os.mkdir('./picLib')
    def process_item(self, item, spider):
        imgPath = './picLib/'+item['name']
        with open(imgPath,'wb') as fp:
            fp.write(item['img_data'])
            print(imgPath+'下载成功!')
        return item
