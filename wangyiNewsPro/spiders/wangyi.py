# -*- coding: utf-8 -*-
import scrapy
from aip import AipNlp
'''
    使用流程:
        1.在爬虫文件中实例化一个浏览器对象
        2.重写爬虫类父类一方法closed,在刚方法中关闭浏览器对象
        3.在下载中间件中process_response中:
            a:获取爬虫文件中实例化好的浏览器对象
            b:执行浏览器自动化的行为动作
            c:实例化了一个新的响应对象,并且将浏览器获取的页面源码数据加载到了该对象中
            d:返回这个新的响应对象
'''
from selenium import webdriver
from wangyiNewsPro.items import WangyinewsproItem
class WangyiSpider(scrapy.Spider):
    
    #百度AI
    APP_ID = '14790912'
    API_KEY = 'db9r8XomfKdhuWphvzWeWGCV'
    SECRET_KEY = 'gpROMOFW6v26WHzhYk2s7TuE2oYs1Il8'

    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
    
    name = 'wangyi'
    # allowed_domains = ['www.xx.com']
    start_urls = ['https://news.163.com/']
    news_urls = [] #存储四个板块的url
    def __init__(self):
        #实例化一个浏览器对象
        self.bro = webdriver.Chrome(executable_path=r'C:\Users\Administrator\Desktop\爬虫+数据\day04\chromedriver.exe')
    def closed(self,spider):
        self.bro.quit()
    def parse(self, response):
        #获取指定板块的连接(国内,国际,军事,航空)
        li_list = response.xpath('//div[@class="ns_area list"]/ul/li')
        indexs = [3,4,6,7]
        new_li_list = [] #四大板块
        for index in indexs:
            new_li_list.append(li_list[index])
            
        #将四大板块对应的li标签进行解析(详情页的超链接)
        for li in new_li_list:
            #四个板块对应的url
            new_url= li.xpath('./a/@href').extract_first()
            self.news_urls.append(new_url)
            yield scrapy.Request(url=new_url,callback=self.parseNews)
    def parseNews(self,response):
        div_list = response.xpath('//div[@class="ndi_main"]/div')
        for div in div_list:
            item = WangyinewsproItem()
            item['title'] = div.xpath('./a/img/@alt').extract_first()
            item['img_url'] = div.xpath('./a/img/@src').extract_first()
            detail_url = div.xpath('./a/@href').extract_first()
            
            yield scrapy.Request(url=detail_url,callback=self.parseDetail,meta={'item':item})
            
    def parseDetail(self,response):
        item = response.meta['item']
        content = response.xpath('//div[@id="endText"]//text()').extract()
        item['content'] = ''.join(content).strip(' \n\t')
        #调用百度AI接口,提取文章的类型和关键字
        keys = self.client.keyword(item['title'].replace(u'\xa0',u''),item['content'].replace(u'\xa0',u''))
        key_list = []
        for dic in keys['items']:
            key_list.append(dic['tag'])
        item['keys'] =  ''.join(key_list)
        kinds = self.client.topic(item['title'].replace(u'\xa0',u''),item['content'].replace(u'\xa0',u''))
        item['kind'] = kinds['item']['lv1_tag_list'][0]['tag']
        
        yield item
        
