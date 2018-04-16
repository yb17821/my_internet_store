# coding=utf-8
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from .filters import GoodsFilter
from .models import Goods, GoodsCategory, Banner
from .serializers import GoodsSerializer, CategorySerializer, BannerSerializer,IndexCategorySerializer


# Create your views here.
# class GoodsListView(APIView):
#     '''
#     hahaha
#     '''
#     def get(self, request, format=None):
#
#         goods = Goods.objects.all()[:10]
#         serializer = GoodsSerializer(goods,many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = GoodsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class GoodsListView(mixins.ListModelMixin,generics.GenericAPIView):
#     '''
#     商品列表
#     '''
#     queryset = Goods.objects.all()[:10]
#     serializer_class = GoodsSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
# class GoodsResultsSetPagination(PageNumberPagination):#自定义分页类
#     page_size = 2#默认每页显示的多少
#     page_size_query_param = 's'#定制url中设置页面大小的参数的名字为p，默认是page_size
#     page_query_param = 'p'#定制url中设置页码的参数的名字为p，默认是page
#     max_page_size = 4#限制用户能设置的页面大小的最大数
#     last_page_strings = 'l'#定制url中设置末页的参数为l，默认是last，page=last可跳转至最后一页
# from rest_framework.pagination import LimitOffsetPagination
# class GoodsResultsSetPagination(LimitOffsetPagination):#自定义分页类
#     default_limit = 3#设置默认的limit，默认值是PAGE_SIZE,limit等同于page_size
#     limit_query_param = 'li'
#     offset_query_param = 'of'
#     max_limit = 9
# class GoodsListViewSet(viewsets.ModelViewSet):
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#     filter_backends = (DjangoFilterBackend,)
#     filter_fields = ('name','shop_price')


# noinspection PyUnresolvedReferences
class GoodsListViewSet(CacheResponseMixin,mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    # 第一种区间过滤，使用类，可以在调api时使用
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'shop_price')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)

        return Response(serializer.data)

    # authentication_classes = (TokenAuthentication,)
    # 第二种，使用函数，只能在url使用
    # filter_backends = (SearchFilter, OrderingFilter)
    # search_fields = ('name','shop_price')
    # ordering_fields = ('id','shop_price')
    #
    # def get_queryset(self,):
    #     price_max = self.request.query_params.get('price_max', None)
    #     price_min = self.request.query_params.get('price_min', None)
    #     queryset = Goods.objects.all()
    #     if price_max:
    #         queryset = queryset.filter(shop_price__lte=price_max)
    #     if price_min:
    #         queryset = queryset.filter(shop_price__gte=price_min)
    #     return queryset


class CategoryViewset(CacheResponseMixin,mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    list:商品分类列表
    retrieve:商品分类详情
    '''
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


# class BannerViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
#     queryset = Banner.objects.all()
#     serializer_class = BannerSerializer


class BannerViewset(CacheResponseMixin,mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取轮播图列表
    """
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer


class IndexCategoryViewset(CacheResponseMixin,mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页商品分类数据
    """
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=["生鲜食品", "酒水饮料"])
    serializer_class = IndexCategorySerializer
