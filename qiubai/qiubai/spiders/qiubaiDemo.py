# -*- coding: utf-8 -*-
import scrapy


class QiubaidemoSpider(scrapy.Spider):
    name = 'qiubaiDemo'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://www.qiushibaike.com/text/']
    def parse(self, response):
        div_list = response.xpath('//div[@id="content-left"]/div')
        all_data = []
        #xpath返回的列表元素类型为Selector类型
        for div in div_list:
            # title = div.xpath('./div[1]/a[2]/h2/text() | ./div[1]/span[2]/h2/text()')[0].extract()
            title = div.xpath('./div[1]/a[2]/h2/text() | ./div[1]/span[2]/h2/text()').extract_first()
            content = div.xpath('./a[1]/div/span/text()').extract_first()
            
            dic = {
                'title':title,
                'content':content
            }
            
            all_data.append(dic)
    #基于终端指令的持久化存储:可以通过终端指令的形式将parse方法的返回值中存储的数据进行本地磁盘的持久化存储
        return all_data
    
        
