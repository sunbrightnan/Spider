# -*- coding: utf-8 -*-
import scrapy

from choutiPro.items import ChoutiproItem
class ChoutiSpider(scrapy.Spider):
    name = 'chouti'
    # allowed_domains = ['www.xxx.com']
    #通用url的封装
    url = 'https://dig.chouti.com/r/scoff/hot/%d'
    pageNum = 1
    
    start_urls = ['https://dig.chouti.com/r/scoff/hot/1']

    def parse(self, response):
        div_list = response.xpath('//div[@id="content-list"]/div')
        for div in div_list:
            head = div.xpath('./div[3]/div[1]/a/text()').extract_first()
            author = div.xpath('./div[3]/div[2]/a[4]/b/text()').extract_first()

            item = ChoutiproItem()
            item['head'] = head
            item['author'] = author
            
            yield item
        
        if self.pageNum < 5: #页码的一个范围
            #封装集成了一个新的页码的url
            self.pageNum += 1
            new_url = format(self.url%self.pageNum)
            #手动的请求发送:callback表示的指定的解析方法
            yield scrapy.Request(url=new_url,callback=self.parse)
            
            #在scrapy框架中yield的使用场景:
            #1.yield item:向管道提交item
            #2.yield scrapy.Request():进行手动请求发送
            
       
        