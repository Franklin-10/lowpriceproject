from django.shortcuts import render, redirect
from django.http import JsonResponse
from utils.tasks import run_scrapy_spider, start_all_requests
from django.conf import settings    
from lowprice.models import Product, Search, SearchSiteStatus, HistoryProduct


# Create your views here.

def index(request):
    return render(
        request,
        'lowprice/pages/index.html'
    )

def search(request):
    search_value = request.GET.get('search', '').strip()

    if search_value:
        new_search = Search.objects.create(search_term=search_value)

        start_all_requests.delay(search_term=search_value, search_id=new_search.id)
    
        return JsonResponse({'status': 'ok', 'search_id': new_search.id})

    return JsonResponse({'status': 'error', 'message': 'termo de busca vazio'}, status=400)

# def results(request):
#     latest_search =  None
#     results_data = []
#     try:
#         latest_search = Search.objects.latest('timestamp')

#         results_data = latest_search.products.all().order_by('-updated_date')
#     except Search.DoesNotExist:
#         pass

    
#     return render(
#         request,
#         'lowprice/pages/results.html',
#         context= {
#             'products': results_data,
#             'search_object': latest_search,
#         }
#     )

def results_api(request, search_id):

    try:
        search_istance = Search.objects.get(id=search_id)
        statuses = search_istance.site_status.all()

        if all(s.status in ("COMPLETED", "FAILED") for s in statuses):
            products_by_seller = {}
            products = search_istance.products.all().order_by('price')

            for product in products:
                try:
                    latest_history = product.history.latest("registration_date")
                    seller = latest_history.seller

                    if seller not in products_by_seller:
                        products_by_seller[seller] = []
                                
                    products_by_seller[seller].append({
                        'description': product.description,
                        'price': str(product.price),
                        'url': product.url,
                        'image_url': product.image_url,
                        'seller': seller,
                    })
                except HistoryProduct.DoesNotExist:
                        print(f"Produto {product.id} não tem histórico")
                        continue
            return JsonResponse({
                'status': 'done',
                'products_by_seller': products_by_seller,
                'search_term': search_istance.search_term,
            })
        else:
            return JsonResponse({
                'status': 'searching',
                'products_by_seller': {},
            })
    
    except Search.DoesNotExist:
        return JsonResponse({'status': 'not_found', 'products_by_seller': {}})

    