from django.contrib import admin
from django.urls import path
from lowprice.views import index

app_name= 'lowprice'

urlpatterns = [
    path('', index, name='index'),
]
