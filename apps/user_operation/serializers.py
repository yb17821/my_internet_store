from rest_framework import  serializers
from .models import UserFav,UserLeavingMessage,UserAddress
from goods.models import Goods
from goods.serializers import GoodsSerializer
from rest_framework.validators import UniqueTogetherValidator
class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()
    class Meta:
        model = UserFav
        fields = ('id','goods')

class UserFavSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())#将user字段隐藏，并且将默认值设置为当前用户
    class Meta:
        model = UserFav
        fields = ('user','goods','id')
        # depth = 3#加了就不能post
        #验证器记住用[]括起来
        validators = [UniqueTogetherValidator(
            queryset=UserFav.objects.all(),
            fields=('user','goods'),
            message='已经收藏过了',
        )]

class LeavingMessageSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(#外键关系
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserLeavingMessage
        fields = ("id","user", "message_type", "subject", "message", "file",  "add_time")


class UserAddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = UserAddress
        fields = ("id","user", "district", "address", "signer_name", "signer_mobile")