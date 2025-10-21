import scrapy

class ecommerceA(scrapy.Spider):
    name = "ecommerceA"
    custom_settings = {
        'RETRY_TIMES': 5,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 408, 403, 429],
    }
    SITE_CONFIG = {
        'base_url': "https://yoursite.com.br/search/{}", # URL de busca de produtos do seu site
        'selectors': {
            # Os seletores que deseja buscar preencha ex: li.identificador
            'container': 'Your selector CSS here', 
            'title': "Your selector CSS here::text", #Selector CSS referente ao titulo/descrição do produto
            'price': "Your selector CSS here::text", #Selector CSS referente ao preço do produto
            'img_src': 'Your selector CSS here::attr(src)', #Selector CSS referente ao img_src do produto
            'link': "Your selector CSS here::attr(href)", #Selector CSS referente ao link do produto
            "next_page": "Your selector CSS here", #Selector CSS referente ao botão de proóxima página do produto
        }
    }

    def __init__(self, search_term='', search_id=None, *args, **kwargs):
        super(ecommerceA, self).__init__(*args, **kwargs)
        self.search_term = search_term
        self.search_id = search_id

    def start_requests(self):
        url = self.SITE_CONFIG['base_url'].format(self.search_term)
        yield scrapy.Request(
            url,
            callback=self.parse,
            meta={
                "playwright": True,
                "playwright_include_page": True, 
                "errback": self.errback,
            }
        )
    def _block_resources(self, req):
        """Bloqueia recursos desnecessários para acelerar o carregamento."""
        if req.resource_type in {"document", "script", "fetch", "xhr", "json"}:
            return False
        
        if req.resource_type in {"image", "stylesheet", "font", "media", "text"}:
            return True
        
        return False

    async def parse(self, response):
        page = response.meta["playwright_page"]
        page_count = 1
        max_pages = 1
        s = self.SITE_CONFIG['selectors']
        await page.route("**/*", lambda route, req: route.abort() if self._block_resources(req) else route.continue_())

        try:

            while page_count <= max_pages:
                print(f"\n--- [PÁGINA {page_count}] INICIANDO COLETA ---", flush=True)
                
                await page.wait_for_selector(s['container'], state='visible')
                
                html_content = await page.content()
                selector = scrapy.Selector(text=html_content)

                product_containers = selector.css(s['container'])
                    
                for product in product_containers:
                    yield {
                        'title': product.css(s['title']).get(),
                        'price': product.css(s['price']).get(),
                        'image': response.urljoin(product.css(s['img_src']).get()),
                        'link': response.urljoin(product.css(s['link']).get()),
                    }

                next_page_selector = s['next_page']
                next_button = page.locator(next_page_selector)
                
                if await next_button.count() > 0 and await next_button.is_visible():
                    print(f"\n--- [PÁGINA {page_count}] Encontrou próxima página. Clicando... ---", flush=True)
                    page_count += 1
                    await next_button.click()

                else:
                    print(f"\n--- [PÁGINA {page_count}] Não encontrou próxima página. Fim da raspagem. ---", flush=True)
                    break
        
        except Exception as e:
            print(f"!!!!!!!!!! ERRO INESPERADO NO PARSE !!!!!!!!!!!!!!", flush=True)
            print(f"O erro foi: {e}", flush=True)
        finally:
            await page.close()

    async def errback(self, failure):
        self.log(f"Erro ao processar a requisição: {failure.request.url}")
        page = failure.request.meta["playwright_page"]
        await page.close()