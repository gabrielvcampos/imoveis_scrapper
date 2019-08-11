# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImoveisCrawlerItem(scrapy.Item):
    url = scrapy.Field()
    preco = scrapy.Field()
    area = scrapy.Field()
    quartos = scrapy.Field()
    banheiros = scrapy.Field()
    vagas_garagem = scrapy.Field()
    condominio = scrapy.Field()
    iptu = scrapy.Field()
    endereco = scrapy.Field()
    imobiliaria = scrapy.Field()

