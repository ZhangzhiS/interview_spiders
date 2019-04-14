#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
# @Author   : zhi
# @Time     : 2019/4/14 下午2:18
# @Filename : spider_xueqiu
# @Software : PyCharm
import scrapy
import json
from jd.items import StockItem


class ExampleSpider(scrapy.Spider):
    name = 'xueqiu'
    allowed_domains = ['xueqiu.com']

    def start_requests(self):
        url = 'https://xueqiu.com/service/v5/stock/screener/quote/list?page={page}&size=30&order=desc&orderby=percent&order_by=percent&market=US&type=us&_=1555222821845'
        for i in range(1,5):
            temp_url = url.format(page=str(i))
            yield scrapy.Request(
                url=temp_url,
                callback=self.parse
            )

    def parse(self, response):
        data = response.body.decode()
        data = json.loads(data)
        data_list = data["data"]["list"]
        for d in data_list:
            item = StockItem()
            item["name"] = d["name"]
            item["symbol"] = d["symbol"]
            item["current"] = d["current"]
            item["percent"] = d["percent"]
            item["market_capital"] = d["market_capital"]
            item["pe_ttm"] = d["pe_ttm"]
            yield item


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute("scrapy crawl xueqiu -o xueqiu.csv".split())
