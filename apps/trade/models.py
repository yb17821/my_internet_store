from django.db import models
# from users.models import UserProfile
from goods.models import Goods
from django.contrib.auth import get_user_model
#获取当前用户模型，其实就是获取settings.AUTH_USER_MODEL。
#from django.conf import settings
User = get_user_model()


# Create your models here.
class ShoppingCart(models.Model):
    '''
    购物车
    '''
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING,verbose_name='用户')
    goods = models.ForeignKey(Goods, on_delete=models.DO_NOTHING,verbose_name='商品')
    goods_sum = models.IntegerField(default=0)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "购物车"
        verbose_name_plural = verbose_name
        unique_together =('user','goods')

    def __str__(self):
        return "%s(%d)".format(self.goods.name, self.goods_sum)


class OrderInfo(models.Model):
    '''
    订单
    '''
    ORDER_STATUS = (
        ('success', '成功'),
        ('cancel', '取消'),
        ('cancel', '待支付'),
    )
    # PAY_TYPE = (
    #     ('alipy', '支付宝'),
    #     ('wechat', '微信'),
    # )
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.DO_NOTHING)
    order_sn = models.CharField(max_length=30, unique=True, verbose_name='用户',null=True, blank=True)
    # nonce_str = models.CharField(max_length=50,null=True,blank=True,verbose_name=u'随')
    trade_no = models.CharField(max_length=100, unique=True, verbose_name='交易编号', null=True, blank=True)
    page_status = models.CharField(choices=ORDER_STATUS, max_length=10, verbose_name='订单状态',default='success')
    post_script = models.CharField(max_length=11, verbose_name='订单留言')
    order_mount = models.FloatField(default=0.0, verbose_name='订单金额')
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')
    address = models.CharField(max_length=100, default="", verbose_name='收货地址')
    signer_name = models.CharField(max_length=20, default="", verbose_name='收货人')
    signer_mobile = models.CharField(max_length=11, verbose_name='签收电话')

    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u"订单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order_sn)


class OrderGoods(models.Model):
    '''
    订单的商品详情
    '''
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE, verbose_name="订单信息",related_name='ordergoods')
    goods = models.ForeignKey(Goods, on_delete=models.DO_NOTHING, verbose_name='商品')
    goods_sum = models.IntegerField(default=0, verbose_name='商品数量')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u"订单的商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.order_sn)
