from django.db import models
from goods.models import Goods
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class UserFav(models.Model):
    '''
    收藏
    '''
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='用户')
    goods = models.ForeignKey(Goods, on_delete=models.DO_NOTHING, verbose_name='商品', help_text='商品id')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u"用户收藏"
        verbose_name_plural = verbose_name
        unique_together = ('user', 'goods')  # 相互绑定，当有相同的一对存储时，数据库报错

    def __str__(self):
        return str(self.user.name)


class UserLeavingMessage(models.Model):
    """
    用户留言
    """
    MESSAGE_CHOICES = (
        (1, "留言"),
        (2, "投诉"),
        (3, "询问"),
        (4, "售后"),
        (5, "求购")
    )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="用户")
    message_type = models.IntegerField(default=1, choices=MESSAGE_CHOICES, verbose_name="留言类型",
                                       help_text=u"留言类型: 1(留言),2(投诉),3(询问),4(售后),5(求购)")
    subject = models.CharField(max_length=100, default="", verbose_name="主题")
    message = models.TextField(default="", verbose_name="留言内容", help_text="留言内容")
    file = models.FileField(upload_to="message/images/", verbose_name="上传的文件", help_text="上传的文件", null=True, blank=True)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户留言"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.subject


class UserAddress(models.Model):
    """
        用户收货地址
        """
    user = models.ForeignKey(User, verbose_name="用户",on_delete=models.DO_NOTHING)
    province = models.CharField(max_length=100, default="", verbose_name="省份")
    city = models.CharField(max_length=100, default="", verbose_name="城市")
    district = models.CharField(max_length=100, default="", verbose_name="区域")
    address = models.CharField(max_length=100, default="", verbose_name="详细地址")
    signer_name = models.CharField(max_length=100, default="", verbose_name="签收人")
    signer_mobile = models.CharField(max_length=11, default="", verbose_name="电话")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "收货地址"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address
