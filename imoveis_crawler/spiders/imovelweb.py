import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from imoveis_crawler.items import ImoveisCrawlerItem


class ImovelwebSpider(CrawlSpider):
    name = "imovelweb"
    allowed_domains = ["www.imovelweb.com.br"] 
    start_urls = ['https://www.imovelweb.com.br/apartamentos-venda.html']
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
    rules = (
        Rule(LinkExtractor(allow="/apartamentos-venda")),
        Rule(LinkExtractor(allow="/propriedades/" ) , callback="parse_webimoveis")
    )

    def parse_webimoveis(self, response):
        eh_lancamento = response.xpath('//*[@id="sidebar-status-development"]/div/h3/b/text()').extract_first() != None
        if eh_lancamento:
            id_imovel = response.xpath("//div[contains(@class,'general-section') and contains(@class, 'publisher-section')]/span[@class='publisher-code'][2]/text()").extract_first()
            url = response.request.url
            area = response.xpath('//*[@id="sidebar-status-development"]/div/div[2]/div[1]/div[2]/span[2]/b/text()').extract_first()[:3].replace('m','')
            banheiros = response.xpath("/html/body/div[1]/main/div/div/article/div/section[1]/ul/li[3]/b/text()").extract_first()
            preco = response.xpath('//*[@id="sidebar-status-development"]/div/div[3]/div/div/span[2]/b/text()').extract_first()[3:]
            quartos = response.xpath('//*[@id="sidebar-status-development"]/div/div[2]/div[2]/div[1]/span[2]/b/text()').extract_first()[:1]
            vagas_garagem = response.xpath('//*[@id="sidebar-status-development"]/div/div[2]/div[2]/div[3]/span[2]/b/text()').extract_first()[:1]
            condominio = response.xpath("/html/body/div[1]/main/div/div/aside/div/div[1]/div/div[4]/span/text()").extract_first()
            iptu = response.xpath("/html/body/div[1]/main/div/div/aside/div/div[1]/div/div[5]/span/text()").extract_first()
            endereco = response.xpath('//*[@id="development-head-container"]/div[2]/div[1]/div[2]/h2[2]/text()').extract_first()
            imobiliaria = response.xpath('//*[@id="article-container"]/section[7]/div/div[1]/a/h3/b/text()').extract_first() 
            caracteristicas =  response.xpath("//ul[@class='section-bullets']/li/h4/text()").extract()
        else:
            id_imovel = response.xpath("//div[contains(@class,'general-section') and contains(@class, 'publisher-section')]/span[@class='publisher-code'][2]/text()").extract_first()
            url = response.request.url
            area = response.xpath("/html/body/div[1]/main/div/div/article/div/section[1]/ul/li[1]/b/text()").extract_first()[:3]
            banheiros = response.xpath("/html/body/div[1]/main/div/div/article/div/section[1]/ul/li[3]/b/text()").extract_first()
            preco = response.xpath("/html/body/div[1]/main/div/div/aside/div/div[1]/div/div[1]/div[2]/span/text()").extract_first()[3:]
            quartos = response.xpath("/html/body/div[1]/main/div/div/article/div/section[1]/ul/li[5]/b/text()").extract_first()
            vagas_garagem = response.xpath("/html/body/div[1]/main/div/div/article/div/section[1]/ul/li[4]/b/text()").extract_first()
            condominio = response.xpath("/html/body/div[1]/main/div/div/aside/div/div[1]/div/div[4]/span/text()").extract_first()
            iptu = response.xpath("/html/body/div[1]/main/div/div/aside/div/div[1]/div/div[5]/span/text()").extract_first()
            endereco = self.get_endereco(response)
            imobiliaria = self.get_imobiliaria(response) 
            caracteristicas =  response.xpath("//ul[@class='section-bullets']/li/h4/text()").extract()
        
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
            'plataforma': 'imovelweb',
            'caracteristicas': caracteristicas
        }

        
    def get_imobiliaria(self , response):
        return response.css("html body#PROPERTY div#modal-hide-elements main div.layout-container div#main-container article.clearfix div#article-container section.general-section.article-section.publisher-section div.content-column div.column-left a h3.publisher-subtitle b::text").get()
    
    def get_endereco(self , response):
        all_elements = response.css("html body#PROPERTY div#modal-hide-elements main div.layout-container div#main-container article.clearfix div#article-container section.general-section.section-map-container div.section-location::text").getall()
        unformatted_location= " ".join(all_elements)
        formatted_location = unformatted_location.strip(' \t\n')
        return formatted_location