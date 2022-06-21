# -*- coding: utf-8 -*-
from scrapy.http import Request
from scrapy.spiders import CrawlSpider
from urlparse import urljoin
from dateutil.parser import parse
from datetime import datetime

from crawlers.items import DocumentItem


class ScrapeEpicos(CrawlSpider):
    name = 'epicos'
    start_urls = ['https://www.epicos.com/']

    def parse(self, response):
        categories_url_path = '//ul/li[contains(@class, "news")]/ul/li/a/@href'
        categories_hrefs = response.xpath(categories_url_path).extract()

        if not categories_hrefs:
            self.logger.error('Missing categories')

        for href in categories_hrefs:
            url = urljoin(response.url, href)
            yield Request(url, callback=self.parse_category)

    def parse_category(self, response):
        next_page_path = '//*[@class="pager-next"]/a/@href'
        items_url_path = '//div[@class="full-list"]//div[@class="views-field views-field-title"]/a/@href'
        documents_hrefs = response.xpath(items_url_path).extract()

        if not documents_hrefs:
            self.logger.error('Missing documents')

        for href in documents_hrefs:
            url = urljoin(response.url, href)
            yield Request(url, callback=self.parse_item)

        next_page_url = response.xpath(next_page_path).extract_first()

        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse_category)

    def parse_item(self, response):
        item = DocumentItem()
        title_path = '//*[@class="content-title"]/text()'
        date_path = '//*[@class="content-date"]/text()'
        text_path = '//*[@class="content-body justified-body"]//text()'
        images_path = '//*[@id="bwbodyimg"]/img/@src'
        youtube_path = '//*[@class="content-body justified-body"]//iframe/@src'

        item['url'] = response.request.url

        title = response.xpath(title_path).extract_first()

        if title:
            item['title'] = title.strip()
        else:
            item['title'] = ''
            self.logger.error('Missing title')

        date = response.xpath(date_path).extract_first()

        if date:
            item['date'] = parse(date)
        else:
            item['date'] = datetime.utcnow()
            self.logger.error('Missing date')

        text_blocks = response.xpath(text_path).extract()
        text_delimiter = self.settings.get('TEXT_DELIMITER')

        if text_blocks:
            item['text'] = text_delimiter.join([text_block.strip() for text_block in text_blocks])
        else:
            item['text'] = ''

        images = [urljoin(response.url, href) for href in response.xpath(images_path).extract()]
        item['image_urls'] = images
        youtube_urls = response.xpath(youtube_path).extract()
        item['youtube_urls'] = youtube_urls

        yield item
