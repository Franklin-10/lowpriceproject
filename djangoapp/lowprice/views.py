from django.shortcuts import render, redirect
from utils.product_request import search_request
from utils.tasks import run_scrapy_spider
from django.conf import settings      # 1. IMPORTE O SETTINGS
from lowprice.models import Product, Search


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

        run_scrapy_spider.delay(search_term=search_value, search_id=new_search.id)
    
        return redirect('lowprice:results')

    return render(
        request,
        'lowprice/pages/index.html',
    )

def results(request):
    latest_search =  None
    results_data = []
    try:
        latest_search = Search.objects.latest('timestamp')

        results_data = latest_search.products.all().order_by('-updated_date')
    except Search.DoesNotExist:
        pass

    
    return render(
        request,
        'lowprice/pages/results.html',
        context= {
            'products': results_data,
            'search_object': latest_search,
        }
    )