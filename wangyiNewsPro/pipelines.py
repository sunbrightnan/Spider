# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
class WangyinewsproPipeline(object):
    conn = None
    cursor = None

    def open_spider(self,spider):
        self.conn = pymysql.Connect(host='127.0.0.1',port=3306,user='root',password='',db='spider')
        print(self.conn)
        
    def process_item(self, item, spider):
        print(item)
        self.cursor = self.conn.cursor()
        sql = 'insert into news values("%s","%s","%s","%s","%s")'%(item['title'],item['content'],item['img_url'],item['keys'],item['kind'])
        print(sql)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        return item

    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()