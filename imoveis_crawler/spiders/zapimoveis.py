# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

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
        id_imovel = response.xpath('//*[@id="article-container"]/section[4]/span[2]/text()').extract_first()
        url = response.request.url
        area = response.xpath("/html/body/div[1]/main/div/div/article/div/section[1]/ul/li[1]/b/text()").extract_first()
        banheiros = response.xpath("/html/body/div[1]/main/div/div/article/div/section[1]/ul/li[3]/b/text()").extract_first()
        preco = response.xpath("/html/body/div[1]/main/div/div/aside/div/div[1]/div/div[1]/div[2]/span/text()").extract_first()
        quartos = response.xpath("/html/body/div[1]/main/div/div/article/div/section[1]/ul/li[5]/b/text()").extract_first()
        vagas_garagem = response.xpath("/html/body/div[1]/main/div/div/article/div/section[1]/ul/li[4]/b/text()").extract_first()
        condominio = response.xpath("/html/body/div[1]/main/div/div/aside/div/div[1]/div/div[4]/span/text()").extract_first()
        iptu = response.xpath("/html/body/div[1]/main/div/div/aside/div/div[1]/div/div[5]/span/text()").extract_first()
        endereco = self.get_endereco(response)
        imobiliaria = self.get_imobiliaria(response) 
                             
        yield {
            'id_imovel': id_imovel,
            'url': url,
            'area': area,
            'banheiros': banheiros,
            'preco': preco,
            'quartos': quartos,
            'vagas_garagem': vagas_garagem,
            'condominio': condominio,
            'iptu': iptu,
            'endereco': endereco,
            'imobiliaria': imobiliaria,
            'plataforma': 'zapimoveis'
        }
