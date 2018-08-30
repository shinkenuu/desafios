# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class RedditorItem(Item):
    subreddit = Field()
    upvotes = Field()
    title = Field()
    link_to_thread = Field()
    link_to_commentaries = Field()
