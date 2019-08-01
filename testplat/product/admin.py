from django.contrib import admin

# Register your models here.

from product.models import ProductInfo


admin.site.register(ProductInfo)