from django.contrib import admin
from .models import GoodsCategory,Goods,GoodsCategoryBrand,GoodsImage
# Register your models here.
admin.site.register(GoodsCategory)
admin.site.register(Goods)
admin.site.register(GoodsCategoryBrand)
admin.site.register(GoodsImage)