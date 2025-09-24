# scrapers/tutorial/tutorial/pipelines.py

from asgiref.sync import sync_to_async
# 1. Importe o novo model Search
from lowprice.models import Product, HistoryProduct, Search 
from decimal import Decimal
import re

class SaveToDjangoPipeline:
    async def process_item(self, item, spider):
        try:
            # 2. Passe o objeto 'spider' para a função de salvamento
            #    para que ela tenha acesso ao 'search_id'.
            await self.save_item_to_db(item, spider)
        except Exception as e:
            print(f"!!!!!!!!!! ERRO NA PIPELINE !!!!!!!!!!!!!!", flush=True)
            print(f"Item que causou o erro: {dict(item)}", flush=True)
            print(f"O erro foi: {e}", flush=True)
        
        return item

    @sync_to_async
    # 3. A função agora recebe o 'spider'
    def save_item_to_db(self, item, spider):
        # A lógica de limpeza do preço continua a mesma
        price_str = item.get('price', '0')
        price_numbers = re.search(r'[\d\.,]+', price_str)
        
        price_decimal = Decimal('0.00')
        if price_numbers:
            cleaned_price_str = price_numbers.group(0).replace('.', '').replace(',', '.')
            try:
                price_decimal = Decimal(cleaned_price_str)
            except Exception as e:
                print(f"PIPELINE-DB: Não foi possível converter o preço: {cleaned_price_str}. Erro: {e}")

        # A lógica de criar/atualizar o produto continua a mesma
        product, created = Product.objects.update_or_create(
            url=item.get('link'),
            defaults={
                'description': item.get('title'),
                'price': price_decimal,
                'image_url': item.get('image'),
            }
        )
        
        if created:
            print(f"PIPELINE-DB: Novo produto salvo -> {product.description[:50]}...", flush=True)
        else:
            print(f"PIPELINE-DB: Produto atualizado -> {product.description[:50]}...", flush=True)
            
        # A lógica de criar o histórico de preço continua a mesma
        HistoryProduct.objects.create(
            product=product,
            price=price_decimal,
            seller='Kabum'
        )

        # --- 4. NOVA LÓGICA PARA ASSOCIAR O PRODUTO À BUSCA ---
        if spider.search_id:
            try:
                # Pega o objeto da Busca correspondente ao ID que recebemos
                search_obj = Search.objects.get(id=spider.search_id)
                # Adiciona o produto encontrado à relação ManyToMany daquela busca
                search_obj.products.add(product)
                print(f"PIPELINE-DB: Produto associado à busca ID {spider.search_id}", flush=True)
            except Search.DoesNotExist:
                print(f"PIPELINE-DB: ERRO! Busca com ID {spider.search_id} não encontrada!", flush=True)