from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import ShoppinglistSerializer,OrderInfoSerializer,OrderInfoDetailSerializer
from .models import ShoppingCart,OrderGoods,OrderInfo
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
class ShoppinglistCartViewset(viewsets.ModelViewSet):
    '''
    购物车功能
    list:
        获取购物车详情
    create:
        加入购物车
    delete:删除购物记录
    '''
    permission_classes = (IsOwnerOrReadOnly,IsAuthenticated)
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
    serializer_class = ShoppinglistSerializer
    lookup_field = 'goods'
    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)
    def create(self, request, *args, **kwargs):
        obj = ShoppingCart.objects.filter(user=self.request.user,goods=request.data['goods'])
        if obj:
            # request.data不可以被修改
            # partial = kwargs.pop('partial', False)#判断是不是部分修改
            instance = obj[0]
            goods_sum = str(instance.goods_sum + int(request.data['goods_sum']))
            serializer = self.get_serializer(instance, data={'goods_sum':goods_sum}, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            return Response(serializer.data)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class OrderInfoViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet):
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # serializer_class = OrderInfoSerializer
    def get_serializer_class(self):
        if self.action ==  'create':
            return OrderInfoSerializer
        return OrderInfoDetailSerializer



    def get_queryset(self):
        return OrderInfo.objects.filter(user = self.request.user)

    def perform_create(self, serializer):
        order = serializer.save()
        shoping_cart = ShoppingCart.objects.filter(user=self.request.user)
        for good_msg in shoping_cart:
            OrderGoods.objects.create(order=order,goods=good_msg.goods,goods_sum=good_msg.goods_sum)
            good_msg.delete()










