import scrapy
from playwright.async_api import Page

class ecommerceB(scrapy.Spider):
    name = "ecommerceB"
    custom_settings = {
        # User-Agent adicionado como custom_settings pra evitar o bloqueio 403 nesse ecommerce específico
        'USER_AGENT': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    }
    # SITE_CONFIG onde você pode facilmente colocar os seletores css do site a ser raspado.
    SITE_CONFIG = {
        'base_url': "https://yoursite.com.br/search/{}", # URL de busca de produtos do seu site
        'selectors': {
            # Os seletores que deseja buscar preencha ex: li.identificador
            'container': 'Your selector CSS here',  # Div que engloba todos os seletores filhos que deseja buscar
            'title': "Your selector CSS here::text", #Selector CSS referente ao titulo/descrição do produto
            'price': "Your selector CSS here::text", #Selector CSS referente ao preço do produto
            'img_data': 'Your selector CSS here::attr(data-src)', #Selector CSS referente ao img_data do produto
            'img_src': 'Your selector CSS here::attr(src)', #Selector CSS referente ao img_src do produto
            'link': "Your selector CSS here::attr(href)", #Selector CSS referente ao link do produto
            "next_page": "Your selector CSS here", #Selector CSS referente ao botão de proóxima página do produto
        }
    }

    def __init__(self, search_term='', search_id =None, *args, **kwargs):
        super(ecommerceB, self).__init__(*args, **kwargs)
        self.search_term = search_term
        self.search_id = search_id

    def start_requests(self):
        url = self.SITE_CONFIG['base_url'].format(self.search_term, self.search_term)
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
        if req.resource_type in {"document", "script", "fetch", "xhr", "json"}:
            return False
        
        if req.resource_type in {"image", "stylesheet", "font", "media", "text"}:
            return True
        
        return False
    
    async def parse(self, response):
        s = self.SITE_CONFIG['selectors']
        page: Page = response.meta["playwright_page"]
        #Deixei o tracing ativado pra caso queira ver como o playwright esta atuando com seu código, ótimo pra debugar
        await page.context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page_count = 1
        """ Máximo de páginas que o scraper vai buscar, note que ao buscar mais páginas o tempo pro resultado
        ser mostrado aumenta"""  
        max_pages = 1 
        await page.route("**/*", lambda route, req: route.abort() if self._block_resources(req) else route.continue_())

        try:
            while page_count <= max_pages:
                print(f"\n--- [PÁGINA {page_count}] INICIANDO COLETA ---", flush=True)
                await page.wait_for_selector(s['container'], state='visible')

                html_content = await page.content()
                selector = scrapy.Selector(text=html_content)

                products_container = selector.css(s['container'])
                print(f"--- [PÁGINA {page_count}] Encontrados {len(products_container)} produtos. ---", flush=True)
                for product in products_container:
                    #Pega o atributo data-src das imagens que não foram carregadas ainda
                    image_url = product.css(s['img_data']).get()
                    if not image_url:
                        #Caso tenham sido carregadas pega o src
                        image_url = product.css(s['img_src']).get()
                    
                    yield{
                        'title': product.css(s['title']).get(),
                        'price': product.css(s['price']).get(),
                        'image': image_url,
                        'link': response.urljoin(product.css(s['link']).get())
                    }
                if page_count >= max_pages:
                    break
                next_page_selector = s['next_page']
                next_button = page.locator(next_page_selector)


                if await next_button.count() > 0 and await next_button.is_visible():
                    print(f"\n--- [PÁGINA {page_count}] Encontrou próxima página. Clicando... ---", flush=True)
                    await next_button.scroll_into_view_if_needed()
                    await next_button.click(force=True)
                    page_count += 1


                else:
                    print(f"\n--- [PÁGINA {page_count}] Não encontrou próxima página. Fim da raspagem. ---", flush=True)
                    break
        except Exception as e:
            print(f"!!!!!!!!!! ERRO INESPERADO NO PARSE !!!!!!!!!!!!!!", flush=True)
            print(f"O erro foi: {e}", flush=True)
        finally:
            await page.context.tracing.stop(path=f"trace.zip")
            await page.close()

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
    
