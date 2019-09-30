# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


from time import sleep

from scrapy.http import HtmlResponse

class WangyinewsproDownloaderMiddleware(object):
  

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        #指定拦截的响应
        if request.url in spider.news_urls:
            #处理响应对象:
            url = request.url
            bro = spider.bro #获取了在爬虫文件中创建好的浏览器对象
            bro.get(url=url)
            sleep(2)
            js = 'window.scrollTo(0,document.body.scrollHeight)'
            bro.execute_script(js)
            sleep(1)
            bro.execute_script(js)
            sleep(1)
            bro.execute_script(js)
            sleep(1)
           
            #我们需求中需要的数据源(携带了动态加载出来新闻数据的页面源码数据)
            page_text = bro.page_source
            
            #创建一个新的响应对象并且将上述获取的数据源加载到该响应对象中,然后响应对象返回
            return HtmlResponse(url=bro.current_url,body=page_text,encoding='utf-8',request=request)
            
        return response
