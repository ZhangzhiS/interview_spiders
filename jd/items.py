# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    merchant_name = scrapy.Field()
    price = scrapy.Field()
    commodity_id = scrapy.Field()
    comment_count = scrapy.Field()


class StockItem(scrapy.Item):
    # 股票代码，股票名称，当前价，涨跌幅，市值，市盈率
    symbol = scrapy.Field()  # 股票代码
    name = scrapy.Field()  # 股票名称
    current = scrapy.Field()  # 当前价
    percent = scrapy.Field()  # 涨跌幅
    market_capital = scrapy.Field()  # 市值
    pe_ttm = scrapy.Field()  # 市盈率
