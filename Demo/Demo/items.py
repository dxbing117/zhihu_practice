# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    profile_head = scrapy.Field()
    achieve_zan = scrapy.Field()
    following_sum = scrapy.Field()
    follower_sum = scrapy.Field()
    url = scrapy.Field()
    # problem_url = scrapy.Field()
    # status = scrapy.Field()

