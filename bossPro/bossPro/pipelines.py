# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#注意:只要涉及到持久化存储的相关的操作,必须要写在管道文件中
#管道文件:需要接受爬虫文件提交过来的数据,并对数据进行持久化存储.(IO操作)
import pymysql
from redis import Redis
class BossproPipeline(object):
    fp = None
    #只会被执行一次(开始爬虫的时候执行一次)
    def open_spider(self,spider):
        print('开始爬虫!!!')
        self.fp = open('./job.txt','w',encoding='utf-8')
    #爬虫文件没提交一次item,该方法会被调用一次
    def process_item(self, item, spider):
        self.fp.write(item['title']+"\t"+item['salary']+'\t'+item['company']+'\n')
        return item
    def close_spider(self,spider):
        print('爬虫结束!!!')
        self.fp.close()
#注意:默认情况下,管道机制并没有开启.需要手动在配置文件中进行开启

#使用管道进行持久化存储的流程:
#1.获取解析到的数据值
#2.将解析的数据值存储到item对象(item类中进行相关属性的声明)
#3.通过yild关键字将item提交到管道
#4.管道文件中进行持久化存储代码的编写(process_item)
#5.在配置文件中开启管道

class mysqlPipeLine(object):
    conn = None
    cursor = None
    def open_spider(self,spider):
        self.conn = pymysql.Connect(host='127.0.0.1', port=3306, user='root', password='', db='spider')
        print(self.conn)
        
    def process_item(self, item, spider):
        self.cursor = self.conn.cursor()
        sql = 'insert into boss values("%s","%s","%s")'%(item['title'],item['salary'],item['company'])
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
        
class RedisPipeLine(object):
    conn = None
    def process_item(self, item, spider):
        dic = {
            'title':item['title'],
            'salary':item['salary'],
            'company':item['company']
        }
        self.conn.lpush('jobInfo',dic)
        return item
    def open_spider(self, spider):
        self.conn = Redis(host='127.0.0.1',port=6380)
        print(self.conn)
#[注意]一定要保证每一个管道类的process_item方法要有返回值