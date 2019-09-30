# -*- coding: utf-8 -*-
import scrapy
from picPro.items import PicproItem

class PicSpider(scrapy.Spider):
    name = 'pic'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['http://pic.netbian.com/']

    def parse(self, response):
        li_list = response.xpath('//div[@class="slist"]/ul/li')
        for li in li_list:
            img_url = 'http://pic.netbian.com'+li.xpath('./a/span/img/@src').extract_first()
            img_name = img_url.split('/')[-1]
            item = PicproItem()
            item['name'] = img_name
            
            yield scrapy.Request(url=img_url,callback=self.getImgData,meta={'item':item})
            
    def getImgData(self,response):
        item = response.meta['item']
        item['img_data'] = response.body
        
        yield item