#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-05-14 21:43:16
# Project: get_proxy

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from pyspider.libs.base_handler import *
from time import sleep
import hashlib


ua = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"

start_urls = (
    "http://www.xicidaili.com/nn",
    "http://www.xicidaili.com/nt/"
)

test_urls = [
    "http://www.baidu.com",
]

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=10)
    def on_start(self):
        for url in start_urls:
            self.crawl(url, 
                   callback=self.index_page,
                   headers= {'User-Agent': ua},
                   )

    @config(age=1)
    def index_page(self, response):
        for each in response.doc('#ip_list tr').items():
            item = {}
            ip = each("td:nth-child(2)").text()
            if ip:
                item["ip"] = ip
                item["port"] = each("td:nth-child(3)").text()
                item["url"] = item["ip"] + ":" + item["port"]
                item["addr"]  = each("td:nth-child(4) a").text()
                item["secure"] = each("td:nth-child(5)").text()
                item["type"] = each("td:nth-child(6)").text()
                item["speed"] = str(each("td:nth-child(7) > div").attr("title")).replace("秒", "")
                item["connect_time"] = str(each("td:nth-child(8) > div").attr("title")).replace("秒", "")
                item["age"] = each("td:nth-child(9)").text()
                item["check_time"] = each("td:nth-child(10)").text()
                test_url = test_urls[0]
                save = {}
                save["data"] = item
                save["test_urls"] = test_urls[1:]
                proxy= item["ip"] + ":" + item["port"]
                self.crawl( test_urls[0] + "#" + hashlib.md5(proxy).hexdigest(),
                                 callback=self.test_page,
                                 headers= {'User-Agent': ua},
                                 proxy=proxy,
                                 save=save,
                                 age=0.01,
                                 timeout=10
                               )

    
    def test_page(self, response):
        title = response.doc("title").text()
        
        test_urls = response.save["test_urls"]
        item = response.save["data"]
        if len(test_urls) > 0:
            test_url = test_urls[0]
            test_urls = test_urls[1:]
            save = {}
            save["data"] = data
            save["test_urls"] = test_urls
            proxy= item["ip"] + ":" + item["port"]
            self.crawl( test_url + "#" + hashlib.md5(proxy).hexdigest() ,
                                 callback=self.test_page,
                                 headers= {'User-Agent': ua},
                                 proxy=proxy,
                                 save=save,
                                 age=0.01,
                                 timeout=10,
                               )
        else:
            return [item]
        
        
        
        
        
