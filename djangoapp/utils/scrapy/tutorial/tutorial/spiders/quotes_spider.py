import scrapy
from scrapy_playwright.page import PageMethod # Importe o PageMethod

class KabumSpider(scrapy.Spider):
    name = "kabum"

    def __init__(self, search_term='controle ps5', search_id=None, *args, **kwargs):
        super(KabumSpider, self).__init__(*args, **kwargs)
        self.search_term = search_term
        self.search_id = search_id

    def start_requests(self):
        url = f"https://www.kabum.com.br/busca/{self.search_term}"
        
        yield scrapy.Request(
            url, 
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod("screenshot", path="kabum.png", full_page=True),
                    PageMethod("wait_for_selector", "article.productCard"),
                ]
            }
        )

    def parse(self, response):
        # A lógica de extração continua a mesma por enquanto
        product_containers = response.css('article.productCard')

        for product in product_containers:
            relative_link = product.css('a.productLink::attr(href)').get()
            full_link = response.urljoin(relative_link)
            link_image = product.css('img.imageCard').xpath("@src").get()
            full_link_image = response.urljoin(link_image)

            yield {
                'title': product.css('span.nameCard::text').get(),
                'price': product.css('span.priceCard::text').get(),
                'image': full_link_image,
                'link': full_link,
            }

            