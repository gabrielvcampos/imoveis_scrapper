# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import pdb

class ZapimoveisSpider(CrawlSpider):
    name = 'zapimoveis'
    allowed_domains = ['www.zapimoveis.com.br']
    start_urls = ['https://www.zapimoveis.com.br/venda/imoveis/']
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"

    rules = (
        Rule(LinkExtractor(allow="/imovel/venda")),
        Rule(LinkExtractor(allow="/"), callback="parse_zap")
    )

    def parse_zap(self, response):
        pdb.set_trace()
        print("IMOVEL")
