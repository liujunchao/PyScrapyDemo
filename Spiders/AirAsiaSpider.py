import scrapy
import urllib2
import os
from datetime import datetime, timedelta

from scrapy.utils.response import open_in_browser

class AirAsiaSpider(scrapy.Spider):
    name = 'AirAsiaSpider'

    start_urls =[]

    contentList=[]

    searchCount = 0
    searchTotal = 140


    def start_requests(self):
        pages=[]
        now = datetime.now()
        now = now + timedelta(30)
        i = 0
        future = now
        while self.searchTotal>i:
            future = future + timedelta(1)
            url = "https://booking.airasia.com/Flight/Select?o1=CAN&d1=BKI&culture=zh-CN&dd1="+ future.strftime("%Y-%m-%d") +"&ADT=1&CHD=0&inl=0&s=true&mon=true&cc=CNY&c=false"
            pages.append(url);
            i = i + 1
            yield self.make_requests_from_url(url)

        #return pages

    def parse(self, response):
        self.log('begin to debug response:%s' % response.url)

        container = response.css(".js_availability_container")
        loopCnt = 0
        for itm in container.xpath("//table[@class='table avail-table']//tr[@class='fare-light-row']"):
            loopCnt = loopCnt +1
            #print(loopCnt)
            if len(itm.css(".avail-fare-price::text")) > 0:
                infoRow = itm.css("td.avail-stops-info").css("#icon_0_0").css("table").css("tr")
                if len(infoRow)>1:
                    time = infoRow[2].css("td")[2].css("div.text-center::text").extract()[0]
                    price = itm.css(".avail-fare-price::text")[0].extract().lstrip('\r\n ').rstrip('\r\n ')
                    print("time: "+time+" price:" + price + " related url :"+response.url)
                    self.contentList.append(time+"  " + price + "  "+response.url)
                    self.contentList.append("\n")

        self.searchCount = self.searchCount+1
        if self.searchCount == self.searchTotal:
            with open("yabi_depart.txt", "w+") as code:
                for content in self.contentList:
                    code.write(content)







