# -*- coding: utf-8 -*-
import json
import random
import time

import scrapy

from Demo.items import ZhihuItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['zhihu.com']
    start_urls = ['http://zhihu.com/']

    user = 'tianshansoft'
    user_url ='https://www.zhihu.com/people/{user}/activities'

    follower_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={follower_query}&offset={offset}&limit={limit}'
    follower_query ='data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'

    followee_url ='https://www.zhihu.com/api/v4/members/{user}/followees?include={followee_query}&offset={offset}&limit={limit}'

    def start_requests(self):
        yield scrapy.Request(url=self.user_url.format(user=self.user), callback=self.parse_user)
        yield scrapy.Request(url=self.follower_url.format(user=self.user, follower_query=self.follower_query, offset=0,
                                                          limit=20), callback=self.parse_followers)
        yield scrapy.Request(url=self.followee_url.format(user=self.user, followee_query=self.follower_query, offset=0,
                                                          limit=20), callback=self.parse_followees)

    def parse_user(self, response):
        '''个人详情页解析方法,另外可以用re匹配知乎response.body中的</script><script id="js-initialData" type="text/json">相应字段
        (followerCount,followingCount,voteupCount)可以直接得到人数的int类型'''
        item = ZhihuItem()
        # print(type(response.status))
        # if response.status == 200:
        name = response.xpath('//div[@id="ProfileHeader"]//h1/span[1]/text()').extract_first()
        profile_head = " ".join(response.xpath("//div[@id='ProfileHeader']//div[@class='ProfileHeader-info']/div[1]/text()").extract())
        achieve_zan = " ".join(response.xpath("(//div[@class='IconGraf'])[1]/text()").extract())
        following_sum = response.xpath("(//strong[@class='NumberBoard-itemValue'])[1]/@title").extract_first()
        follower_sum = response.xpath("(//strong[@class='NumberBoard-itemValue'])[2]/@title").extract_first()
        item['name'] = name
        item['profile_head'] = profile_head
        item['achieve_zan'] = achieve_zan
        item['following_sum'] = following_sum
        item['follower_sum'] = follower_sum
        item['url'] = response.url
        # item['status'] = response.status
        # item['problem_url'] = None
        yield item
        # else:
        #     print('遇到问题,请调试', response.status, response.url)
        #     item['problem_url'] = (response.status, response.url)
        #     yield item


    def parse_followers(self, response):
        # item = ZhihuItem()
        # if response.status == 200:
        results = json.loads(response.text)
        if "data" in results.keys():
            for result in results.get('data'):
                yield scrapy.Request(url=self.user_url.format(user=result.get('url_token')), callback=self.parse_user)
                yield scrapy.Request(
                    url=self.follower_url.format(user=result.get('url_token'), follower_query=self.follower_query,
                                                 offset=0, limit=20), callback=self.parse_followers
                )
                yield scrapy.Request(
                    url=self.followee_url.format(user=result.get('url_token'), followee_query=self.follower_query,
                                                 offset=0, limit=20), callback=self.parse_followees
                )
        if "paging" in results.keys() and results.get('paging').get('is_end') == 'false':
            next_page = results.get('paging').get(next)
            time.sleep(random.uniform(0.1, 3))
            yield scrapy.Request(url=next_page, callback=self.parse_followers)
        # else:
        #     print('遇到问题,请调试', response.status, response.url)
        #     item['problem_url'] = (response.status, response.url)
        #     yield item


    def parse_followees(self, response):
        # item = ZhihuItem()
        # if response.status == 200:
        results = json.loads(response.text)
        if "data" in results.keys():
            for result in results.get('data'):
                yield scrapy.Request(url=self.user_url.format(user=result.get('url_token')), callback=self.parse_user)
                yield scrapy.Request(
                    url=self.follower_url.format(user=result.get('url_token'),follower_query=self.follower_query,
                                                 offset=0, limit=20), callback=self.parse_followers
                )
                yield scrapy.Request(
                    url=self.followee_url.format(user=result.get('url_token'), followee_query=self.follower_query,
                                                 offset=0, limit=20), callback=self.parse_followees
                )
        if "paging" in results.keys() and results.get('paging').get('is_end') == 'false':
            next_page = results.get('paging').get(next)
            yield scrapy.Request(url=next_page, callback=self.parse_followees)
        # else:
        #     print('遇到问题,请调试', response.status, response.url)
        #     item['problem_url'] = (response.status, response.url)
        #     yield item






