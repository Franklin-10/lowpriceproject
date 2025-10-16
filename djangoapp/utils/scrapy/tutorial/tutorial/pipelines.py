from asgiref.sync import sync_to_async
from lowprice.models import Product, HistoryProduct, Search 
from decimal import Decimal
import re

class SaveToDjangoPipeline:
    async def process_item(self, item, spider):
        try:
            await self.save_item_to_db(item, spider)
            
        except Exception as e:
            print(f"!!!!!!!!!! ERRO NA PIPELINE !!!!!!!!!!!!!!", flush=True)
            print(f"Item que causou o erro: {dict(item)}", flush=True)
            print(f"O erro foi: {e}", flush=True)
        
        return item

    @sync_to_async
    def save_item_to_db(self, item, spider):
        price_str = item.get('price', '0')
        price_numbers = re.search(r'[\d\.,]+', price_str)
        
        price_decimal = Decimal('0.00')
        if price_numbers:
            cleaned_price_str = price_numbers.group(0).replace('.', '').replace(',', '.')
            try:
                price_decimal = Decimal(cleaned_price_str)
            except Exception as e:
                print(f"PIPELINE-DB: Não foi possível converter o preço: {cleaned_price_str}. Erro: {e}")

        product, created = Product.objects.update_or_create(
            url=item.get('link'),
            defaults={
                'description': item.get('title'),
                'price': price_decimal,
                'image_url': item.get('image'),
            }
        )
        
        if created:
            ...
            print(f"PIPELINE-DB: Novo produto salvo -> {product.description[:50]}...", flush=True)
        else:
            ...
            print(f"PIPELINE-DB: Produto atualizado -> {product.description[:50]}...", flush=True)
            
        HistoryProduct.objects.create(
            product=product,
            price=price_decimal,
            seller=spider.name
        )

        if spider.search_id:
            try:
                search_obj = Search.objects.get(id=spider.search_id)
                search_obj.products.add(product)
                print(f"PIPELINE-DB: Produto associado à busca ID {spider.search_id}", flush=True)
            except Search.DoesNotExist:
                print(f"PIPELINE-DB: ERRO! Busca com ID {spider.search_id} não encontrada!", flush=True)