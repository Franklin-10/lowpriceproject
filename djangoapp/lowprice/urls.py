from django.contrib import admin
from django.urls import path
from lowprice.views import index, search, results_api

app_name= 'lowprice'

urlpatterns = [
    path('', index, name='index'),
    path('search/', search, name='search'),
    # path('results/', results, name='results'),
    path('api/results/<int:search_id>/', results_api, name='results_api'),
]
