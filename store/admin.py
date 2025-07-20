from django.contrib import admin
from .models import Category, Product, ProductSize

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'gender', 'price', 'sale_price', 'available', 'featured', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'category', 'gender', 'featured']
    list_editable = ['price', 'sale_price', 'available', 'featured']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    list_per_page = 20

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ['product', 'size', 'price', 'stock']
    list_filter = ['product', 'size']
    search_fields = ['product__name', 'size']
