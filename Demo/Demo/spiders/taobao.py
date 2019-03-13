# -*- coding: utf-8 -*-
import scrapy
import js2py
import selenium


class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['taobao.com']
    start_urls = ['http://taobao.com/']

    def parse(self, response):
        pass
