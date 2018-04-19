# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy import Request
from pprint import pprint


class MoviesSpider(scrapy.Spider):
    BASE_URL = 'https://movie.douban.com/j/search_subjects?type=movie&tag={tag}&sort=recommend&page_limit={limit}&page_start={start}'
    MOVIE_TAG = '豆瓣高分'
    PAGE_LIMIT = 20
    page_start = 0

    name = 'movies'
    allowed_domains = ['movie.douban.com']
    start_urls = [BASE_URL.format(tag=MOVIE_TAG, limit=PAGE_LIMIT, start=page_start)]

    def parse(self, response):
        infos = json.loads(response.body.decode('utf-8'))

        for movie_info in infos['subjects']:
            movie_item = {}
            movie_item['片名'] = movie_info['title']
            movie_item['评分'] = movie_info['rate']

            yield Request(movie_info['url'], callback=self.parse_movie,
                          meta={'_movie_item': movie_item})

        if len(infos['subjects']) == self.PAGE_LIMIT:
            self.page_start += self.PAGE_LIMIT
            url = self.BASE_URL.format(tag=self.MOVIE_TAG, limit=self.PAGE_LIMIT, start=self.page_start)
            yield Request(url)

    def parse_movie(self, response):
        movie_item = response.meta['_movie_item']

        # 获取整个信息字符串
        info = response.css('div#info').xpath('string(.)').extract_first()

        # 提取所有字段名
        fields = [s.strip().replace(':', '') for s in response.css('div#info span.pl::text').extract()]

        # 提取所有字段的值
        values = [re.sub('\s+', '', s.strip()) for s in re.split('\s*(?:%s):\s*' % '|'.join(fields), info)][1:]

        movie_item.update(dict(zip(fields, values)))

        yield movie_item