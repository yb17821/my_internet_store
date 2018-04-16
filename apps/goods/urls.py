from rest_framework.routers import DefaultRouter
from .views import GoodsListViewSet,CategoryViewset
from django.urls import path,include
app_name = 'goods'
router = DefaultRouter()
router.register(r'goods', GoodsListViewSet, base_name="goods")
router.register(r'categorys', CategoryViewset, base_name="categorys")
urlpatterns = [
    path(r"",include(router.urls)),
]