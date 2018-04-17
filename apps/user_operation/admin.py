from django.contrib import admin
from .models import UserFav,UserAddress,UserLeavingMessage
# Register your models here.
admin.site.register(UserFav)
admin.site.register(UserAddress)
admin.site.register(UserLeavingMessage)
