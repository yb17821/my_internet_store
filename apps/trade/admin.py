from django.contrib import admin
from .models import ShoppingCart,OrderInfo,OrderGoods
# Register your models here.
admin.site.register(ShoppingCart)
admin.site.register(OrderInfo)
admin.site.register(OrderGoods)