from django.db import models
from django.utils import timezone


class Product(models.Model):
    url = models.URLField(max_length=600, unique=True)
    description = models.CharField(max_length=400)
    price = models.DecimalField(max_digits=10, decimal_places=2, default='0.00')
    image_url = models.URLField(max_length=600, default='')
    registration_date = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True, help_text='Desmarque ' \
    'este campo para parar a veiculação')
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.description
    

class HistoryProduct(models.Model):
    price = models.FloatField(max_length=5)
    registration_date = models.DateTimeField(default=timezone.now)
    seller = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=False, null=True)


class Search(models.Model):
    search_term = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product)
    
    def __str__(self):
        return f"Busca por '{self.search_term}' em {self.timestamp.strftime('%d/%m/%Y %H:%M')}"


# Create your models here.
