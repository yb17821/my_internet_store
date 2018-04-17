from rest_framework import serializers
from .models import ShoppingCart, OrderInfo, OrderGoods
from random import choice
from datetime import datetime


class ShoppinglistSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ShoppingCart
        fields = ('id', 'user', 'goods', 'goods_sum')


class OrderGoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderGoods
        fields = '__all__'


class OrderInfoDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_sn = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    page_status = serializers.CharField(read_only=True)
    order_mount = serializers.CharField(read_only=True)
    pay_time = serializers.CharField(read_only=True)
    ordergoods = OrderGoodsSerializer(many=True)

    class Meta:
        model = OrderInfo
        # fields = ('id','user','order_sn', 'trade_no', 'page_status', 'post_script', 'order_mount', )
        fields = '__all__'


class OrderInfoSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_sn = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    page_status = serializers.CharField(read_only=True)
    order_mount = serializers.CharField(read_only=True)
    pay_time = serializers.CharField(read_only=True)

    class Meta:
        model = OrderInfo
        # fields = ('id','user','order_sn', 'trade_no', 'page_status', 'post_script', 'order_mount', )
        fields = '__all__'

    # 不能使用self.request.user，就不能查询金额

    # def validate(self, attrs):
    #     def get_sn():
    #         base_num = '1234567890'
    #         sn = []
    #         for i in range(20):
    #             sn.append(choice(base_num))
    #         return ''.join(sn)
    #     order_sn = get_sn()
    #     while OrderInfo.objects.filter(order_sn=order_sn):
    #         order_sn = get_sn()
    #     attrs['order_sn'] = order_sn
    #     attrs['trade_no'] = str(user)+str(datetime.now().strftime('%Y%m%d%H%M%S'))
    #     user = attrs['user']
    #     shoping_cart = ShoppingCart.objects.filter(user=user)
    #     money = 0
    #     for good_msg in shoping_cart:
    #         money += good_msg.goods_sum * good_msg.goods.shop_price
    #     attrs['order_mount'] = money
    #     return attrs

    # 不能使用self.request.user，就不能查询金额
    # def create(self, validated_data):
    #     def get_sn():
    #         base_num = '1234567890'
    #         sn = []
    #         for i in range(20):
    #             sn.append(choice(base_num))
    #         return ''.join(sn)
    #     order_sn = get_sn()
    #     while OrderInfo.objects.filter(order_sn=order_sn):
    #         order_sn = get_sn()
    #
    #     user = validated_data['user']
    #     shoping_cart = ShoppingCart.objects.filter(user=user)
    #     money = 0
    #     for good_msg in shoping_cart:
    #         money += good_msg.goods_sum * good_msg.goods.shop_price
    #     order_info = OrderInfo(**validated_data)
    #     order_info.order_sn = order_sn
    #     order_info.trade_no = str(user)+str(datetime.now().strftime('%Y%m%d%H%M%S'))
    #     order_info.order_mount = money
    #     order_info.save()
    #     return order_info
