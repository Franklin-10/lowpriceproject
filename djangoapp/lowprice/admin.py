from django.contrib import admin
from lowprice.models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = 'id', 'description', 'price', 'is_published'
    list_display_links = 'id', 'description',
    search_fields = 'id', 'description',
    list_per_page = 10
    list_filter = 'is_published',
    list_editable = 'is_published',
    ordering = '-id',
    readonly_fields = ('registration_date', 'updated_date')

# Register your models here.
