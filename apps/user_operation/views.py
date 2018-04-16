from django.shortcuts import render
from rest_framework import mixins, viewsets
from .serializers import UserFavSerializer, UserFavDetailSerializer, LeavingMessageSerializer, UserAddressSerializer
from .models import UserLeavingMessage, UserFav, UserAddress
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import TokenAuthentication


# Create your views here.
class UserFavViewset(mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    '''
    list:所有收藏
    create:添加收藏
    retrieve:收藏详情
    destory:删除收藏
    '''

    # serializer_class = UserFavSerializer
    def get_serializer_class(self):
        if self.action == 'create':
            return UserFavSerializer
        elif self.action == 'list':
            return UserFavDetailSerializer
        return UserFavDetailSerializer

    # 设置本页面需要的验证类，没有则使用settings里的默认配置
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication,)

    permission_classes = (IsAuthenticated,  # IsAuthenticated,验证是否登录
                          # IsOwnerOrReadOnly,自定义的验证类，验证当前用户和收藏的用户是不是同一个
                          IsOwnerOrReadOnly,  # 外键关系采用
                          )

    lookup_field = 'goods_id'  # 设置详情也的搜索条件，默认是数据表的id，look_up可以指定表里的某个字段为搜索条件
                                # 为了方便的使用显示是否收藏和取消收藏功能，所以把搜索条件改为goods_id,
                                # 否则就要根据goods_id查询收藏id，再做查询和删除操作

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)


class LeavingMessageViewset(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    '''
    list:获取留言
    create:添加留言
    destory:删除留言
    '''
    serializer_class = LeavingMessageSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication,)
    permission_classes = (
        IsAuthenticated,
        IsOwnerOrReadOnly,
    )

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class UserAddressViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    '''
    list:所有收货地址
    create:添加收货地址
    updata:更新收货地址
    destory:删除收货地址
    '''
    serializer_class = UserAddressSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,
                          IsOwnerOrReadOnly
                          )

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
    # def get_object(self):
    #     return UserAddress.objects.get(id=10)
