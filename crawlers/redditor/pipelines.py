# -*- coding: utf-8 -*-
import json

from scrapy.exceptions import DropItem

from redditor.settings import MINIMUM_UPVOTES, OUTPUT_FILE

class RedditorPipeline(object):

    def open_spider(self, spider):
        self.file = open(OUTPUT_FILE, 'w')
        self.file.write("[")

    def close_spider(self, spider):
        self.file.write("]")
        self.file.close()

    def process_item(self, item, spider):
        if not self.has_enough_upvotes(item):
            raise DropItem('Not enough upvotes')

        if item['link_to_thread'].startswith('/r/'):
            item['link_to_thread'] = 'https://old.reddit.com' + item['link_to_thread']

        line = json.dumps(
            dict(item),
            sort_keys=True,
            indent=4,
            separators=(',', ': ')
        ) + ",\n"

        self.file.write(line)

        return item

    @staticmethod
    def has_enough_upvotes(item):
        return item['upvotes'] and int(item['upvotes']) >= MINIMUM_UPVOTES
