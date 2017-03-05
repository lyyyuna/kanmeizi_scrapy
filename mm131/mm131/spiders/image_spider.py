import scrapy
from mm131.items import Mm131Item

class ImageSpider(scrapy.Spider):
    name = "mm131spider"

    def start_requests(self):
        for i in range(1,200):
            url = "http://m.mm131.com/more.php?page=" + str(i)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        urls = response.css("div.post-content.post-text a::attr(href)").extract()

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_imgurl)

    def parse_imgurl(self, response):
        total = response.css("span.rw::text").extract_first()[2:4]
        if total is not None:
            total = int(total)
        else:
            self.logger.info("The total of %s is None", response.url)
            return
        
        title = response.css("h2.mm-title::text").extract_first()
        if title is None:
            self.logger.info("The title of %s is None", response.url)
            return
        
        imgurl = response.css("div.post-content img::attr(src)").extract_first()
        if imgurl is None:
            self.logger.info("The imgurl of %s is None", response.url)
            return

        base_imgurl = imgurl[:-imgurl[::-1].index('/')]
        imgurls = []
        for i in range(1,total+1):
            imgurls.append(base_imgurl + str(i) + '.jpg')
        
        item = Mm131Item()
        item['file_urls'] = imgurls
        item['title'] = title
        return item
        
