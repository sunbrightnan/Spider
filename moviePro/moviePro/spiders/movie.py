# -*- coding: utf-8 -*-
import scrapy

from moviePro.items import MovieproItem
class MovieSpider(scrapy.Spider):
    name = 'movie'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['http://www.55xia.com/']

    def parse(self, response):
        div_list = response.xpath('//div[@class="col-xs-1-5 movie-item"]')
        for div in div_list:
            item = MovieproItem()
            item['name'] = div.xpath('.//div[@class="meta"]/h1/a/text()').extract_first()
            item['score'] = div.xpath('.//div[@class="meta"]/h1/em/text()').extract_first()
            if item['score'] == None:
                item['score'] = '0'
            detail_url = 'https:'+div.xpath('.//div[@class="meta"]/h1/a/@href').extract_first()
            
            #对详情页的url发请求
            #使用meta参数实现请求传参
            yield scrapy.Request(url=detail_url,callback=self.getDetailPage,meta={'item':item})
    
    def getDetailPage(self,response):
        item = response.meta['item']
        deactor = response.xpath('/html/body/div[1]/div/div/div[1]/div[1]/div[2]/table/tbody/tr[1]/td[2]/a/text()').extract_first()
        desc = response.xpath('/html/body/div[1]/div/div/div[1]/div[2]/div[2]/p/text()').extract_first()
        item['desc'] = desc
        item['deactor'] =deactor
        
        yield item
        
        
        #总结:当使用scrapy进行数据爬取的时候,如果发现爬取的数据值没有在同一张页面中进行存储.则必须使用请求传参进行处理(持久化)
        
            
