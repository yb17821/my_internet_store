from rest_framework import serializers
from  .models import UserProfile,VerifyCode
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
import re
from datetime import datetime,timedelta
from django.conf import settings
User = get_user_model()
class UserRegSerializer(serializers.ModelSerializer):#required=True表示这是一个必填字段
    code = serializers.CharField(required=True,write_only = True, max_length=4,min_length=4,help_text='验证码',
                                 error_messages={
                                     'max_length':'长度不要超过4',
                                     'min_length':'长度不要少于4',
                                     'required':'此项必填',
                                     'blank':'此项必填',
                                 },label='验证码')
    username = serializers.CharField(required=True,allow_blank=False,label='用户名',
                                     validators=[UniqueValidator(queryset=UserProfile.objects.all(),message='用户已存在')])
    password = serializers.CharField(required=True,write_only=True,label='密码',style={'input_type':'password'})


    # 重写create，对密码加密
    # def create(self,validated_data):
    #     # user =super(UserRegSerializer,self).create(validated_data=validated_data)
    #     user = User(**validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user



    def validate_code(self,code):
        #前端传过来的值都会存放serializers.ModelSerializer.initial_data里
        #因为是用手机号注册，所以username等于mobile
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')

        if verify_records:
            last_record = verify_records[0]
            five_mintes_ago = datetime.now()-timedelta(minutes=5)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError('验证码过期')
            if last_record.code != code:
                raise serializers.ValidationError('验证码错误')
        else:
            raise serializers.ValidationError('验证码错误')


    #直接修改的方式,attrs存储这验证后的数据,
    #code 加write_only,保证在返回数据给前端时不会不会将fields里的‘code’字段序列化，否则出错
    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        # attrs['password'] = make_password(attrs['password'])#对密码进行加密
        del attrs["code"]
        return attrs


    class Meta:
        model = UserProfile
        fields = ('id','username','code','password')
class UserChangePwdSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    class Meta:
        model = UserProfile
        fields = ('id','username','password')
    # def update(self, instance, validated_data):
    #     password = validated_data['password']
    #     instance.set_password(password)
    #     instance.save()
    #     return instance
    def validate(self, attrs):
        password = attrs.get('password',None)
        if password:
            attrs['password'] = make_password(attrs['password'])#对密码进行加密
        return attrs

class UserDetailSerizlizer(serializers.ModelSerializer):
    '''
    用户详情
    '''
    class Meta:
        model = UserProfile
        fields = ('id','username', 'gender', 'birthday','email','mobile')

    # def update(self, instance, validated_data):
    #     password = validated_data['password']
    #     instance.set_password(password)
    #     instance.save()
    #     return instance
    # def validate(self, attrs):
    #     password = attrs.get('password',None)
    #     if password:
    #         attrs['password'] = make_password(attrs['password'])#对密码进行加密
    #     return attrs

class SmsSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(max_length=11)
    def validate_mobile(self, mobile):
        '''
        验证手机号码
        '''
        #手机是否注册
        if User.objects.filter(mobile = mobile).count():
            raise serializers.ValidationError('用户已存在')
        #验证手机号吗是否合法
        # REGEX_MOBILE = r'1[3-8]\d{9}'
        if not re.match(settings.REGEX_MOBILE,mobile):
            raise serializers.ValidationError('手机好吗不合法')
        #验证码发送频率
        one_mintes_ago = datetime.now()-timedelta(minutes=1)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago,mobile=mobile):
            raise serializers.ValidationError('距离上次发送不超过一分钟')
        return mobile
    class Meta:
        model = VerifyCode
        fields = ('mobile',)


