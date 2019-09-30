# -*- coding: utf-8 -*-
import scrapy
from bossPro.items import BossproItem
from redis import Redis

#爬虫文件的作用:
#1.url的指定
#2.请求的发送
#3.进行数据解析
#4.对item进行管道的提交
class BossSpider(scrapy.Spider):
    name = 'boss'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://www.zhipin.com/job_detail/?query=python%E7%88%AC%E8%99%AB&scity=101010100&industry=&position=']

    def parse(self, response):
        li_list = response.xpath('//div[@class="job-list"]/ul/li')

        for li in li_list:
            title = li.xpath('.//div[@class="info-primary"]/h3[@class="name"]/a/div/text()').extract_first()
            salary = li.xpath('.//div[@class="info-primary"]/h3[@class="name"]/a/span/text()').extract_first()
            company = li.xpath('.//div[@class="company-text"]/h3/a/text()').extract_first()
            
            #实例化一个item类型的对象
            item = BossproItem()
            #将解析到的数据值存储到item对象中:why?
            item['title'] = title
            item['salary'] = salary
            item['company'] = company
            
            #将item对象提交给管道进行持久化存储
            yield item
            
        