# -*- coding: utf-8 -*-
from scrapy import Spider, Request

from redditor.items import RedditorItem


class PopstarsSpider(Spider):
    """
    Scrap popular threads of a subreddit.
    """
    name = 'popstars'

    def __init__(self, *args, **kwargs):
        """
        Initialize PopstarsSpider.

        Set via crawler.process(popstars_spider, subreddits=['redit1', ...])
        or set self.subreddits via -a subreddit=SUBREDDITS in CLI, separating elements with ','
        """

        super().__init__(*args, **kwargs)

        if isinstance(self.subreddits, str):
            self.subreddits = self.subreddits.split(',')

        elif not isinstance(self.subreddits, list):
            raise ValueError('No specified subreddits to crawl')

    def start_requests(self):

        for subreddit in self.subreddits:
            subreddit_url = 'https://old.reddit.com/r/{subreddit}/'.format(subreddit=subreddit)
            yield Request(url=subreddit_url, callback=self.parse_subreddit_page)

    def parse_subreddit_page(self, response):
        """
        Look for elegible threads within subreddit response, creating their `Items`

        :param response: response from a subrredit page
        """
        def extract_subreddit_name_from_url():
            # subreddit set in self.subreddit within start_requests() doesnt work, needs to get from URL
            return response.url.split('/')[-2]

        threads = response.xpath('//div[starts-with(@id, "thing_t3_")]')

        for thread in threads:
            thread_item = RedditorItem(subreddit=extract_subreddit_name_from_url())
            thread_item['upvotes'] = thread.xpath('.//div[@class="score likes"]/@title').extract_first()
            thread_item['title'] = thread.xpath('.//p[@class="title"]/a/text()').extract_first()
            thread_item['link_to_thread'] = thread.xpath('.//p[@class="title"]/a/@href').extract_first()
            thread_item['link_to_commentaries'] = thread.xpath(
                './/ul[@class="flat-list buttons"]/li[@class="first"]/a/@href').extract_first()

            yield thread_item
