# -*- coding: utf-8 -*-
import scrapy


class LoginSpider(scrapy.Spider):
    name = 'login'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['http://www.renren.com/ajaxLogin/login?1=1&uniqueTimestamp=201873958471']
    def start_requests(self):
        formdata = {
            'email': '17701256561',
            'icode': '',
            'origURL': 'http://www.renren.com/home',
            'domain': 'renren.com',
            'key_id': '1',
            'captcha_type': 'web_login',
            'password': '7b456e6c3eb6615b2e122a2942ef3845da1f91e3de075179079a3b84952508e4',
            'rkey': '44fd96c219c593f3c9612360c80310a3',
            'f': 'https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3Dm7m_NSUp5Ri_ZrK5eNIpn_dMs48UAcvT-N_kmysWgYW%26wd%3D%26eqid%3Dba95daf5000065ce000000035b120219',
        }
        for url in self.start_urls:
            yield scrapy.FormRequest(url=url,formdata=formdata,callback=self.parse)
            
    def parse(self, response):
        url = 'http://www.renren.com/960481378/profile'
        
        yield scrapy.Request(url=url,callback=self.personalPage)
        
    def personalPage(self,response):
        page_text = response.text
        print(response)
