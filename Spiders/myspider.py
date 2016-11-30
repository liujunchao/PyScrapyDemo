import scrapy
import urllib2
import os
from scrapy.utils.response import open_in_browser

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['http://ts.hjenglish.com/']

    def parse(self, response):
       # open_in_browser(response)
        self.log('begin to debug response:%s' % response.url)
       # from scrapy.shell import inspect_response
       # inspect_response(response, self)

        for url in response.css("#VOATabDiv_2 li a::attr('href')").extract():
            print(url)
            yield scrapy.Request(response.urljoin(url), self.parse_titles)

    def parse_titles(self, response):
        print("handle %s " % response.url)
        all_p =  response.css("#ArticleCnt p")
        if len(all_p)>0:
            all_a = all_p[0].css("a::attr('href')")
            if len(all_a)>0:
                downpath =  all_a[0].extract()
                if downpath.endswith(".mp3"):
                    filename = os.path.basename(downpath)
                    f = urllib2.urlopen(downpath)
                    print("down file %s" % filename)
                    with open(filename, "wb") as code:
                        code.write(f.read())


