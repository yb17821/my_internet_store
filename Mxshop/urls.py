"""Mxshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
import xadmin
from users.views import UserViewset,SmsCodeViewset,UserChangePwdViewSet
from goods.views import GoodsListViewSet,CategoryViewset,BannerViewset,IndexCategoryViewset
from user_operation.views import UserFavViewset,LeavingMessageViewset,UserAddressViewset
from trade.views import ShoppinglistCartViewset,OrderInfoViewSet
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_jwt.views import obtain_jwt_token
router = DefaultRouter()
router.register(r'goods', GoodsListViewSet, base_name="goods")
router.register(r'categorys', CategoryViewset, base_name="categorys")
router.register(r'users', UserViewset, base_name="users")
router.register(r'codes', SmsCodeViewset, base_name="codes")
router.register(r'userfavs', UserFavViewset, base_name="userfavs")
router.register(r'messages', LeavingMessageViewset, base_name="messages")
router.register(r'address', UserAddressViewset, base_name="address")
router.register(r'userpwd', UserChangePwdViewSet, base_name="userpwd")
router.register(r'shopcarts', ShoppinglistCartViewset, base_name="shopcarts")
router.register(r'orders', OrderInfoViewSet, base_name="orders")
router.register(r'banners', BannerViewset, base_name="banners")
router.register(r'indexgoods', IndexCategoryViewset, base_name="indexgoods")
urlpatterns = [
    # path('goods/',include('goods.urls')),
    path(r"",include(router.urls)),
    path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    #drf自带的token认证模式
    path('api-token-auth/',ObtainAuthToken),
    #jwt的认证借口
    path('login/', obtain_jwt_token),
    # path('goods/',GoodsListViewSet.as_view(),name='goods_list'),
    path('docs/',include_docs_urls(title='标题在url设置')),
    path('api-auth/', include('rest_framework.urls')),

]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
