import scrapy
import urllib2
import os
from scrapy.utils.response import open_in_browser

class EnglishDownSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['http://www.tingclass.net/list-5544-1.html','http://www.tingclass.net/list-5544-2.html','http://www.tingclass.net/list-5544-3.html']

    def parse(self, response):
        self.log('begin to debug response:%s' % response.url)

        for url in response.css("#share_con ul li a::attr('href')").extract():
            #print(url)
            yield scrapy.Request(response.urljoin(url), self.parse_details)

    def parse_details(self, response):
        #print("handle %s " % response.url)

        url =  response.css("#jplayer_tc_yinpin ::attr('href')")[0].extract()
        #print("handle %s " % url)
        yield scrapy.Request(response.urljoin(url), self.down_file)
        return

    def down_file(self,response):
         print("handle %s " % response.url)
         downpath = response.css("div.download a ::attr('href')")[0].extract()
         if downpath.endswith(".mp3"):
                    filename = os.path.basename(downpath)
                    f = urllib2.urlopen(downpath)
                    print("down file %s" % filename)
                    with open(filename, "wb") as code:
                        code.write(f.read())
         return ;



