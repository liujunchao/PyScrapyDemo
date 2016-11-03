from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

import os
from datetime import datetime, timedelta

def trimString(val):
    return val.lstrip('\r\n ').rstrip('\r\n ')
def trimVal(val):
    return trimString(val).lstrip('\n').rstrip('\n').replace("\n"," ");
pages=[]
now = datetime.now()
now = now + timedelta(30)
i = 0
future = now
searchTotal = 140
contentList=[]
while searchTotal>i:
    future = future + timedelta(1)
    url = "https://booking.airasia.com/Flight/Select?o1=CAN&d1=BKI&culture=zh-CN&dd1="+ future.strftime("%Y-%m-%d") +"&ADT=1&CHD=0&inl=0&s=true&mon=true&cc=CNY&c=false"
    #html = urlopen(url)
    session = requests.Session()
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
    req = session.get(url, headers=headers)
    bsObj = BeautifulSoup(req.text,"html.parser")
    rows = bsObj.findAll("tr", {"class": "fare-light-row"})
    for row in rows:
        rowOfFareLight = row.findAll("tr",{"class","fare-light-row"})
        startHour = ""
        endHour = ""
        price = ""
        if len(rowOfFareLight)>0:
            startHour = row.findAll("td",{"class":"avail-table-detail"})[0].getText()
            endHour = row.findAll("td",{"class":"avail-table-detail"})[1].getText()
            price = row.findAll("div",{"class":"avail-fare-price"})[0].getText()
            msg = trimVal(startHour)+"   "+trimVal(endHour)+" "+trimVal(price)+" "+future.strftime("%Y-%m-%d")+"    "+url+"   \n"
            contentList.append(msg)
            print(msg)
    i = i + 1
    print("loop count "+str(i))

with open("yabi_depart.txt", "w+") as code:
    for content in contentList:
        code.write(content)