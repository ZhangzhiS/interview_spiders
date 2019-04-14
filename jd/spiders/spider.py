#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
# @Author   : zhi
# @Time     : 2019/4/14 下午12:23
# @Filename : spider
# @Software : PyCharm
# -*- coding: utf-8 -*-
import scrapy

from jd.items import JdItem


class ExampleSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']
    start_urls = ["https://search.jd.com/Search?keyword=%E8%BF%9B%E5%8F%A3%E7%89%9B%E5%A5%B6&enc=utf-8&wq=%E8%BF%9B%E5%8F%A3%E7%89%9B%E5%A5%B6&pvid=888ba44cc3874afe9dd1d13e054b76b2"]

    def parse(self, response):
        commodity_items = response.css("li.gl-item")
        print(len(commodity_items))
        for item in commodity_items:
            commodity_id = item.xpath("@data-sku").extract()[0]
            commodity_url = "https://item.jd.com/{commodity_id}.html".format(commodity_id=commodity_id)
            price = item.xpath('div/div[3]/strong/i/text()').extract()[0]
            # price = item.xpath('div/div[7]/span/a/text()').extract()[0]
            # print(price)
            yield scrapy.Request(
                url=commodity_url,
                callback=self.get_commodity_info,
                meta={
                    "price": price,
                    "commodity_id": commodity_id
                }
            )

    def get_commodity_info(self, response):
        # title = response.xpath("/html/body/div[8]/div/div[2]/div[1]/text()")
        commodity_item = response.css("div.itemInfo-wrap")
        title = commodity_item.xpath("div[1]/text()").extract()
        # 商品名称
        title = "".join(title).replace(" ", '').replace("\n", '')
        # 店铺名称
        merchant_name = response.xpath('//*[@id="crumb-wrap"]/div/div[2]/div[2]/div[1]/div/a/text()').extract()[0]
        # 价格
        price = response.meta["price"]
        commodity_id = response.meta["commodity_id"]

        meta = {
            "title": title,
            "merchant_name": merchant_name,
            "price": price,
            "commodity_id": commodity_id
        }
        url = "https://club.jd.com/comment/productCommentSummaries.action?referenceIds={commodity_id}".format(commodity_id=commodity_id)
        yield scrapy.Request(
            url=url,
            meta=meta,
            callback=self.parse_detail
        )

    def parse_detail(self, response):
        json_data = response.body.decode("GBK")
        print(json_data)
        item = JdItem()
        meta = response.meta
        item["title"] = meta["title"]
        item["merchant_name"] = meta["merchant_name"]
        item["price"] = meta["price"]
        item["commodity_id"] = meta["commodity_id"]
        item["comment_count"] = json_data
        yield item



if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute("scrapy crawl jd -o data.csv".split())
