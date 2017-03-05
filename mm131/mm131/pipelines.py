# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem
import scrapy
import os
import shutil
# from scrapy.http import Request

class Mm131Pipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        for file_url in item['file_urls']:
            yield scrapy.Request(file_url)

    def item_completed(self, results, item, info):
        file_paths = [x['path'] for ok, x in results if ok]
        if not file_paths:
            raise DropItem("Item contains no files")
        # item['file_paths'] = file_paths
        title = item['title']
        newpath = 'img/' + title
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        for path in file_paths:
            try:
                shutil.move('files/' + path, newpath)
            except:
                pass
        #self.logger.info("download finished for %s", title)
        return item