# -*- coding: utf-8 -*-
import scrapy


class PostSpider(scrapy.Spider):
    name = 'post'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://fanyi.baidu.com/sug']
    #原始作用:将起始url列表中的url进行get请求的发送.
    #通过如下操作进行父类方法的重写,让其进行post请求的发送
    def start_requests(self):
        data = {
            'kw':'dog'
        }
        for url in self.start_urls:
            yield scrapy.FormRequest(url=url,callback=self.parse,formdata=data)
        
    def parse(self, response):
        print(response.text)
