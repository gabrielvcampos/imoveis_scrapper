import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from imoveis_crawler.items import ImoveisCrawlerItem


class ImovelwebSpider(CrawlSpider):
    name = "imovelweb"
    allowed_domains = ["www.imovelweb.com.br"] 
    start_urls = ['https://www.imovelweb.com.br/apartamentos-venda-sao-paulo-sp.html']
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
    rules = [Rule(LinkExtractor(allow="/propriedades/" ) , callback="parse_webimoveis")]

    def parse_webimoveis(self, response):
        property_data = ImoveisCrawlerItem()
        property_data['url'] = response.request.url
        property_data['area'] = response.xpath("/html/body/div[1]/main/div/div/article/div/section[1]/ul/li[1]/b/text()").extract_first()
        property_data['banheiros'] = response.xpath("/html/body/div[1]/main/div/div/article/div/section[1]/ul/li[3]/b/text()").extract_first()
        property_data['preco'] = response.xpath("/html/body/div[1]/main/div/div/aside/div/div[1]/div/div[1]/div[2]/span/text()").extract_first()
        property_data['quartos'] = response.xpath("/html/body/div[1]/main/div/div/article/div/section[1]/ul/li[5]/b/text()").extract_first()
        property_data['vagas_garagem'] = response.xpath("/html/body/div[1]/main/div/div/article/div/section[1]/ul/li[4]/b/text()").extract_first()
        property_data['condominio'] = response.xpath("/html/body/div[1]/main/div/div/aside/div/div[1]/div/div[4]/span/text()").extract_first()
        property_data['iptu'] = response.xpath("/html/body/div[1]/main/div/div/aside/div/div[1]/div/div[5]/span/text()").extract_first()
        property_data['endereco'] = self.get_endereco(response)
        property_data['imobiliaria'] = self.get_imobiliaria(response)                      
        return property_data
    
    def get_imobiliaria(self , response):
        return response.css("html body#PROPERTY div#modal-hide-elements main div.layout-container div#main-container article.clearfix div#article-container section.general-section.article-section.publisher-section div.content-column div.column-left a h3.publisher-subtitle b::text").get()
    
    def get_endereco(self , response):
        all_elements = response.css("html body#PROPERTY div#modal-hide-elements main div.layout-container div#main-container article.clearfix div#article-container section.general-section.section-map-container div.section-location::text").getall()
        unformatted_location= " ".join(all_elements)
        formatted_location = unformatted_location.strip(' \t\n')
        return formatted_location