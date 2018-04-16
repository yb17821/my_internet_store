from django.contrib import admin
from .models import UserProfile,VerifyCode
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(VerifyCode)