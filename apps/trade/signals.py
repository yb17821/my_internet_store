from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderInfo,ShoppingCart,OrderGoods
from random import choice
from datetime import datetime
@receiver(post_save, sender=OrderInfo)
def create_user(sender, instance=None, created=False, **kwargs):
    if created:
#不能使用self.request.user
        def get_sn():
            base_num = '1234567890'
            sn = []
            for i in range(20):
                sn.append(choice(base_num))
            return ''.join(sn)

        order_sn = get_sn()
        while OrderInfo.objects.filter(order_sn=order_sn):
            order_sn = get_sn()


        user = instance.user
        shoping_cart = ShoppingCart.objects.filter(user=user)
        money = 0
        for good_msg in shoping_cart:
            money += good_msg.goods_sum * good_msg.goods.shop_price

        instance.order_mount = money
        instance.order_sn = order_sn
        instance.trade_no = str(user)+str(datetime.now().strftime('%Y%m%d%H%M%S'))
        instance.save()
